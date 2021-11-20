from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd04daf94f0fc0f6cbe6095797c18dc2c03d089fa'
Bootstrap(app)


@app.route('/')
def home():
    return "<h1>030</h1>"


if __name__ == "__main__":
    app.run(debug=True)
