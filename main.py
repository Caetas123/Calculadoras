import math
from flask import Flask, render_template, request

app = Flask(__name__)

# Função que resolve a equação quadrática
def bhaskara(a, b, c):
    # Calculando o discriminante (delta)
    delta = b**2 - 4*a*c
    
    if delta < 0:
        return f"Não existem raízes reais. Delta: {delta}"
    else:
        raiz1 = (-b + math.sqrt(delta)) / (2 * a)
        raiz2 = (-b - math.sqrt(delta)) / (2 * a)
    
    return raiz1, raiz2, delta

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None  
    if request.method == 'POST':
        try:
            # Pegando os valores de a, b e c
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])

            # Calculando as raízes
            resultados = bhaskara(a, b, c)

            # Se as raízes são válidas, passamos para o template
            if isinstance(resultados, tuple):  # Se for uma tupla, existem raízes reais
                raiz1, raiz2, delta = resultados
                return render_template('index.html', raiz1=raiz1, raiz2=raiz2, delta=delta)
            else:  # Se for uma string, é uma mensagem de erro
                error = resultados  # Atribuindo a mensagem de erro à variável `error`
        except ValueError:
            error = "Por favor, insira valores válidos."  # Mensagem de erro se houver ValueError

    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)