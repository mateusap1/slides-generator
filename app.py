from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, send_file

from pptx import Presentation

import os
import sys
import tarfile
import shutil
import json

from threading import Event, Thread

from slide import Slide
import simplify
import get_lyrics

UPLOAD_FOLDER = './uploads/'
SLIDES_FOLDER = './slides/'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        fonts = simplify.get_fonts()
        return render_template("/index.html", font_names=fonts, positions=simplify.possible_positions(),
                              formats=["Normal", "Bold", "Italic", "Shadow"])
    elif request.method == "POST":
        output_format = request.form.get("pwp-or-img")

        music = request.form.get("music")
        artist = request.form.get("artist")

        font_name = request.form.get("font-names")
        font_size = int(request.form.get("font-sizes"))

        stacks = int(request.form.get("stacks"))
        position = request.form.get("positions").lower().replace("-", "_")

        border = int(request.form.get("border"))
        text_format = request.form.get("format")

        f = request.files['background-path']
        filename = UPLOAD_FOLDER + f.filename
        f.save(filename)

        if simplify.get_size(simplify.assign_image(filename))[1] < (font_size * stacks * 1.2 + border * 2):
            font_size = int((simplify.get_size(simplify.assign_image(filename))[1] - border * 2) / (stacks * 1.2))

        lyrics = session['lyrics']

        if type(lyrics) is dict:
            return redirect(request.url)
        
        key = os.urandom(24).hex()

        sprs = Slide(filename)
        sprs.width, sprs.height = simplify.get_size(simplify.assign_image(filename))
        sprs.font_type.set_family(font_name)
        sprs.font_type.set_size(font_size)
        if text_format and "Shadow" in text_format:
            sprs.shadow = True
        elif text_format:
            sprs.font_type.set_text_format(text_format.lower())
        sprs.border = border
        sprs.extra = 6 * font_size / 72
        sprs.stacks = stacks
        sprs.position = position
        sprs.directory = SLIDES_FOLDER + key

        if output_format == "pwp":
            sprs.prs = Presentation()
            sprs.create_slideshow(lyrics)
            sprs.prs.save(sprs.directory + ".pptx")
            
            file_to_be_sent = send_file(sprs.directory + ".pptx", as_attachment=True, attachment_filename="Slides.pptx")

            os.remove(filename)
            os.remove(sprs.directory + ".pptx")

            return file_to_be_sent
        else:
            sprs.create_imageshow(lyrics)
            compress(sprs.directory, "Slide")

            file_to_be_sent = send_file(sprs.directory + ".tgz", as_attachment=True, attachment_filename="Slides.tgz")

            os.remove(filename)
            os.remove(sprs.directory + ".tgz")
            os.rmdir(sprs.directory)

            return file_to_be_sent


@app.route("/validate/", methods=["POST"])
def validate():
    music = request.form.get("music")
    artist = request.form.get("artist")
    lyrics = request.form.get("lyrics")

    if lyrics.replace(" ", "").replace("\n", "") == "":
        lyrics = get_lyrics.requestsScrape(artist, music)
    else:
        lyrics = get_lyrics.divide_by_text(lyrics)

    if not lyrics:
        return jsonify("Lyrics not found. If you can't find any typos, consider typing the lyrics manually."), 406

    if type(lyrics) is dict:
        music = lyrics['Music']
        artist = lyrics['Artist']
        return jsonify(f'Did you mean \"{music}\" by \"{artist}\"?'), 406
    
    session['lyrics'] = lyrics
    return jsonify("OK"), 200


def compress(path, name):
    """Compress a folder into a .tgz file"""
    # Currently I am not using it, but if sometime I want to make this a Flask application I will need that function
    print(path, name)
    tar = tarfile.open(f"{path}.tgz", "w:gz")
    tar.add(path, arcname=name)
    tar.close()


if __name__ == "__main__":
    app.run()