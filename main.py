from flask import Flask, render_template
from matematica.bhaskara import bhaskaraView
from matematica.trigonometria import trigonometriaView
from matematica.pitagoras import pitagorasView


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Rota para a calculadora de Bhaskara
app.add_url_rule('/bhaskara', view_func = bhaskaraView, methods = ['GET', 'POST'])

# Rota para a calculadora de Trigonometria
app.add_url_rule('/trigonometria', view_func = trigonometriaView, methods = ['GET', 'POST'])

# Rota para a calculadora de Pitágoras
app.add_url_rule('/pitagoras', view_func = pitagorasView, methods = ['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug = True)