import PySimpleGUI
from PySimpleGUI import Window, Text, Radio, set_options, Button

set_options(font=("Arial Bold", 14))

# Layouts
format_text = Text("Music format: ")
default_radio = Radio("MP3", "format", default=True)
flex_format_radio = Radio("All types (mp3, wav, flac...)", "format")

format_layout = [[format_text], [default_radio], [flex_format_radio]]

start_button = Button("Start Download")

layout = [[format_layout], [start_button]]

window = Window(title="MSR Downloader", layout=layout, margins=(300, 100))

if __name__ == '__main__':
    window.read()
