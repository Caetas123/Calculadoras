import math

def bhaskara(a, b, c):
    """
    Resolve uma equação do segundo grau (ax² + bx + c = 0) usando a fórmula de Bhaskara.

    Args:
        a (float): Coeficiente do termo x² (não pode ser zero).
        b (float): Coeficiente do termo x.
        c (float): Termo independente.

    Returns:
        tuple: (raiz1, raiz2, delta, sucesso)
            raiz1 (float or None): Primeira raiz real, ou None se não existir.
            raiz2 (float or None): Segunda raiz real, ou None se não existir.
            delta (float): Valor do discriminante.
            sucesso (bool): True se existem raízes reais, False caso contrário.
    """

    delta = b**2 - 4*a*c
    
    if delta < 0:
        return None, None, delta, False
    else:
        raiz1 = (-b + math.sqrt(delta)) / (2 * a)
        raiz2 = (-b - math.sqrt(delta)) / (2 * a)
        return raiz1, raiz2, delta, True
    
def trigonometria(catetoAdjascente, catetoOposto, hipotenusa, angulo):
    """
    Calcula o lado ou ângulo faltante de um triângulo retângulo usando relações trigonométricas.

    Fórmulas utilizadas:
        - seno   (sen θ = catetoOposto / hipotenusa)
        - cosseno(cos θ = catetoAdjascente / hipotenusa)
        - tangente(tan θ = catetoOposto / catetoAdjascente)
        - Pitágoras (hipotenusa² = catetoOposto² + catetoAdjascente²)

    Args:
        catetoAdjascente (float, opcional): Valor do cateto adjacente. Use 0 se desconhecido.
        catetoOposto (float, opcional): Valor do cateto oposto. Use 0 se desconhecido.
        hipotenusa (float, opcional): Valor da hipotenusa. Use 0 se desconhecido.
        angulo (float, opcional): Valor do ângulo em graus. Use 0 se desconhecido.

    Returns:
        tuple: (catetoAdjascente, catetoOposto, hipotenusa, angulo, erro)
            - catetoAdjascente (float): valor encontrado/informado do cateto adjacente.
            - catetoOposto (float): valor encontrado/informado do cateto oposto.
            - hipotenusa (float): valor encontrado/informado da hipotenusa.
            - angulo (float): valor encontrado/informado do ângulo (em graus).
            - erro (bool): 
                * False → cálculo realizado com sucesso.  
                * True  → dados inconsistentes ou insuficientes.
    """

    if angulo and catetoOposto and not hipotenusa:
        hipotenusa = catetoOposto / math.sin(math.radians(angulo))
        catetoAdjascente = hipotenusa * math.cos(math.radians(angulo))
        return catetoAdjascente, catetoOposto, hipotenusa, angulo, False

    if angulo and catetoAdjascente and not hipotenusa:
        hipotenusa = catetoAdjascente / math.cos(math.radians(angulo))
        catetoOposto = hipotenusa * math.sin(math.radians(angulo))
        return catetoAdjascente, catetoOposto, hipotenusa, angulo, False

    if angulo and hipotenusa and not catetoOposto:
        catetoOposto = hipotenusa * math.sin(math.radians(angulo))
        catetoAdjascente = hipotenusa * math.cos(math.radians(angulo))
        return catetoAdjascente, catetoOposto, hipotenusa, angulo, False

    if angulo and hipotenusa and not catetoAdjascente:
        catetoAdjascente = hipotenusa * math.cos(math.radians(angulo))
        catetoOposto = hipotenusa * math.sin(math.radians(angulo))
        return catetoAdjascente, catetoOposto, hipotenusa, angulo, False

    # Quando o ângulo não é informado
    if not angulo:
        if catetoOposto and hipotenusa:
            angulo = math.degrees(math.asin(catetoOposto / hipotenusa))
            catetoAdjascente = math.sqrt(hipotenusa**2 - catetoOposto**2)
            return catetoAdjascente, catetoOposto, hipotenusa, angulo, False
        
        if catetoAdjascente and hipotenusa:
            angulo = math.degrees(math.acos(catetoAdjascente / hipotenusa))
            catetoOposto = math.sqrt(hipotenusa**2 - catetoAdjascente**2)
            return catetoAdjascente, catetoOposto, hipotenusa, angulo, False
        
        if catetoOposto and catetoAdjascente:
            angulo = math.degrees(math.atan(catetoOposto / catetoAdjascente))
            hipotenusa = math.sqrt(catetoOposto**2 + catetoAdjascente**2)
            return catetoAdjascente, catetoOposto, hipotenusa, angulo, False


def pitagoras(catetoAdjascente, catetoOposto, hipotenusa):
    """
    Calcula lados de um triângulo retângulo usando o Teorema de Pitágoras.

    A função permite calcular o valor de um lado desconhecido 
    quando dois são fornecidos.

    Args:
        catetoAdjascente : float | None
            Valor do cateto adjacente. Pode ser None se desconhecido.
        catetoOposto : float | None
            Valor do cateto oposto. Pode ser None se desconhecido.
        hipotenusa : float | None
            Valor da hipotenusa. Pode ser None se desconhecido.

    Returns:
        tuple : (catetoAdjascente, catetoOposto, hipotenusa, erro)
            - catetoAdjascente : float
                Valor calculado ou informado do cateto adjacente.
            - catetoOposto : float
                Valor calculado ou informado do cateto oposto.
            - hipotenusa : float
                Valor calculado ou informado da hipotenusa.
            - erro : bool
                Indica se houve erro de validação:
                * True  → valores inválidos (ex.: hipotenusa menor ou igual a um cateto).
                * False → cálculo realizado com sucesso.
    """
    # Verificações básicas
    if hipotenusa is not None:
        
        if (catetoAdjascente is not None and hipotenusa <= catetoAdjascente) or \
           (catetoOposto is not None and hipotenusa <= catetoOposto):
                return None, None, None, True
        
        if catetoOposto and hipotenusa and not catetoAdjascente:
            catetoAdjascente = math.sqrt(hipotenusa**2 - catetoOposto**2)
            return catetoAdjascente, catetoOposto, hipotenusa, False
            
        if catetoAdjascente and hipotenusa and not catetoOposto:
            catetoOposto = math.sqrt(hipotenusa**2 - catetoAdjascente**2)
            return catetoAdjascente, catetoOposto, hipotenusa, False
    else:
        hipotenusa = math.sqrt(catetoOposto**2 + catetoAdjascente**2)
        return catetoAdjascente, catetoOposto, hipotenusa, False