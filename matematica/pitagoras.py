from funcoesMatematicas import pitagoras
from logicasFuncoesEndPoint import pegarCamposFloatsOuNone, pegarCasasDecimais, arredondarResultados
from flask import render_template, request

def pitagorasView():
    error = None
    if request.method == 'POST':
        # Pegando os dados do formulário HTML
        # 'request.form.get' retorna o valor enviado pelo usuário ou None se o campo estiver vazio
        campos = pegarCamposFloatsOuNone(['ladoA', 'ladoB', 'ladoC'], request.form)
        cateto1 = campos['ladoA']
        cateto2 = campos['ladoB']
        hipotenusa = campos['ladoC']

        # Criando uma lista apenas com as váriaveis preenchidas
        preenchidos = [campo for campo in [cateto1, cateto2, hipotenusa] if campo is not None]

        # Verifica se o usuário prencheu exatamente 2 campos, se não retorna erro pedindo 2 campos apenas
        if len(preenchidos) != 2:
            error = "Preencha exatamente dois campos!"
            return render_template('pitagoras.html', error=error)
        try:
            cateto1, cateto2, hipotenusa, error = pitagoras(cateto1, cateto2, hipotenusa)

            if error == True:
                error = "A hipotenusa deve ser maior que os catetos"
                return render_template('pitagoras.html', error = error)
            
            # Mantendo os mesmos nomes das variáveis
            casasDecimais = pegarCasasDecimais(request)

            # Aplica o arredondamento nas variáveis
            cateto1, cateto2, hipotenusa = arredondarResultados(
                [cateto1, cateto2, hipotenusa], casasDecimais
            )
            
            return render_template('pitagoras.html', error = error,
                                   cateto1 = cateto1,
                                   cateto2 = cateto2,
                                   hipotenusa = hipotenusa)

        except ValueError:
            error = 'Valores inválidos.'
            return render_template('pitagoras.html', error=error)

    return render_template('pitagoras.html', error=error)