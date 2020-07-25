import requests

from requests_html import HTMLSession
from bs4 import BeautifulSoup

import re

from time import sleep, time

from unicodedata import normalize


def requestsScrape(artist, music):
    """Gets the lyrics from cifraclub according to the artist and music names"""

    # Basically changes the name in a way that the website will understand
    artist = stress_remove(artist).lower().replace(" ", "-")
    music = stress_remove(music).lower().split(" ")
    music = list(filter(lambda i: i != "e", music))
    music = "-".join(music)

    url = f"https://www.cifraclub.com.br/{artist}/{music}/letra/"
    
    # Get the lyrics from the website
    letra = pure_letra(url)

    # If it didn't find anything, use the search_in_google function to find the correct url and filters it
    if len(letra) == 0:
        letra = pure_letra(f"{search_in_google(artist, music)}/letra")

        if len(letra) == 0:
            return None
    
    result = filter_letra(letra)
    
    return result


def pure_letra(url):
    """Goes to the url and try to find the lyrics. If it wasn't the right website returns an empty list"""
    start = time()
    
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
        lyrics = response.html.xpath('//div[@class="letra"]/div[@class="letra-l"]/p')

    print(time() - start, "-> Get the lyrics from the website")
    return lyrics


# Filtra a letra em um formato mais fácil para usar depois
def filter_letra(link):
    """Filters the lyrics, so it's easier to manipulate it"""
    start = time()

    # Basically splits the strophes in verses. *Is 'strophes' really a word? I mean 'group of verses'.
    # Basicamente divide as estrofes em versos
    if hasattr(link[0], 'text'):
        result = [i.text.split("\n") for i in link]
    else:
        result = [i.split("\n") for i in link]

    # If it has the format of "(x3)" or "(x4)" it will repeat the strophe N times according to "(xN)"
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
    
    print(time() - start, "-> Filtrar a Letra")
    return result


# Faz uma pesquisa no google e retorna o link do cifraclub
def search_in_google(artist, music):
    """Makes a google search and returns the cifraclub link"""
    start = time()

    url = f"https://www.google.com/search?q={music} {artist} cifra club"
    try:
        session = HTMLSession()
        response = session.get(url)   
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
    link = response.html.xpath('//div[@class="r"]/a/@href')

    print(time() - start, "-> Pesquisar no Google")
    
    print(link[0])
    # I think it's pretty clear what this does
    if "https://www.cifraclub" not in link[0]:
        return None
    else:
        return link[0]


# Divide a letra em versos e estrofes
def divide_by_text(text):
    """Divides the lyrics in verses and strophes"""
    while text[-1] == "\n":
        text = text[:-1]

    # If there is anything between parenthesis, remove it.
    regex = re.escape("(") + r".+\S" + re.escape(")") + "\n"
    text = re.sub(regex, "", text)

    # Divide in strophes
    # Divide em estrofes
    text = text.split("\n\n")

    text = [re.sub(regex, "", i) for i in text]

    return filter_letra(text)


# https://wiki.python.org.br/RemovedorDeAcentos
# I really need this stress_remove for my life
def stress_remove(txt, codif='utf-8'):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')