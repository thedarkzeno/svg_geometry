# generation/world_builder.py

import random
from visual.environment import Environment

def build_world(seed=None):
    if seed is not None:
        random.seed(seed)

    env = Environment(400, 300)

    # Triângulo isósceles
    A = env.add_point(200, 50, "A")
    B = env.add_point(100, 200, "B")
    C = env.add_point(300, 200, "C")

    triangle = env.add_triangle(A, B, C)

    # Construção auxiliar: mediatriz
    # Adicionar ponto médio M de BC explicitamente
    M = env.add_point((B.x + C.x) / 2, (B.y + C.y) / 2, "M")
    env.add_perpendicular(triangle, A)

    return env
