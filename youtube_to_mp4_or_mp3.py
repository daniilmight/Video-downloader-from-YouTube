from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QComboBox, QHBoxLayout
from pytube import YouTube
import os
from moviepy.editor import AudioFileClip

class YoutubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")

        self.init_ui()

    def init_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout(self)

        # Создание фрейма для ввода URL и выбора качества
        url_quality_frame = QFrame(self)
        layout.addWidget(url_quality_frame)

        # Создание горизонтального макета для ввода URL и выбора качества
        url_quality_layout = QHBoxLayout(url_quality_frame)

        # Создание текстового поля для ввода URL
        self.entry = QLineEdit(self)
        url_quality_layout.addWidget(self.entry)

        # Кнопка для вставки из буфера обмена
        insert_from_clipboard_button = QPushButton("Вставить из буфера обмена", self)
        insert_from_clipboard_button.clicked.connect(self.insert_from_clipboard)
        url_quality_layout.addWidget(insert_from_clipboard_button)

        # Выпадающий список для выбора качества видео
        self.quality_combo = QComboBox(self)
        self.quality_combo.addItem("Выберите качество")
        url_quality_layout.addWidget(self.quality_combo)

        # Создание фрейма для кнопок "Скачать видео" и "Конвертировать в MP3"
        button_frame = QFrame(self)
        layout.addWidget(button_frame)

        # Кнопка для скачивания видео
        download_button = QPushButton("Скачать видео", self)
        download_button.clicked.connect(self.download_video)

        # Кнопка для конвертации в MP3
        convert_button = QPushButton("Конвертировать в MP3", self)
        convert_button.clicked.connect(self.convert_to_mp3)

        button_frame_layout = QHBoxLayout(button_frame)
        button_frame_layout.addWidget(download_button)
        button_frame_layout.addWidget(convert_button)

        # Метка для вывода статуса
        self.status_label = QLabel(self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Применение стилей
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: #333;
                font-size: 14px;
            }

            QPushButton {
                background-color: #009B77;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #00664E;
            }

            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 14px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)

    def get_clipboard_data(self):
        clipboard = QApplication.clipboard()
        return clipboard.text()

    def insert_from_clipboard(self):
        clipboard_data = self.get_clipboard_data()
        self.entry.setText(clipboard_data)

    def download_video(self):
        url = self.entry.text()
        if not url:
            clipboard_data = self.get_clipboard_data()
            self.entry.setText(clipboard_data)
            url = self.entry.text()

        if url and self.quality_combo.currentIndex() > 0:
            yt = YouTube(url)
            selected_quality = self.quality_combo.currentText()
            video_stream = yt.streams.filter(res=selected_quality).first()
            video_stream.download(output_path=os.path.expanduser('~/Downloads'), filename='temp.mp4')
            self.status_label.setText("Видео успешно скачано!")
        else:
            self.status_label.setText("Пожалуйста, введите URL и выберите качество")

    def convert_to_mp3(self):
        video = os.path.expanduser('~/Downloads/temp.mp4')
        audio = os.path.expanduser('~/Downloads/temp.mp3')
        file = AudioFileClip(video)
        file.write_audiofile(audio)
        file.close()
        self.status_label.setText("Конвертация завершена!")

if __name__ == "__main__":
    app = QApplication([])
    window = YoutubeDownloaderApp()

    # Заполнение выпадающего списка качества видео
    quality_options = ["360p", "720p"]
    window.quality_combo.addItems(quality_options)

    window.show()
    app.exec_()
