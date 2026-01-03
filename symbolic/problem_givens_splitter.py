# symbolic/problem_givens_splitter.py

def split_givens(givens_all, aux_labels):
    """
    Separa givens em problem (dados ao aluno) vs hidden (verdadeiros mas não dados).
    
    Args:
        givens_all: lista completa de fatos (givens lógicos)
        aux_labels: set de labels de pontos auxiliares (ex: {'M'})
    
    Returns:
        tuple: (givens_problem, givens_hidden)
    """
    givens_problem = []
    givens_hidden = []
    
    for fact in givens_all:
        # Verificar se o fato envolve pontos auxiliares
        fact_args = fact[1:] if isinstance(fact, tuple) and len(fact) > 0 else []
        involves_aux = any(arg in aux_labels for arg in fact_args if isinstance(arg, str))
        
        if involves_aux:
            # Fatos com pontos auxiliares são "hidden" (construções auxiliares)
            givens_hidden.append(fact)
        else:
            # Fatos sem auxiliares são "problem" (dados ao aluno)
            givens_problem.append(fact)
    
    return givens_problem, givens_hidden

def extract_aux_labels_from_givens(givens):
    """
    Extrai labels de pontos auxiliares dos givens.
    Usa mesma lógica do mask_environment.
    
    Args:
        givens: lista de fatos
    
    Returns:
        set: conjunto de labels auxiliares
    """
    aux_labels = set()
    
    for fact in givens:
        pred_name = fact[0] if isinstance(fact, tuple) and len(fact) > 0 else None
        if pred_name == "coll":
            # coll(B, M, C) - M é auxiliar
            args = fact[1:]
            if len(args) == 3:
                aux_labels.add(args[1])  # M é o ponto do meio
        elif pred_name == "perp":
            # perp(A, M, B, C) - M é auxiliar
            args = fact[1:]
            if len(args) >= 2:
                aux_labels.add(args[1])  # Segundo ponto é geralmente auxiliar
        elif pred_name == "cong" and len(fact) >= 5:
            # cong(B, M, M, C) - M aparece duas vezes, é ponto médio
            args = fact[1:]
            if args[1] == args[2]:  # M aparece no meio
                aux_labels.add(args[1])
    
    return aux_labels

