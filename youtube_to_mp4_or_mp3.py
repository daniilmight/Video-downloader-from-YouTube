from tkinter import *
from pytube import YouTube
import os
from moviepy.editor import *
from tkinter import Tk

def get_clipboard_data():
    c = Tk()
    c.withdraw()
    clip = c.clipboard_get()
    c.update()
    c.destroy()
    return clip

def download_video():
    url = entry.get()
    if not url:
        # Если URL не введен, попробуйте взять его из буфера обмена
        clipboard_data = get_clipboard_data()
        entry.delete(0, END)
        entry.insert(0, clipboard_data)
        url = entry.get()
    
    if url:
        yt = YouTube(url)
        video_stream = yt.streams.first()
        video_stream.download(output_path=os.path.expanduser('~/Downloads'), filename='temp.mp4')
        status_label.config(text="Видео успешно скачано!")
    else:
        status_label.config(text="Пожалуйста, введите URL")

def convert_to_mp3():
    video = os.path.expanduser('~/Downloads/temp.mp4')
    audio = os.path.expanduser('~/Downloads/temp.mp3')
    file = AudioFileClip(video)
    file.write_audiofile(audio)
    file.close()
    status_label.config(text="Конвертация завершена!")

def insert_from_clipboard():
    clipboard_data = get_clipboard_data()
    entry.delete(0, END)
    entry.insert(0, clipboard_data)

# Создание главного окна
root = Tk()
root.title("YouTube Video Downloader")

# Создание фрейма для ввода URL
url_frame = Frame(root)
url_frame.pack(pady=10)

# Создание текстового поля для ввода URL
entry = Entry(url_frame, width=40)
entry.grid(row=0, column=0, padx=5)

# Кнопка для вставки из буфера обмена
insert_from_clipboard_button = Button(url_frame, text="Вставить из буфера обмена", command=insert_from_clipboard)
insert_from_clipboard_button.grid(row=0, column=1, padx=5)

# Создание фрейма для кнопок "Скачать видео" и "Конвертировать в MP3"
button_frame = Frame(root)
button_frame.pack(pady=10)

# Кнопка для скачивания видео
download_button = Button(button_frame, text="Скачать видео", command=download_video)
download_button.grid(row=0, column=0, padx=5)

# Кнопка для конвертации в MP3
convert_button = Button(button_frame, text="Конвертировать в MP3", command=convert_to_mp3)
convert_button.grid(row=0, column=1, padx=5)

# Метка для вывода статуса
status_label = Label(root, text="")
status_label.pack(pady=10)

# Запуск главного цикла
root.mainloop()
