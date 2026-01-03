# main.py

from generation.world_builder import build_world
from symbolic.fact_extractor import extract_facts
from symbolic.ddar_adapter import DDARAdapter, extract_points_from_env
from generation.goal_selector import select_goal
from generation.masker import mask_environment
from generation.snapshot_generator import generate_solution_snapshots
from dataset.exporter import export_sample

# 1. construir mundo completo
env = build_world(seed=42)

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
assert goal is not None, f"Nenhum goal encontrado! All facts: {all_facts}, Givens: {facts}"

# 5. traceback
proof = ddar.get_proof(goal)

# 6. criar problema (apagamento)
# Criar cópia do ambiente antes de mascarar (para snapshots da solução)
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
    aux_removed=aux_removed
)

print(sample)
