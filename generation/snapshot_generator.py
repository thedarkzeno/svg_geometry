# generation/snapshot_generator.py

from visual.environment import Environment
from symbolic.fact_extractor import extract_facts
from generation.world_builder import build_world

def generate_solution_snapshots(env_complete, proof_steps, givens, goal):
    """
    Gera snapshots do ambiente para cada passo da solução.
    
    Args:
        env_complete: Environment completo com todas as construções
        proof_steps: lista de fatos da prova (cada passo)
        givens: fatos dados
        goal: fato objetivo
    
    Returns:
        list: lista de SVGs, um para cada passo
    """
    # Por enquanto, retornar o SVG completo para cada passo
    # TODO: implementar progressivo (construções aparecem conforme a prova)
    svgs = []
    for step in proof_steps:
        # Usar o ambiente completo para todos os passos
        # (no futuro, pode-se implementar construção progressiva)
        svg = env_complete.generate_svg()
        svgs.append(svg)
    return svgs

