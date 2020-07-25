from tkinter import filedialog
from tkinter import Tk, Frame, Label, Entry, Button, X, Y, LEFT, RIGHT, BOTTOM, TOP, StringVar, Menu, Text, Scrollbar, PhotoImage
from tkinter.ttk import Combobox, Style

from image import create_slides
from simplify import get_fonts, possible_positions, get_font_path
from translation import get_dictionaries

import time
import os


class Translate(Exception):
    pass


def main():
    # The default language of the program
    global lng
    lng = "Portuguese"

    spaces = 2

    global elements
    elements = []

    main_color = "#1C1C1C"
    color2 = "#363636"

    global window
    window = Tk()
    window.title("Slides Generator")

    window.geometry("750x450+710+270")
    window.configure(background=main_color)

    menubar = Menu(window)

    languagebar = Menu(menubar, tearoff=0)
    languagebar.add_command(label="Português", command = lambda *args: change_language("Portuguese"))
    languagebar.add_command(label="English", command = lambda *args: change_language("English"))

    languagebar.add_separator()

    menubar.add_cascade(label="Language", menu=languagebar)

    window.config(menu=menubar)

    # Creates a label placed on the top of the program with an empty string as default text
    global error_message
    error_message = Label(window, text="", font=("Sans-Serif", 10, "bold"), fg="red")
    error_message.pack(side = TOP, pady=10)
    error_message.configure(background=main_color)

    elements.append(error_message)

    artist_frame = Frame(window) 
    artist_frame.pack(fill = X, padx=10, pady=10) 
    artist_frame.rowconfigure(0, weight=1)
    artist_frame.configure(background=main_color)

    # This spaces are used so the elements will be aligned. It's not a good code (in fact it's a pretty bad one), but it works
    artist_lbl = Label(artist_frame, text=translate_language("Artista" + " " * (spaces + 16), lng), font=("Sans-Serif", 10, "bold"), fg="white")
    artist_lbl.pack(side = LEFT)
    artist_lbl.configure(background=main_color)
    elements.append(artist_lbl)

    global artist
    artist = Entry(artist_frame, font=("Sans-Serif", 10, "bold"), relief="ridge", fg="white")
    artist.pack(side = LEFT, fill = X, expand=True)
    artist.configure(background=color2)

    music_frame = Frame(window)
    music_frame.pack(fill = X, padx=10, pady=10)
    music_frame.configure(background=main_color)
    
    music_lbl = Label(music_frame, text=translate_language("Música" + " " * (spaces + 15), lng), font=("Sans-Serif", 10, "bold"), fg="white")
    music_lbl.pack(side = LEFT)
    music_lbl.configure(background=main_color)
    elements.append(music_lbl)

    global music
    music = Entry(music_frame, font=("Sans-Serif", 10, "bold"), relief="ridge", fg="white")
    music.pack(side = LEFT, fill = X, expand=True)
    music.configure(background=color2)

    settings = {
        'TCombobox': {
            'configure': {
                'selectbackground': "#1E90FF",
                'fieldbackground': color2,
                'foreground': "white",
                'relief': "ridge"
            }
        }
    }

    combostyle = Style()
    combostyle.theme_create('combostyle', parent='alt', settings = settings)
    combostyle.theme_use('combostyle')

    stacks_frame = Frame(window)
    stacks_frame.pack(fill = X, padx=10, pady=10)
    stacks_frame.configure(background=main_color)

    stacks_label = Label(stacks_frame, text=translate_language("Versos p/ slide" + " " * (spaces + 3), lng), font=("Sans-Serif", 10, "bold"), fg="white")
    stacks_label.pack(side = LEFT)
    stacks_label.configure(background=main_color)
    elements.append(stacks_label)

    global stacks
    stacks = Combobox(stacks_frame, width = 3, font=("Sans-Serif", 10, "bold"))
    stacks["values"] = [i for i in range(1, 9)]
    stacks.current(1)
    stacks.pack(side = LEFT, fill=X, expand=True)

    position_label = Label(stacks_frame, text= translate_language(" " * spaces + "Posição" + " " * spaces, lng), font=("Sans-Serif", 10, "bold"), fg="white")
    position_label.pack(side = LEFT)
    position_label.configure(background=main_color)
    elements.append(position_label)

    global position
    position = Combobox(stacks_frame, width = 11, font=("Sans-Serif", 10, "bold"))
    position["values"] = possible_positions()
    position.current(3)
    position.pack(side = RIGHT, fill=X, expand=True)

    font_frame = Frame(window)
    font_frame.pack(fill = X, padx=10, pady=10)
    font_frame.rowconfigure(0, weight=1)
    font_frame.configure(background=main_color)

    font_lbl = Label(font_frame, text=translate_language("Fonte" + " " * (spaces + 17), lng), font=("Sans-Serif", 10, "bold"), fg="white")
    font_lbl.configure(background=main_color)
    font_lbl.pack(side = LEFT)
    elements.append(font_lbl)

    global fonts
    font_names = get_fonts()
    fonts = Combobox(font_frame, width=10, font=("Sans-Serif", 10, "bold"))
    fonts["values"] = font_names
    fonts.current(font_names.index("Arial"))
    fonts.pack(side = LEFT, fill = X, expand = True)

    global size
    size = Combobox(font_frame, width = 11, font=("Sans-Serif", 10, "bold"))
    size["values"] = [8, 9, 10, 11, 12, 14, 18, 24, 30, 36, 48, 60, 72, 96]
    size.current(8)
    size.pack(side = RIGHT, fill=X, expand=True)

    size_lbl = Label(font_frame, text=translate_language(" " * spaces + "Tamanho" + " " * spaces, lng), font=("Sans-Serif", 10, "bold"), fg="white")
    size_lbl.configure(background=main_color)
    size_lbl.pack(side = RIGHT)
    elements.append(size_lbl)

    path_frame = Frame(window)
    path_frame.pack(fill = X, padx=10, pady=10)
    path_frame.rowconfigure(0, weight=1)
    path_frame.configure(background=main_color)

    path_lbl = Label(path_frame, text=translate_language("Imagem Base" + " " * (spaces + 5), lng), font=("Sans-Serif", 10, "bold"), fg="white")
    path_lbl.configure(background=main_color)
    path_lbl.pack(side = LEFT)
    elements.append(path_lbl)

    global path
    path = Entry(path_frame, font=("Sans-Serif", 10, "bold"), relief="ridge", fg="white")
    path.insert(0, fr"{get_desktop_path()}\exempleimg.png")
    path.pack(side = LEFT, fill = X, expand=True)
    path.configure(background=color2)

    path_btn = Button(path_frame, text=translate_language("Selecionar", lng), font=("Sans-Serif", 8, "bold"), command=get_directory, bg=color2, fg="white", height = 1)
    path_btn.pack(side = RIGHT, padx=10)
    elements.append(path_btn)

    lyrics_frame = Frame(window)
    lyrics_frame.pack(fill = X, padx=10, pady=10)
    lyrics_frame.rowconfigure(0, weight=1)
    lyrics_frame.configure(background=main_color)

    lyrics_lbl = Label(lyrics_frame, text=translate_language("Letra (opcional)" + " " * (spaces + 2), lng), font=("Sans-Serif", 10, "bold"), fg="white")
    lyrics_lbl.configure(background=main_color)
    lyrics_lbl.pack(side = LEFT)
    elements.append(lyrics_lbl)

    global lyrics
    lyrics = Text(lyrics_frame, height=6, font=("Sans-Serif", 10, "bold"), relief="ridge", fg="white")
    lyrics.pack(side = LEFT, fill = X, expand=True)
    lyrics.configure(background=color2)

    scroller = Scrollbar(lyrics_frame, command=lyrics.yview)
    scroller.pack(side = RIGHT, fill = Y, expand = True)

    lyrics['yscrollcommand'] = scroller.set

    btn = Button(window, text=translate_language("Gerar slides", lng), font=("Sans-Serif", 10, "bold"), command=generate, bg=color2, fg="white")
    btn.pack(padx=10, pady=10)
    elements.append(btn)

    window.mainloop()


def change_language(lang):
    global lng
    lng = lang

    for element in elements:
        element["text"] = translate_language(element["text"], lng)


def get_directory():
    filename =  filedialog.askopenfilename(initialdir = get_desktop_path(), title = "Imagem de Fundo", filetypes = (("png files","*.png"),("all files","*.*")))
    path.delete("0", "end")
    path.insert(0, filename)


def generate():
    directory =  f"{filedialog.askdirectory(initialdir = get_desktop_path(), title = 'Save as')}/"

    # Check if the path is valid
    # Checar se o diretório é válido
    if directory == "/" or not os.path.isdir(directory):
        display_error(translate_language("Caminho Inválido!", lng))
        return

    artist_name = artist.get()
    music_name = music.get()

    # Check if the artist and music names are not empty
    # Checar se artista e música não estão em branco
    if not len(artist_name) > 0 or not len(music_name) > 0:
        display_error(translate_language("Nome do artista ou da música inválido!", lng))
        return

    # "Stk" is the same as "verses per slide"
    # "Stk" é o mesmo que "versos por slide"
    stk = stacks.get()

    # Check if the verses per slide aree integers from 1 to 8.
    # Checar se stacks são números inteiros de 1 a 8.
    if not stk.isdigit() or int(stk) < 1 or int(stk) > 8:
        display_error(translate_language("Os versos por slide devem ser um número de 1 a 8!", lng))
        return

    stk = int(stk)

    pos = position.get().lower()

    # Check if the position is one of the possible positions
    # Checar se a posição está entre as posições existentes
    if not pos in [string.lower() for string in possible_positions()]:
        display_error(translate_language("Posição Inexistente!", lng))
        return

    font = fonts.get()

    # Check if the font name is one of the possible names
    # Checar se a fonte está entre as fontes existentes
    if not font in get_fonts():
        display_error(translate_language("Fonte não encontrada!", lng))
        return
    
    font = get_font_path(font)
    print("Fonte:", font)

    font_size = size.get()

    # Check if the size is a number greater then zero and if it's not an integer, transforms it.
    # Verificar se o tamanho é um número maior que 0 e transformá-lo em inteiro (caso não seja)
    if not font_size.isdigit() or int(font_size) < 8 or int(font_size) > 100:
        display_error(translate_language("Tamanho da fonte deve ser um número de 8 a 100!", lng))
        return

    font_size = int(font_size)

    src = path.get()

    # Check if it's a valid image
    # Checar se a imagem existe
    if not os.path.isfile(src):
        display_error(translate_language("Imagem não encontrada!", lng))
        return

    color = "white"

    text = lyrics.get("1.0", "end")

    start = time.time()

    # Removes any "\n" that the user may have writen by accident
    if text.replace("\n", "") == "":
        text = None
    
    slides = create_slides(src, artist_name, music_name, font, font_size, color, pos, stk, directory, 80, text)

    print("Time:", time.time() - start)

    if not slides: # If the lyrics weren't found, displays an error message
        display_error(translate_language("A letra dessa música não foi encontrada. Tente digitar a letra manualmente na aba 'texts'.", lng))


def translate_language(text, language):
    english, portuguese = get_dictionaries()

    if language == "Portuguese" and text in english:
        return english[text]
    elif language == "Portuguese" and text in portuguese:
        return text
    elif language == "English" and text in portuguese:
        return portuguese[text]
    elif language == "English" and text in english:
        return text
    else:
        return ""


def display_error(error):
    print(error)
    error_message["text"] = error
    return


def get_desktop_path():
    """Returns the default downloads path for linux or windows"""
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


if __name__ == "__main__":
    main()