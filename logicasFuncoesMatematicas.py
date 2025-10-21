from funcoesMatematicas import bhaskara, pitagoras, trigonometria
from flask import render_template, request
from sympy import nsimplify, sqrt
import re

# --------------------------
# Funções auxiliares
# --------------------------

def GetCasasDecimais(request):
    """
    Retorna o número de casas decimais a serem usadas para arredondamento, 
    com base nos campos do formulário HTML.

    Comportamento:
        - Se 'precisao' == 'custom' e 'precisaoCustom' estiver preenchido, retorna esse valor como int.
        - Se 'precisao' for um valor numérico (ex: "1", "0.01"), retorna o número de casas decimais após o ponto.
        - Se 'precisao' == 'none' ou não preenchido, retorna 8 (padrão).

    Args:
        request: objeto de requisição contendo os campos do form 'precisao' e 'precisaoCustom'.

    Returns:
        int: número de casas decimais a serem usadas no arredondamento.
    """

    precisao = request.form.get('precisao')
    precisaoCustom = request.form.get('precisaoCustom')

    if precisao == 'custom' and precisaoCustom:
        return int(precisaoCustom)
    
    elif precisao and precisao != 'none':
        return len(str(precisao).split('.')[-1])
    
    # Precisão padrão
    else:
        return 8

def arredondarResultados(valores, casasDecimais):
    """
    Arredonda valores numéricos para a quantidade de casas decimais informada.
    Funciona com dicionários, listas/tuplas ou valores únicos. Mantém None intacto.

    Args:
        valores (dict, list, tuple, float, int, None): Valores a serem arredondados.
        casasDecimais (int): Número de casas decimais para arredondamento.

    Returns:
        Mesmo tipo que 'valores', mas com os números arredondados.
    """

    if isinstance(valores, dict):
        return {k: round(v, casasDecimais) if v is not None else None for k, v in valores.items()}
    
    elif isinstance(valores, (list, tuple)):
        return [round(v, casasDecimais) if v is not None else None for v in valores]
    
    else:
        return round(valores, casasDecimais) if valores is not None else None

def transformarEmRaiz(valores, tol=1e-1, max_mult=50):
    """
    Tenta transformar números decimais em representações com raízes.

    A função percorre os valores recebidos e procura:
      1. Aproximações de múltiplos de raízes conhecidas (sqrt(2), sqrt(3), ...).
      2. Caso não encontre, utiliza sympy.nsimplify para gerar uma forma simbólica.

    Args:
        valores : list[float | None]
            Lista de valores numéricos (ou None) a serem transformados.
        tol : float, opcional
            Tolerância para comparação numérica (default: 1e-1).
        max_mult : int, opcional
            Máximo multiplicador a ser testado para múltiplos de raízes (default: 50).

    Returns:
        list[str | None]
            Lista de representações simbólicas (strings) dos valores.
            Se o valor for None, retorna None na mesma posição.
    """
    resultados = []

    # Raízes base possíveis
    bases = [sqrt(2), sqrt(3), sqrt(5), sqrt(10), sqrt(13), sqrt(17), sqrt(20), sqrt(25)]

    for v in valores:
        encontrado = False

        if v is None:
            resultados.append(None)
            continue

        # Verifica se v é múltiplo de alguma raiz
        for base in bases:
            for k in range(1, max_mult):
                if abs(v - k*base.evalf()) < tol:
                    resultados.append(f"{k}*{base}")  # formato simbólico
                    encontrado = True
                    break
            if encontrado:
                break

        # Se não encontrou múltiplo, tenta simplificar com nsimplify
        if not encontrado:
            expr = nsimplify(v, bases)
            resultados.append(str(expr))

    return resultados

# --------------------------
# Views
# --------------------------

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


def trigonometriaView():
    error = None
    if request.method == 'POST':
        # Pegando os dados do formulário HTML
        # 'request.form.get' retorna o valor enviado pelo usuário ou None se o campo estiver vazio
        catetoAdjascente = request.form.get('ladoA')
        catetoOposto = request.form.get('ladoB')
        hipotenusa = request.form.get('ladoC')
        angulo = request.form.get('angulo')

        # Convertendo os valores para float se foram preenchidos, caso contrário mantém None
        catetoAdjascente = float(catetoAdjascente) if catetoAdjascente else None
        catetoOposto = float(catetoOposto) if catetoOposto else None
        hipotenusa = float(hipotenusa) if hipotenusa else None
        angulo = float(angulo) if angulo else None
        
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

            def formatarRaiz(expr):
                if expr is None:
                    return None
                
                # troca sqrt(10) → √10
                expr = expr.replace('sqrt', '√')
                expr = re.sub(r'√\((\d+)\)', r'√\1', expr)

                # remove multiplicador 1* → só √n
                expr = expr.replace('1*√', '√')

                # tira o * quando for tipo 19*√10 → 19√10
                expr = expr.replace('*√', '√')

                # se não tiver '√', então não é raiz → retorna None
                if '√' not in expr:
                    return None

                return expr

            # Mantendo os mesmos nomes das variáveis
            catetoAdjascenteRaizSimbolica = formatarRaiz(catetoAdjascenteRaizSimbolica)
            catetoOpostoRaizSimbolica = formatarRaiz(catetoOpostoRaizSimbolica)
            hipotenusaRaizSimbolica = formatarRaiz(hipotenusaRaizSimbolica)


            # Arredonda resultados conforme a precisão que o usuário pediu no form
            casasDecimais = GetCasasDecimais(request)

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


def pitagorasView():
    error = None
    if request.method == 'POST':
        # Pegando os dados do formulário HTML
        # 'request.form.get' retorna o valor enviado pelo usuário ou None se o campo estiver vazio
        catetoAdjascente = request.form.get('ladoA')
        catetoOposto = request.form.get('ladoB')
        hipotenusa = request.form.get('ladoC')

        # Convertendo os valores para float se foram preenchidos, caso contrário mantém None
        catetoOposto = float(catetoOposto) if catetoOposto else None
        catetoAdjascente = float(catetoAdjascente) if catetoAdjascente else None
        hipotenusa = float(hipotenusa) if hipotenusa else None

        # Criando uma lista apenas com as váriaveis preenchidas
        preenchidos = [campo for campo in [catetoAdjascente, catetoOposto, hipotenusa] if campo is not None]

        # Verifica se o usuário prencheu exatamente 2 campos, se não retorna erro pedindo 2 campos apenas
        if len(preenchidos) != 2:
            error = "Preencha exatamente dois campos!"
            return render_template('pitagoras.html', error=error)
        try:
            catetoAdjascente, catetoOposto, hipotenusa, error = pitagoras(catetoAdjascente, catetoOposto, hipotenusa)

            if error == True:
                error = "A hipotenusa deve ser maior que os catetos"
                return render_template('pitagoras.html', error = error)
            
            # Mantendo os mesmos nomes das variáveis
            casasDecimais = GetCasasDecimais(request)

            # Aplica o arredondamento nas variáveis
            catetoAdjascente, catetoOposto, hipotenusa = arredondarResultados(
                [catetoAdjascente, catetoOposto, hipotenusa], casasDecimais
            )
            
            return render_template('pitagoras.html', error = error,
                                   catetoOposto = catetoOposto,
                                   catetoAdjascente = catetoAdjascente,
                                   hipotenusa = hipotenusa)

        except ValueError:
            error = 'Valores inválidos.'
            return render_template('pitagoras.html', error=error)

    return render_template('pitagoras.html', error=error)
