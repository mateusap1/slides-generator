import os
import simplify
import tarfile
import shutil

from get_lyrics import requestsScrape, divide_by_text


def create_slides(src, artist, music, font, font_size, color, position, stacks=2, directory="./slides/", border=20, text=None):
    """Creates slides accroding to the name of the artist and music or according to a text"""

    # If the user writes any text, this function will use it. Otherwise, it will get the lyrics using the 'webscraping' function
    # Se o usuário colocou algum texto, o programa vai usar esse texto. Caso contrário, pega a letra através de 'webscraping'
    if not text:
        letra = requestsScrape(artist, music)
    else:
        letra = divide_by_text(text)

    # If it could not find the lyrics, return None
    # Se não houver letra, retorna None
    if not letra or len(letra) == 0:
        return None

    name = f"{music} ({artist}) - Slides"
    file_dir = f"{directory}{name}"

    # Get all the folders in the path selected by the user, so we can delete any folder that has this same name
    # Pega todas as pastas no caminho que o usuário escolheu para que o programa delete qualquer pasta com o mesmo nome da pasta que pretendemos criar
    files = os.listdir(directory)

    # If there is a folder with the same name, delete it
    # Se já há uma pasta com os mesmos slides, deleta ela
    if name in files:
        shutil.rmtree(f"{file_dir}")

    os.mkdir(file_dir)

    # Create an image object (using Pillow) according to the path the user gave us
    # Cria um objeto de imagem de acordo com o background do usuário
    image = simplify.assign_image(src)
    height = image.size[1]

    # The font_size of the music title is 2 times the lyrics normal size. That's just a style option, you can change that number.
    # O tamanho da fonte do título da música é o dobro do tamanho da fonte da letra. Isso é questão de estilo, você pode mudar.
    music_size = int(2 * font_size)
    artist_size = int(1.6 * font_size)

    # Just adjusting the position of the Music title and artist name to be in the bottom-left corner.
    pos = (border, height - border - (music_size + artist_size + 10))
    image = simplify.draw_text(image=image, text=music, font=font, size=music_size, color="white", pos_name=pos)

    pos = (border, height - border - (artist_size))
    simplify.draw_text(image=image, text=artist, font=font, size=artist_size, color="white", pos_name=pos).save(f"{file_dir}/0.png")

    image = simplify.assign_image(src)

    count = 1
    for estrofe in letra:
        for n in range(0, len(estrofe), stacks):
            # Adjust the lyric verses to the number of verses per slide(I am calling it 'stacks')
            if n < len(estrofe) - (stacks - 1):
                text = "\n".join([estrofe[i] for i in range(n, n+stacks)])
            else:
                last = len(estrofe)
                text = "\n".join([estrofe[i] for i in range(n, last)])

            simplify.draw_text(image=image, text=text.upper(), font=font, size=font_size, color="white", pos_name=position).save(f"{file_dir}/{count}.png")

            count += 1
    
    return file_dir


def compress(path, name):
    """Compress a folder into a .tgz file"""
    # Currently I am not using it, but if sometime I want to make this a Flask application I will need that function
    print(path, name)
    tar = tarfile.open(f"{path}.tgz", "w:gz")
    tar.add(path, arcname=name)
    tar.close()