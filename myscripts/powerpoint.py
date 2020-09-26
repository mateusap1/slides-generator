from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import ColorFormat, RGBColor
from pptx.enum.text import MSO_AUTO_SIZE

from get_lyrics import requestsScrape
from image import compress

import os
import time


# Currently the GUI doesn't have a powerpoint option because it would be really specific, but you can adapt yor program according to your needs.
# Atualmente a GUI não tem uma opção para escolher o modo "powerpoint" porque seria muito específico, mas você pode adaptar essa função às suas necessidades.
def main():
    data = [
        "Sei que Estás Aqui - Arena Louvor", 
        "Preciso de Ti - Quatro Por Um",
        "Te Agradeço - DK6",
        "Eu Corro Para Ti - Paulo César Baruk",
        "Senhor Te Quero - DK6",
        "Viverei pra Ti - Bereana Louvor Adoração"
    ]

    create_main(data[2].split(" - ")[1], data[2].split(" - ")[0], "Arial", 20)


def create_main(artist, music, font_name, size, color=RGBColor(255, 255, 255), stacks=2):
    start = time.time()

    letra = requestsScrape(artist, music)

    end = time.time()
    print(end - start, "API")
    print(letra)

    prs, layout = init_slides()

    start = time.time()

    prs = get_title(prs, layout, artist, music)

    count = 1
    for estrofe in letra:
        for n in range(0, len(estrofe), stacks):
            # cons = stacks
            if n < len(estrofe) - (stacks - 1):
                text = "\n".join([estrofe[i] for i in range(n, n+stacks)])
            else:
                last = len(estrofe)
                text = "\n".join([estrofe[i] for i in range(n, last)])
                # cons = last - n

            # simplify.draw_text(image=image, text=text, font="arial", size=font_size, color="white", position=pos).save(f"{file_dir}/{count}.png")
            prs = create_pwp(prs, layout, text.upper(), font_name, size, color)

            count += 1
    
    end = time.time()
    print(end - start, "PowerPoint")

    name = f"{music} - {artist}.pptx"
    save(name, prs)

    path = os.getcwd().replace("\\", "/")

    files = os.listdir(path)
    file_dir = f"{path}/{name[:-5]}"
    print(file_dir)

    if name + ".pptx" in files:
        os.remove(name + ".pptx")

    # compress(file_dir, name)

    return file_dir


def get_title(prs, layout, artist, music, font_name="Arial"):
    prs = create_pwp(prs, layout, artist, font_name, 32, RGBColor(255, 255, 255))

    cons = 7.5 - 1 - 40 * .016 * (1 + 1)

    slide = prs.slides[-1]

    left = Inches(1)
    top = Inches(cons)
    width = Inches(9)
    height = Inches(.4)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.paragraphs[0]

    run = p.add_run()
    run.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    # run.vertical_anchor = MSO_ANCHOR.BOTTOM
    run.text = music

    font = run.font
    font.name = font_name
    font.size = Pt(40)
    font.color.rgb = RGBColor(255, 255, 255)

    return prs


def init_slides():
    INDEX = 6
    prs = Presentation()

    # 13.333
    prs.slide_width = Inches(13.333)
    # 7.5
    prs.slide_height = Inches(7.5)

    # O index representa o tipo de layout que vamos usar
    layout = prs.slide_layouts[INDEX]

    return prs, layout


def create_pwp(prs, layout, text, font_name, size, color=RGBColor(255, 255, 255)):
    """
    Cria Slides no Power Point de acordo com os inputs
    """
    times = count_chars(text, "\n")
    cons = 7.5 - 1 - size * .016 * (times + 1)
    
    slide = prs.slides.add_slide(layout)

    background = slide.background

    # Isso coloca a cor de fundo como azul escuro
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(32, 56, 100)

    left = Inches(1)
    # Adapta a distância do topo ao tamanho do texto
    top = Inches(cons)
    width = Inches(9)
    height = Inches(.2 + .13 * times + .2 * (times+1))

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.paragraphs[0]

    run = p.add_run()
    run.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    # run.vertical_anchor = MSO_ANCHOR.BOTTOM
    run.text = text

    font = run.font
    font.name = font_name
    font.size = Pt(size)
    font.color.rgb = RGBColor(255, 255, 255)

    imgLeft = Inches(.8)
    imgTop = Inches(.65)
    imgWidth = Inches(1)
    imgHeight = Inches(.838)
    # imgHeight = Inches(imgWidth * .838)

    img_path = "images/Logo da Juventude.png"
    slide.shapes.add_picture(img_path, imgLeft, imgTop, imgWidth, imgHeight)

    imgLeft = Inches(13.333 - 2.7)
    imgTop = Inches(.65)
    imgWidth = Inches(1 * 1.7)
    imgHeight = Inches(.512 * 1.7)
    # imgHeight = Inches(imgWidth * .838)

    img_path = "images/Logo JMTV.png"
    slide.shapes.add_picture(img_path, imgLeft, imgTop, imgWidth, imgHeight)

    return prs


def save(name, prs):
    prs.save(name)
    # Open the file on the operating system
    # os.startfile(name)


def count_chars(string, char):
    counter = 0
    c = len(char)
    for i in range(0, len(string) - c, c):
        if string[i:i+c] == char:
            counter += 1
    
    return counter


if __name__ == "__main__":
    main()
