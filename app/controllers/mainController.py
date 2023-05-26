from flask import render_template, redirect, url_for

def index():
    return render_template('main/index.html')

def prediction():
    return render_template('main/predict.html')
