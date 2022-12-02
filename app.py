import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
serverName = os.getenv("SERVER_NAME")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        print(response.choices[0].text)
        
        url = url_for("index", _external=True, result=response.choices[0].text)
        url = url.replace('localhost:5000', serverName)
        # url = url.replace('http', 'https')
        print(url)
        return redirect(url)

    result = request.args.get("result")
    print(f"Result is: {result}")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
