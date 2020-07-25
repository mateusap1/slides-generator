def get_dictionaries():
    spaces = 2

    # I know, this spaces are pretty ugly, but I haven't found any better option.
    portuguese = {
        "Letra (opcional)" + " " * (spaces + 2): "Lyrics (optional)" + " " * (spaces + 2),
        "Artista" + " " * (spaces + 16): "Artist" + " " * (spaces + 20),
        "Música" + " " * (spaces + 15): "Music" + " " * (spaces + 19),
        "Versos p/ slide" + " " * (spaces + 3): "Verses p/ slide" + " " * (spaces + 5),
        " " * spaces + "Posição" + " " * spaces: " " * spaces + "Position" + " " * spaces,
        "Fonte" + " " * (spaces + 17): "Font" + " " * (spaces + 21),
        " " * (spaces) + "Tamanho" + " " * (spaces): " " * (spaces) + "Size" + " " * (spaces),
        "Imagem Base" + " " * (spaces + 5): "Base Image" + " " * (spaces + 9),
        "Selecionar": "Select",
        "Gerar slides": "Generate",
        "Caminho Inválido!": "Invalid Path!",
        "Nome do artista ou da música inválido!": "Artist or music name not found!",
        "Os versos por slide devem ser um número de 1 a 8!": "Verses per slide must be one number from 1 to 8!",
        "Posição Inexistente!": "Invalid Position",
        "Fonte não encontrada!": "Font name not found!",
        "Tamanho da fonte deve ser um número de 8 a 100!": "Font size must be a number from 8 to 100",
        "Imagem não encontrada!": "Image not found!",
        "A letra dessa música não foi encontrada. Tente digitar a letra manualmente na aba 'texts'.": "The lyrics weren't found. Try typing them manually.",
    }

    english = {}

    # Populate english dictionary with the reverse of the portuguese dictionary
    for i in portuguese:
        english[portuguese[i]] = i
    
    return english, portuguese