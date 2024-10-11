from tkinter import *
from tkinter import ttk
import yt_dlp
import subprocess
import os

# Configurar ventana principal
root = Tk()
root.geometry('500x400')
root.resizable(0,0)
root.title("YouTube Downloader & Converter")
root.configure(bg="#FFFACD")

# Título
Label(root, text='YouTube Video Downloader', font=('Times New Roman', 20, 'bold'), bg="#f2eee3", fg="red").pack()

# Campo para el link de YouTube
link = StringVar()
Label(root, text='Pega el link de YouTube aqui:', font=('Times New Roman', 20, 'bold'), bg="#f2eee3").place(x=40, y=60)
link_enter = Entry(root, width=50, textvariable=link).place(x=32, y=100)
# Opciones de formato
format_var = StringVar(value="mp3")
Label(root, text='Formato de salida:', font=('Times New Roman', 15, 'bold'), bg="#f2eee3").place(x=40, y=160)
ttk.Combobox(root, textvariable=format_var, values=["mp3", "flac", "aac"]).place(x=250, y=165)


# Directorio de salida (puedes modificarlo)
output_dir = "Descargas"

# Función para descargar el video de YouTube
def downloader():
    video_url=str(link.get())
    select_format = format_var.get()
    ydl_opts = {
        'format': 'bestaudio/best', #descargar solo el audio en el mejor formato posible 
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec':select_format,
            'preferredquality':'192',
        }]  
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        Label(root, text='DESCARGADO', font='arial 15', bg="#f2eee3", fg="green").place(x=180, y=260)
    except Exception as e:
        Label(root, text='ERROR EN DESCARGA', font='arial 15', bg="#f2eee3", fg="red").place(x=150, y=200)
# Función para convertir el archivo descargado al formato deseado
def converter():
    input_file = downloader()
    output_file = os.path.join(output_dir, f"output.{format_var.get()}")
    
    # Comando para convertir usando ffmpeg
    command = [
        'ffmpeg', '-i', input_file, output_file
    ]

    try:
        subprocess.run(command, check=True)
        Label(root, text='CONVERTIDO', font='arial 15', bg="#f2eee3", fg="green").place(x=180, y=245)
    except Exception as e:
        Label(root, text='ERROR EN CONVERSIÓN', font='arial 15', bg="#f2eee3", fg="red").place(x=150, y=245)

# Botones para descargar y convertir
download_btn = Button(root, text='DESCARGAR', font='arial 15 bold', bg='pale violet red', padx=2, command=downloader, fg="blue").place(x=150, y=220)
convert_btn = Button(root, text='Convertir', font='arial 15 bold', bg='pale violet red', padx=2, command=converter, fg="blue").place(x=150, y=300)

root.mainloop()
