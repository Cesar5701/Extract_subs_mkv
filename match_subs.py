import os
import re
import sys
from pathlib import Path

def encontrar_correspondencias(dir_videos, dir_subs):
    patron_video = re.compile(r'(S\d{2}E\d{2})', re.IGNORECASE)
    patron_sub = re.compile(r'(S\d{2}E\d{2})', re.IGNORECASE)  # Regex simplificado
    
    videos = [f for f in os.listdir(dir_videos) if f.lower().endswith('.mkv')]
    
    for video in videos:
        match_video = patron_video.search(video)
        if not match_video:
            continue
            
        codigo = match_video.group(1).upper()
        print(f"\nVideo: {video}")
        print("Subtítulos correspondientes:")
        
        encontrados = False
        for sub in Path(dir_subs).glob('*.ass'):
            match_sub = patron_sub.search(sub.name)
            if not match_sub:
                continue
                
            sub_codigo = match_sub.group(1).upper()
            
            if sub_codigo == codigo:
                encontrados = True
                print(f"  ▸ {sub.name}")  # Solo muestra el nombre del archivo
        
        if not encontrados:
            print("  ▸ No se encontraron subtítulos")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} [directorio_videos] [directorio_subtitulos]")
        sys.exit(1)
    
    dir_videos = sys.argv[1]
    dir_subs = sys.argv[2]
    
    if not os.path.isdir(dir_videos):
        print(f"Error: Directorio de videos no encontrado: {dir_videos}")
        sys.exit(1)
        
    if not os.path.isdir(dir_subs):
        print(f"Error: Directorio de subtítulos no encontrado: {dir_subs}")
        sys.exit(1)

    encontrar_correspondencias(dir_videos, dir_subs)