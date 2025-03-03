import os
import re
import subprocess
import sys

def extract_subtitles(file_path):
    """
    Extrae las pistas de subtítulos de un archivo MKV.
    """
    # Obtiene la información de las pistas del archivo con mkvmerge.
    cmd = ['mkvmerge', '-i', file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Verificar si el comando se ejecutó correctamente
    if result.returncode != 0:
        print(f"[ERROR] El comando mkvmerge falló con el código de salida {result.returncode}")
        print(f"[ERROR] Mensaje de error: {result.stderr}")
        return

    output = result.stdout
    print(f"[DEBUG] Salida de mkvmerge:\n{output}")

    subtitle_tracks = []
    # Patrón para identificar las pistas de subtítulos en la salida.
    # Ejemplo de línea: "Track ID 2: subtitles (S_TEXT/ASS)"
    pattern = re.compile(r"Track ID (\d+): subtitles \(([^)]+)\)")
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            track_id = match.group(1)
            track_format = match.group(2)
            # Determinar la extensión de salida según el formato
            if "SRT" in track_format.upper():
                ext = ".srt"
            elif "ASS" in track_format.upper() or "SUBSTATIONALPHA" in track_format.upper():
                ext = ".ass"
            else:
                ext = ".sub"
            
            subtitle_tracks.append((track_id, ext))
    
    if not subtitle_tracks:
        print(f"[INFO] No se encontraron pistas de subtítulos en: {file_path}")
        return

    # Construir el comando para extraer todas las pistas de subtítulos encontradas.
    # Se creará un archivo de salida por cada pista, nombrado a partir del archivo original.
    cmd_extract = ['mkvextract', 'tracks', file_path]
    for track_id, ext in subtitle_tracks:
        base = os.path.splitext(file_path)[0]
        output_filename = f"{base}_track{track_id}{ext}"
        cmd_extract.append(f"{track_id}:{output_filename}")

    print("Ejecutando:", " ".join(cmd_extract))
    subprocess.run(cmd_extract)

def main():
    # Obtener la ruta de la carpeta desde argumentos o por input
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("Introduce la ruta de la carpeta: ")

    if not os.path.isdir(folder):
        print(f"'{folder}' no es una ruta válida.")
        return

    # Procesa cada archivo MKV en la carpeta especificada
    for filename in os.listdir(folder):
        if filename.lower().endswith(".mkv"):
            file_path = os.path.join(folder, filename)
            print(f"\n[PROCESANDO] {file_path}")
            extract_subtitles(file_path)

if __name__ == "__main__":
    main()
