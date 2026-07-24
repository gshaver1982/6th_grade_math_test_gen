# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:08:24 2026

@author: Garrett
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Math Test Generator</h1>"

if __name__ == "__main__":
    app.run(debug=True)