from funcoesMatematicas import trigonometria
from logicasFuncoesEndPoint import pegarCamposFloatsOuNone,transformarEmRaiz, formatarRaiz, pegarCasasDecimais, arredondarResultados
from funcoesMatematicas import pitagoras
from flask import render_template, request

def trigonometriaView():
    error = None
    if request.method == 'POST':
        # Pegando os dados do formulário HTML
        # 'request.form.get' retorna o valor enviado pelo usuário ou None se o campo estiver vazio
        campos = pegarCamposFloatsOuNone(['ladoA', 'ladoB', 'ladoC', 'angulo'], request.form)
        catetoAdjascente = campos['ladoA']
        catetoOposto = campos['ladoB']
        hipotenusa = campos['ladoC']
        angulo = campos['angulo']
        
        # Criando uma lista apenas com as váriaveis preenchidas
        preenchidos = [campo for campo in [catetoAdjascente, catetoOposto, hipotenusa, angulo] if campo is not None]

        # Verifica se o usuário prencheu exatamente 2 campos, se não retorna erro pedindo 2 campos apenas
        if len(preenchidos) != 2:
            error = "Preencha exatamente dois campos!"
            return render_template('trigonometria.html', error = error)
        try:
            if (catetoAdjascente and catetoOposto) or (catetoOposto and hipotenusa) or (catetoAdjascente and hipotenusa):
                catetoAdjascente, catetoOposto, hipotenusa, error = pitagoras(catetoAdjascente,
                catetoOposto, hipotenusa)
                
                if error == True:
                    error = "A hipotenusa deve ser maior que os catetos"
                    return render_template('trigonometria.html', error = error)
                
            if (angulo and catetoAdjascente) or (angulo and catetoOposto) or (angulo and hipotenusa):
                catetoAdjascente, catetoOposto, hipotenusa, angulo, error = trigonometria(catetoAdjascente,
                catetoOposto, hipotenusa, angulo)
                
            if angulo is None:
                catetoAdjascente, catetoOposto, hipotenusa, angulo, error = trigonometria(catetoAdjascente,
                catetoOposto, hipotenusa, angulo)
                
            transformaRaiz = [catetoAdjascente, catetoOposto, hipotenusa]
            resultadosRaiz = transformarEmRaiz(transformaRaiz)
            catetoAdjascenteRaizSimbolica, catetoOpostoRaizSimbolica, hipotenusaRaizSimbolica = resultadosRaiz

            # Mantendo os mesmos nomes das variáveis
            catetoAdjascenteRaizSimbolica = formatarRaiz(catetoAdjascenteRaizSimbolica)
            catetoOpostoRaizSimbolica = formatarRaiz(catetoOpostoRaizSimbolica)
            hipotenusaRaizSimbolica = formatarRaiz(hipotenusaRaizSimbolica)


            # Arredonda resultados conforme a precisão que o usuário pediu no form
            casasDecimais = pegarCasasDecimais(request)

            # Aplica o arredondamento nas variáveis
            catetoAdjascente, catetoOposto, hipotenusa, angulo = arredondarResultados(
                [catetoAdjascente, catetoOposto, hipotenusa, angulo], casasDecimais
            )

            return render_template('trigonometria.html', error = error,
                                   catetoOposto = catetoOposto,
                                   catetoAdjascente = catetoAdjascente,
                                   hipotenusa = hipotenusa,
                                   angulo = angulo,
                                   catetoAdjascenteRaizSimbolica = catetoAdjascenteRaizSimbolica,
                                   catetoOpostoRaizSimbolica = catetoOpostoRaizSimbolica,
                                   hipotenusaRaizSimbolica = hipotenusaRaizSimbolica)

        except ValueError:
            error = 'Erro: Valores inválidos.'

    return render_template('trigonometria.html', error = error)