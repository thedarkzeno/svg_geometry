# generation/goal_selector.py

def _extract_aux_labels(givens):
    """Extrai labels de pontos auxiliares dos givens (mesma lógica do masker)."""
    aux_labels = set()
    for fact in givens:
        pred_name = fact[0] if isinstance(fact, tuple) and len(fact) > 0 else None
        if pred_name == "coll":
            args = fact[1:]
            if len(args) == 3:
                aux_labels.add(args[1])
        elif pred_name == "perp":
            args = fact[1:]
            if len(args) >= 2:
                aux_labels.add(args[1])
        elif pred_name == "cong" and len(fact) >= 5:
            args = fact[1:]
            if args[1] == args[2]:
                aux_labels.add(args[1])
    return aux_labels

def select_goal(all_facts, givens):
    """
    Seleciona um goal que:
    - Não está nos givens
    - Prefere não envolver pontos auxiliares (apenas triângulo principal)
    - É preferencialmente uma igualdade de ângulos (eqangle)
    - Tem prova não vazia (verificado externamente)
    """
    givens_set = {tuple(g) for g in givens}
    aux_labels = _extract_aux_labels(givens)
    
    def involves_aux(fact):
        """Verifica se um fato envolve pontos auxiliares."""
        if not isinstance(fact, tuple) or len(fact) == 0:
            return False
        args = fact[1:]
        return any(arg in aux_labels for arg in args if isinstance(arg, str))
    
    def count_aux_in_fact(fact):
        """Conta quantos pontos auxiliares estão em um fato."""
        if not isinstance(fact, tuple) or len(fact) == 0:
            return 0
        args = fact[1:]
        return sum(1 for arg in args if isinstance(arg, str) and arg in aux_labels)
    
    # Tentar primeiro: eqangle sem auxiliares
    candidates_no_aux = []
    for f in all_facts:
        if f[0] == "eqangle" and tuple(f) not in givens_set and not involves_aux(f):
            return f
    
    # Tentar segundo: outras igualdades sem auxiliares
    for f in all_facts:
        if f[0] in ("cong",) and tuple(f) not in givens_set and not involves_aux(f):
            return f
    
    # Tentar terceiro: qualquer fato sem auxiliares
    for f in all_facts:
        if tuple(f) not in givens_set and not involves_aux(f):
            return f
    
    # Fallback: se não há goal sem auxiliares, permitir com auxiliares
    # Mas priorizar os que têm menos auxiliares
    candidates_with_aux = []
    for f in all_facts:
        if f[0] == "eqangle" and tuple(f) not in givens_set:
            candidates_with_aux.append((count_aux_in_fact(f), f))
    
    if candidates_with_aux:
        # Ordenar por número de auxiliares (menos primeiro)
        candidates_with_aux.sort(key=lambda x: x[0])
        return candidates_with_aux[0][1]
    
    # Último recurso: qualquer fato deduzido
    for f in all_facts:
        if tuple(f) not in givens_set:
            return f
    
    return None
