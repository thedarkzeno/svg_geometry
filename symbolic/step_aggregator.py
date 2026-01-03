# symbolic/step_aggregator.py

from symbolic.symbolic_to_text import fact_to_text

def aggregate_steps(steps):
    """
    Agrega passos semanticamente relacionados em passos compostos.
    
    Args:
        steps: lista de fatos (tuplas)
    
    Returns:
        list: lista de passos agregados (strings ou tuplas)
    """
    if not steps:
        return []
    
    aggregated = []
    i = 0
    
    while i < len(steps):
        current_step = steps[i]
        
        # Verificar se podemos agrupar com próximos passos
        if i + 2 < len(steps):
            next_step = steps[i + 1]
            next_next_step = steps[i + 2]
            
            # Padrão: coll + cong (ponto médio) + perp (perpendicular)
            if (_is_collinear(current_step) and 
                _is_cong_midpoint(next_step) and 
                _is_perpendicular(next_next_step)):
                # Verificar se são sobre os mesmos pontos
                if _same_base_points([current_step, next_step, next_next_step]):
                    aggregated_step = _format_aggregated_midpoint_perp(
                        current_step, next_step, next_next_step
                    )
                    aggregated.append(aggregated_step)
                    i += 3
                    continue
        
        # Se não agregou, adicionar passo normal
        aggregated.append(fact_to_text(current_step))
        i += 1
    
    return aggregated

def _is_collinear(step):
    """Verifica se o passo é uma colinearidade."""
    return isinstance(step, tuple) and len(step) > 0 and step[0] == "coll"

def _is_cong_midpoint(step):
    """Verifica se o passo é congruência de ponto médio (cong(B, M, M, C))."""
    return (isinstance(step, tuple) and len(step) >= 5 and 
            step[0] == "cong" and step[2] == step[3])

def _is_perpendicular(step):
    """Verifica se o passo é perpendicularidade."""
    return isinstance(step, tuple) and len(step) > 0 and step[0] == "perp"

def _same_base_points(steps):
    """
    Verifica se os passos referem-se aos mesmos pontos base.
    Por exemplo: coll(B, M, C), cong(B, M, M, C), perp(A, M, B, C)
    todos referem-se a B, M, C (com A adicional no perp).
    """
    if len(steps) < 2:
        return True
    
    # Extrair pontos únicos de cada passo
    points_sets = []
    for step in steps:
        if isinstance(step, tuple):
            points = set(arg for arg in step[1:] if isinstance(arg, str))
            points_sets.append(points)
        else:
            return False
    
    # Verificar se há sobreposição significativa (pelo menos 2 pontos em comum)
    if len(points_sets) < 2:
        return True
    
    intersection = points_sets[0]
    for ps in points_sets[1:]:
        intersection = intersection & ps
    
    # Se há pelo menos 2 pontos em comum, consideramos relacionados
    return len(intersection) >= 2

def _format_aggregated_midpoint_perp(coll_step, cong_step, perp_step):
    """
    Formata passo agregado para ponto médio + perpendicular.
    
    Exemplo:
    coll(B, M, C), cong(B, M, M, C), perp(A, M, B, C)
    → "M é o ponto médio de BC e AM é perpendicular a BC"
    """
    # Extrair pontos
    # coll(B, M, C): B, M, C
    # cong(B, M, M, C): B, M, C
    # perp(A, M, B, C): A, M, B, C
    
    if len(coll_step) >= 4:
        B, M, C = coll_step[1], coll_step[2], coll_step[3]
        
        if len(perp_step) >= 5:
            A = perp_step[1]
            return f"M é o ponto médio de {B}{C} e {A}{M} é perpendicular a {B}{C}"
    
    # Fallback: combinar textos individuais
    return f"{fact_to_text(coll_step)}. {fact_to_text(cong_step)}. {fact_to_text(perp_step)}"

