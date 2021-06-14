from PIL import Image, ImageDraw, ImageFont

import matplotlib.colors
import matplotlib.font_manager


def assigning_colors():
    """Returns a dictionary with the corresponding RGB values of a color name"""
    rgb_colors = {}
    for name, hex in matplotlib.colors.cnames.items():
        color = []
        # So the values are from 0-255 and not 0-1
        for i in matplotlib.colors.to_rgb(hex):
            color.append(int(i * 255))

        color = tuple(color)
        rgb_colors[name] = color

    return rgb_colors


def assign_image(srcImage):
    try:
        original = Image.open(srcImage)
    except ValueError:
        raise Exception("Imagem não encontrada")

    return original


def draw_text(image, text, font, size, color, pos_name, shadow=False):
    """Returns an image with a text"""
    # Make a copy of the image
    image = image.copy()

    draw = ImageDraw.Draw(image)

    width, height = get_size(image)

    rgb_colors = assigning_colors()

    try:
        font_type = ImageFont.truetype(font, size)
    except ValueError:
        raise Exception("Fonte ou tamanho de fonte inválidos")

    w, h = draw.textsize(text, font=font_type)

    position = get_position(height, h, width, w, pos_name, shadow=shadow)

    if color in rgb_colors:
        color = rgb_colors[color]
    else:
        raise Exception("Cor inválida")

    draw.text(xy=position, text=text, fill=color,
              font=font_type, align=check_alignment(pos_name))

    return image


def possible_positions():
    # return ['Meio', 'Centro-Esquerda', 'Centro-Direita', 'Inferior-Esquerda', 'Inferior-Direita']
    return ['Middle', 'Center-Left', 'Center-Right', 'Bottom-Left', 'Bottom-Right',
            'Bottom-Center', 'Top-Left', 'Top-Center', 'Top-Right']


def check_alignment(name):
    """Retorns the text aligment according to the position"""
    translate_alignment = {
        'middle': 'center',
        'center-left': 'left',
        'center-right': 'right',
        'bottom-left': 'left',
        'bottom-right': 'right',
        'bottom-center': 'center',
    }

    if name in translate_alignment:
        return translate_alignment[name]
    else:
        return None


def get_position(height, h, width, w, pos, border=80, shadow=False):
    """Returns a position according to the dictionary 'places' or, if it's not there, returns the position itself"""
    extra = 2

    places = {
        'middle': (int((width - w) / 2) - extra * shadow, int((height - h) / 2) + extra * shadow),
        'center-left': (border - extra * shadow, int((height - h) / 2) + extra * shadow),
        'center-right': (width - w - border - extra * shadow, int((height - h) / 2) + extra * shadow),
        'bottom-left': (border - extra * shadow, height - border - h + extra * shadow),
        'bottom-right': (width - w - border - extra * shadow, height - border - h + extra * shadow),
        'bottom-center': (int((width - w) / 2) - extra * shadow, height - border - h + extra * shadow),
    }

    if pos in places:
        position = places[pos]
    else:
        position = pos

    return position


def get_size(image):
    """Returns the size of the image (width, height)"""
    width, height = image.size

    return (width, height)


def get_fonts():
    """Get the name of font families that are in the system"""
    fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
    fonts.append([f.name for f in matplotlib.font_manager.fontManager.afmlist])

    fonts = sorted(list(set(fonts[:-1])))

    return fonts


def get_font_path(family, font_format="normal"):
    """Returns the regular font path according to its family"""
    weight = "roman"
    weight = None
    if font_format == "bold":
        font_format = "normal"
        weight = "bold"
    font = matplotlib.font_manager.FontProperties(
        family=family, style=font_format, weight=weight)
    file = matplotlib.font_manager.findfont(font)
    return file
