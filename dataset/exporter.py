# dataset/exporter.py

from symbolic.symbolic_to_text import fact_to_text, goal_to_text

def calculate_difficulty(proof_length):
    """
    Calcula dificuldade baseada no tamanho da prova.
    
    Args:
        proof_length: número de passos na prova
    
    Returns:
        str: "easy", "medium", ou "hard"
    """
    if proof_length <= 3:
        return "easy"
    elif proof_length <= 6:
        return "medium"
    else:
        return "hard"

def export_sample(problem_svg, givens, goal, steps, solution_svgs=None, aux_removed=0):
    """
    Exporta um sample do dataset.
    
    Args:
        problem_svg: SVG do problema (sem construções auxiliares)
        givens: lista de fatos dados
        goal: fato objetivo
        steps: lista de passos da prova (cada passo é um fato ou lista de fatos)
        solution_svgs: lista opcional de SVGs para cada passo da solução
    """
    # Processar steps para o formato esperado
    solution_steps = []
    if solution_svgs:
        for i, step in enumerate(steps):
            text = fact_to_text(step) if isinstance(step, tuple) else str(step)
            svg = solution_svgs[i] if i < len(solution_svgs) else ""
            solution_steps.append({
                "text": text,
                "svg": svg
            })
    else:
        # Se não há SVGs, apenas texto
        for step in steps:
            text = fact_to_text(step) if isinstance(step, tuple) else str(step)
            solution_steps.append({
                "text": text,
                "svg": ""
            })
    
    # Calcular metadata
    proof_length = len(steps)
    difficulty = calculate_difficulty(proof_length)
    
    return {
        "problem": {
            "givens": givens,
            "goal": goal_to_text(goal),
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
