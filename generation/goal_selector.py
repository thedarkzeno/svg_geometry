# generation/goal_selector.py

def select_goal(all_facts, givens):
    """
    Seleciona um goal que:
    - Não está nos givens
    - É preferencialmente uma igualdade de ângulos (eqangle)
    - Tem prova não vazia (verificado externamente)
    """
    givens_set = {tuple(g) for g in givens}
    
    # Preferir eqangle (igualdade de ângulos)
    for f in all_facts:
        if f[0] == "eqangle" and tuple(f) not in givens_set:
            return f
    
    # Depois, outras igualdades interessantes
    for f in all_facts:
        if f[0] in ("cong",) and tuple(f) not in givens_set:
            return f
    
    # Por último, qualquer fato que não está nos givens
    for f in all_facts:
        if tuple(f) not in givens_set:
            return f
    
    return None
