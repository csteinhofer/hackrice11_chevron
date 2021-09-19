# main.py
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello World'

@app.route('/submit')
def submit():
    return render_template('submit.html')

if __name__ == '__main__':
    app.run()
