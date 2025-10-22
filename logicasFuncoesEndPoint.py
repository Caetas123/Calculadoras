from sympy import nsimplify, sqrt
import re

def pegarCamposFloatsOuNone(nomes, request_form):
    return {
        nome: float(valor) if valor not in (None, '', 'None') else None
        for nome in nomes
        for valor in [request_form.get(nome)]
    }

def pegarCasasDecimais(request):
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
    bases = [sqrt(i) for i in range(2, 51)]

    for v in valores:
        if v is None:
            resultados.append(None)
            continue

        melhorExpr = None
        menorErro = float("inf")

        # Testa todos os múltiplos de todas as raízes
        for base in bases:
            for k in range(1, max_mult + 1):
                estimado = k * base.evalf()
                erro = abs(v - estimado)
                if erro < menorErro:
                    menorErro = erro
                    melhorExpr = f"{k}*{base}"

        # Adiciona apenas o melhor candidato
        if menorErro <= tol:
            resultados.append(melhorExpr)
        else:
            resultados.append(str(nsimplify(v, bases)))
    return resultados

def formatarRaiz(expr:str):
    if expr is None:
        return None
                
    if not "sqrt" in expr:
        return None
                
    expr = expr.replace('sqrt', '√')
    expr = re.sub(r'√\((\d+)\)', r'√\1', expr)

    expr = expr.replace('*√', '√')

    if '√' not in expr:
        return None

    return expr
