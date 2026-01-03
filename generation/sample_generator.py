# generation/sample_generator.py

from generation.world_builder import build_world
from symbolic.fact_extractor import extract_facts
from symbolic.ddar_adapter import DDARAdapter, extract_points_from_env
from generation.goal_selector import select_goal
from generation.masker import mask_environment
from generation.snapshot_generator import generate_solution_snapshots
from dataset.exporter import export_sample

def generate_sample(seed=None, variant_id=0):
    """
    Gera um sample completo do dataset.
    
    Args:
        seed: semente para randomização
        variant_id: ID da variante geométrica (0=original, 1=espelhado, etc.)
    
    Returns:
        dict: sample completo no formato do dataset, ou None se falhar
    """
    try:
        # 1. construir mundo completo
        env = build_world(seed=seed, variant_id=variant_id)

        # 2. extrair pontos e fatos simbólicos
        points_dict = extract_points_from_env(env)
        facts = extract_facts(env)

        # 3. rodar DDAR
        ddar = DDARAdapter(points_dict)
        for f in facts:
            ddar.add_fact(f)

        ddar.run()

        all_facts = ddar.all_facts()

        # 4. escolher objetivo
        goal = select_goal(all_facts, facts)
        if goal is None:
            return None  # Não encontrou goal válido

        # 5. traceback
        proof = ddar.get_proof(goal)
        if not proof:
            return None  # Prova vazia

        # 6. criar problema (apagamento)
        env_complete = env.clone()
        aux_removed = mask_environment(env, proof, facts, goal)

        problem_svg = env.generate_svg()

        # 7. gerar snapshots da solução
        solution_svgs = generate_solution_snapshots(env_complete, proof, facts, goal)

        # 8. exportar
        sample = export_sample(
            problem_svg=problem_svg,
            givens=facts,
            goal=goal,
            steps=proof,
            solution_svgs=solution_svgs,
            aux_removed=aux_removed,
            env_problem=env
        )
        
        return sample
    
    except Exception as e:
        # Em caso de erro, retornar None (pode ser logado externamente)
        return None

