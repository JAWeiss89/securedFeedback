from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def get_root_route():
    return render_template('base.html')