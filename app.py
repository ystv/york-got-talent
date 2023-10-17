from flask import Flask, render_template, request, Response
from flask_assets import Bundle, Environment

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

num_buzzers = 4
buzzers = [False] * num_buzzers


@app.route('/')
def index():
    return render_template("index.html", buzzers=buzzers)


@app.route('/buzzer/<int:id>')
def buzzer(id):
    print(f"Pressed buzzer {id}")
    global buzzers
    buzzers[id - 1] = True

    # Send OSC message to QLab to update the graphics

    return render_template("buzzer.html", id=id)


@app.route('/buzzers')
def buzzersRoute():
    global buzzers
    return render_template("buzzers.html", buzzers=buzzers)


@app.route('/reset')
def reset():
    print(f"Resetting buzzers")
    global buzzers
    buzzers = [False] * num_buzzers

    # Send OSC message to QLab telling it to reset the graphics

    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
