from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "ABC"


@app.route('/')
def index():
    """Homepage"""

    return render_template('test.html')



if __name__ == "__main__":

    app.debug = True
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
