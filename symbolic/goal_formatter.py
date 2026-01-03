# symbolic/goal_formatter.py

def normalize_angle_notation(angle_points):
    """
    Normaliza uma notação de ângulo para formato canônico.
    
    Args:
        angle_points: tupla de 3 pontos (ex: ('A', 'B', 'C'))
    
    Returns:
        str: notação normalizada "∠ABC"
    """
    if len(angle_points) == 3:
        return f"∠{angle_points[0]}{angle_points[1]}{angle_points[2]}"
    return f"angle({''.join(angle_points)})"

def canonicalize_eqangle(goal, main_triangle_points=None):
    """
    Canonicaliza um goal eqangle para não usar pontos auxiliares.
    
    Args:
        goal: tupla eqangle (ex: ('eqangle', 'B', 'C', 'M', 'B', 'M', 'C'))
        main_triangle_points: set de pontos do triângulo principal (ex: {'A', 'B', 'C'})
    
    Returns:
        goal canonizado (mesmo formato), ou goal original se não houver auxiliares
    """
    if not isinstance(goal, tuple) or len(goal) == 0 or goal[0] != "eqangle":
        return goal
    
    if main_triangle_points is None:
        # Se não fornecido, tentar inferir dos pontos do goal
        # Assumir que pontos comuns (A, B, C) são principais, pontos raros (M, etc.) são auxiliares
        all_points = set(goal[1:])
        # Heurística: pontos auxiliares são geralmente únicos (como M)
        # Pontos principais aparecem mais frequentemente
        from collections import Counter
        point_counts = Counter(goal[1:])
        # Pontos que aparecem apenas uma vez podem ser auxiliares
        # Mas isso é uma heurística - melhor receber explicitamente
        return goal
    
    args = list(goal[1:])
    if len(args) < 8:
        return goal
    
    # Verificar se algum ponto dos ângulos é auxiliar (não está no triângulo principal)
    angle1_points = (args[0], args[1], args[3])  # vértice em args[1]
    angle2_points = (args[4], args[5], args[7])  # vértice em args[5]
    
    # Se ambos os ângulos usam apenas pontos do triângulo principal, já está canônico
    angle1_aux = any(p not in main_triangle_points for p in angle1_points)
    angle2_aux = any(p not in main_triangle_points for p in angle2_points)
    
    if not angle1_aux and not angle2_aux:
        return goal  # Já está canônico
    
    # Se há ponto auxiliar, não podemos canonizar automaticamente
    # Retornar goal original (o goal_selector já deve evitar goals com auxiliares)
    return goal

def format_goal(goal, main_triangle_points=None):
    """
    Formata um goal para notação normalizada e humana.
    
    Args:
        goal: tupla simbólica do goal (ex: ('eqangle', 'A', 'B', 'B', 'C', 'A', 'C', 'C', 'B'))
        main_triangle_points: set de pontos do triângulo principal (ex: {'A', 'B', 'C'})
    
    Returns:
        str: goal formatado (ex: "Provar: ∠ABC = ∠ACB")
    """
    if not isinstance(goal, tuple) or len(goal) == 0:
        return str(goal)
    
    # Canonicalizar se necessário (remover pontos auxiliares)
    if goal[0] == "eqangle" and main_triangle_points:
        goal = canonicalize_eqangle(goal, main_triangle_points)
    
    pred_name = goal[0]
    args = goal[1:]
    
    if pred_name == "eqangle":
        # eqangle(a1, a2, b1, b2, c1, c2, d1, d2) representa
        # ângulo entre direções (a1→a2) e (b1→b2) = ângulo entre (c1→c2) e (d1→d2)
        # Para ∠ABC: direções são (A→B) e (B→C), então eqangle(A, B, B, C, ...)
        if len(args) >= 8:
            # Primeiro ângulo: vértice em args[1], pontos args[0], args[1], args[3]
            # Segundo ângulo: vértice em args[5], pontos args[4], args[5], args[7]
            angle1_points = (args[0], args[1], args[3])  # ∠ABC
            angle2_points = (args[4], args[5], args[7])  # ∠DEF
            
            angle1_str = normalize_angle_notation(angle1_points)
            angle2_str = normalize_angle_notation(angle2_points)
            
            return f"Provar: {angle1_str} = {angle2_str}"
    
    elif pred_name == "cong":
        # cong(A, B, C, D) significa AB = CD
        if len(args) >= 4:
            return f"Provar: {args[0]}{args[1]} = {args[2]}{args[3]}"
    
    elif pred_name == "perp":
        # perp(A, B, C, D) significa AB ⟂ CD
        if len(args) >= 4:
            return f"Provar: {args[0]}{args[1]} ⟂ {args[2]}{args[3]}"
    
    elif pred_name == "para":
        # para(A, B, C, D) significa AB ∥ CD
        if len(args) >= 4:
            return f"Provar: {args[0]}{args[1]} ∥ {args[2]}{args[3]}"
    
    # Fallback: formato genérico
    from symbolic.symbolic_to_text import fact_to_text
    return f"Provar: {fact_to_text(goal)}"

