import requests
import re

from requests_html import HTMLSession
from unicodedata import normalize


def requestsScrape(original_artist, original_music):
    """Gets the lyrics from cifraclub according to the artist and music names"""

    url = search_in_google(original_artist, original_music)

    if not url:
        return None
    else:
        title = get_music_title(url)

    if not title:
        return None
    else:
        music, artist = title

    if original_artist.lower() == artist.lower() and original_music.lower() == music.lower():
        letra = pure_letra(f"{url}/letra")
    else:
        return {"Music": music, "Artist": artist, "Url": url}

    result = filter_letra(letra)

    return result


def pure_letra(url):
    """Goes to the url and try to find the lyrics. If it wasn't the right website returns an empty list"""
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return []

    if response.status_code != 200:
        return []

    # It gets the lyrics
    lyrics = response.html.xpath('//div[@class="letra"]/p')
    if len(lyrics) == 0:
        lyrics = response.html.xpath(
            '//div[@class="letra"]/div[@class="letra-l"]/p')

    return lyrics


# Filtra a letra em um formato mais fácil para usar depois
def filter_letra(link):
    """Filters the lyrics, so it's easier to manipulate it"""
    # Basicamente divide as estrofes em versos
    if hasattr(link[0], 'text'):
        result = [i.text.split("\n") for i in link]
    else:
        result = [i.split("\n") for i in link]

    # Se tem o formato "(x3)" ou "(x4)", repete a estrofe N vezes de acordo com "(xN)"
    regex = re.escape("(") + r"x\d" + re.escape(")")

    for i, estrofe in enumerate(result):
        for j, verso in enumerate(estrofe):
            # Em por enquanto só repete duas vezes independente do número, preciso mudar isso
            searched = re.search(regex, verso)
            if searched is not None:
                result[i][j] = re.sub(regex, "", verso)

                # Repete a estrofe n vezes. 'n' é o número depois do parêntese e do 'x'
                for _ in range(int(searched.group()[2]) - 1):
                    result.insert(i+1, result[i])
                    if result[i][j] == "":
                        result[i].pop(j)

    return result


# Faz uma pesquisa no google e retorna o link do cifraclub
def search_in_google(artist, music):
    """Makes a google search and returns the cifraclub link"""
    url = f"https://www.google.com/search?q={music} {artist} cifra club"
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    link = response.html.xpath('//div[@class="yuRUbf"]/a/@href')

    if not link or "https://www.cifraclub" not in link[0]:
        print(f"Failed to find {music} lyrics!")
        return None
    else:
        return link[0]


def get_music_title(url):
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    music_el = response.html.xpath('//h1[@class="t1"]')
    artist_el = response.html.xpath('//h2[@class="t3"]')

    if not music_el or not artist_el:
        return None
    else:
        music = music_el[0].text
        artist = artist_el[0].text

    return music, artist


# Divide a letra em versos e estrofes
def divide_by_text(text):
    """Divides the lyrics in verses and strophes"""
    text = text.replace("\r", "")

    while text[-1] == "\n":
        text = text[:-1]

    regex = re.escape("(") + r".+\S" + re.escape(")") + "\n"
    text = re.sub(regex, "", text)

    # Divide em estrofes
    text = text.split("\n\n")

    text = [re.sub(regex, "", i) for i in text]

    letra = filter_letra(text)

    letra = filter(lambda x: len(x) > 0 and not "" in x, letra)

    return list(letra)


# https://wiki.python.org.br/RemovedorDeAcentos
def stress_remove(txt, codif='utf-8'):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
