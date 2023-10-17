from flask import Flask, render_template, request, Response
from flask_assets import Bundle, Environment

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

num_buzzers = 6
buzzers = [False] * num_buzzers


@app.route('/')
def index():
    return render_template("index.html", buzzers=buzzers)


@app.route('/buzzer/<int:id>')
def buzzer(id):
    print(f"Pressed buzzer {id}")
    global buzzers
    buzzers[id - 1] = True
    return render_template("buzzer.html", id=id)


@app.route('/reset')
def reset():
    print(f"Resetting buzzers")
    global buzzers
    buzzers = [False] * num_buzzers

    return Response(headers={
        'HX-Refresh': 'true'
    })


if __name__ == "__main__":
    app.run(debug=True, port=3000)
