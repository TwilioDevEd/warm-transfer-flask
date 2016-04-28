from . import app
from flask import render_template


@app.route('/')
def root():
    return render_template('index.html')
