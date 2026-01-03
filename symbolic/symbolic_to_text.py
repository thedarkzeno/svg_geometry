# symbolic/symbolic_to_text.py

def fact_to_text(fact):
    """
    Converte um fato simbólico para texto humano-legível.
    
    Args:
        fact: tupla (pred_name, *args)
    
    Returns:
        str: texto legível do fato
    """
    if not isinstance(fact, tuple) or len(fact) == 0:
        return str(fact)
    
    pred_name = fact[0]
    args = fact[1:]
    
    if pred_name == "cong":
        # cong(A, B, C, D) significa AB = CD
        if len(args) >= 4:
            return f"{args[0]}{args[1]} = {args[2]}{args[3]}"
    
    elif pred_name == "eqangle":
        # eqangle(a1, a2, b1, b2, c1, c2, d1, d2) significa que o ângulo entre (a1→a2) e (b1→b2) 
        # é igual ao ângulo entre (c1→c2) e (d1→d2)
        # Para ângulo ∠ABC: direções são (A→B) e (B→C), então eqangle(A, B, B, C, ...)
        # Isso representa ∠ABC = ∠...
        if len(args) >= 8:
            # eqangle(A, B, B, C, D, E, E, F) significa ∠ABC = ∠DEF
            # onde o vértice do primeiro ângulo é args[1] (B), do segundo é args[5] (E)
            vertex1 = args[1]  # vértice do primeiro ângulo
            vertex2 = args[5]  # vértice do segundo ângulo
            # Para ∠ABC: A, B, C (vértice B no meio)
            # Para ∠DEF: D, E, F (vértice E no meio)
            return f"∠{args[0]}{vertex1}{args[3]} = ∠{args[4]}{vertex2}{args[7]}"
    
    elif pred_name == "perp":
        # perp(A, B, C, D) significa AB ⟂ CD
        if len(args) >= 4:
            return f"{args[0]}{args[1]} ⟂ {args[2]}{args[3]}"
    
    elif pred_name == "coll":
        # coll(A, B, C) significa A, B, C são colineares
        if len(args) >= 3:
            points = ", ".join(args[:3])
            return f"Os pontos {points} são colineares"
        elif len(args) == 2:
            return f"Os pontos {', '.join(args)} são colineares"
    
    elif pred_name == "para":
        # para(A, B, C, D) significa AB ∥ CD
        if len(args) >= 4:
            return f"{args[0]}{args[1]} ∥ {args[2]}{args[3]}"
    
    elif pred_name == "cyclic":
        # cyclic(A, B, C, D) significa A, B, C, D são concíclicos
        if len(args) >= 4:
            points = ", ".join(args[:4])
            return f"Os pontos {points} são concíclicos"
    
    # Fallback: formato genérico
    return f"{pred_name}({', '.join(map(str, args))})"


def goal_to_text(goal):
    """Converte um goal (fato objetivo) para texto."""
    return f"Provar: {fact_to_text(goal)}"

