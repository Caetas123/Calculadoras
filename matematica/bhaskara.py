from funcoesMatematicas import bhaskara
from flask import render_template, request

def bhaskaraView():
    error = None    
    if request.method == 'POST':
        try:
        # Pegando os valores do formulário HTML diretamente e convertendo para float
        # request.form['a'] acessa o valor do input
        # Se o campo estiver vazio ou não existir, vai dar erro
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])

            if a == 0:
                error = 'O termo "A" não pode ser 0, pois vira uma equação linear.'
                return render_template('bhaskara.html', error = error)

            raiz1, raiz2, delta, possuiRaizes = bhaskara(a, b, c)

            if not possuiRaizes:
                error = "Não existem raízes reais."
                return render_template('bhaskara.html', error = error, delta = delta)
            
            return render_template('bhaskara.html', delta = delta,
                                    raiz1 = raiz1, 
                                    raiz2 = raiz2)

        except ValueError:
            error = "Por favor, insira valores válidos."
            return render_template('bhaskara.html', error = error)

    return render_template('bhaskara.html', error = error)