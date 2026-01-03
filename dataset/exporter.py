# dataset/exporter.py

from symbolic.symbolic_to_text import fact_to_text
from symbolic.goal_formatter import format_goal
from symbolic.step_aggregator import aggregate_steps
from symbolic.visual_givens_extractor import extract_visual_givens
from symbolic.problem_givens_splitter import split_givens, extract_aux_labels_from_givens

def calculate_difficulty(proof_length, aux_removed, goal_type="eqangle"):
    """
    Calcula dificuldade baseada em fatores ajustados:
    - comprimento da prova (peso 1)
    - número de auxiliares removidos (peso 1)
    - tipo do goal (apenas cyclic é mais difícil)
    
    Args:
        proof_length: número de passos na prova
        aux_removed: número de construções auxiliares removidas
        goal_type: tipo do goal ("eqangle", "cong", "cyclic", etc.)
    
    Returns:
        str: "easy", "medium", ou "hard"
    """
    # Penalidade apenas para tipos realmente avançados
    goal_penalty = 0
    if goal_type == "cyclic":
        goal_penalty = 1
    
    # Cálculo do score (ajustado)
    difficulty_score = proof_length + aux_removed + goal_penalty
    
    # Mapeamento ajustado
    if difficulty_score <= 4:
        return "easy"
    elif difficulty_score <= 7:
        return "medium"
    else:
        return "hard"

def export_sample(problem_svg, givens, goal, steps, solution_svgs=None, aux_removed=0, env_problem=None):
    """
    Exporta um sample do dataset.
    
    Args:
        problem_svg: SVG do problema (sem construções auxiliares)
        givens: lista de fatos dados (lógicos)
        goal: fato objetivo
        steps: lista de passos da prova (cada passo é um fato)
        solution_svgs: lista opcional de SVGs para cada passo da solução
        aux_removed: número de construções auxiliares removidas
        env_problem: Environment do problema (para extrair givens visuais)
    """
    # Agregar passos semanticamente
    aggregated_steps = aggregate_steps(steps)
    
    # Processar steps para o formato esperado
    solution_steps = []
    if solution_svgs:
        for i, step_text in enumerate(aggregated_steps):
            svg = solution_svgs[i] if i < len(solution_svgs) else ""
            solution_steps.append({
                "text": step_text,
                "svg": svg
            })
    else:
        # Se não há SVGs, apenas texto
        for step_text in aggregated_steps:
            solution_steps.append({
                "text": step_text,
                "svg": ""
            })
    
    # Extrair givens visuais
    givens_visual = []
    if env_problem:
        givens_visual = extract_visual_givens(env_problem)
    
    # Separar givens em problem vs hidden
    aux_labels = extract_aux_labels_from_givens(givens)
    givens_problem, givens_hidden = split_givens(givens, aux_labels)
    
    # Identificar pontos do triângulo principal (para canonicalização do goal)
    # Extrair de givens_problem (cong sem ponto médio)
    main_triangle_points = set()
    for fact in givens_problem:
        if isinstance(fact, tuple) and len(fact) > 0 and fact[0] == "cong":
            args = fact[1:]
            if len(args) >= 4 and args[1] != args[2]:  # Não é ponto médio
                for arg in args:
                    if isinstance(arg, str):
                        main_triangle_points.add(arg)
    
    # Calcular metadata
    proof_length = len(steps)  # Usar steps originais para metadata
    goal_type = goal[0] if isinstance(goal, tuple) and len(goal) > 0 else "unknown"
    difficulty = calculate_difficulty(proof_length, aux_removed, goal_type)
    
    # Formatar goal (com canonicalização)
    goal_formatted = format_goal(goal, main_triangle_points if main_triangle_points else None)
    
    return {
        "problem": {
            "givens_logical": givens_problem,
            "givens_hidden": givens_hidden,
            "givens_visual": givens_visual,
            "goal": goal_formatted,
            "svg": problem_svg
        },
        "solution": {
            "steps": solution_steps
        },
        "metadata": {
            "proof_length": proof_length,
            "aux_removed": aux_removed,
            "difficulty": difficulty
        }
    }
