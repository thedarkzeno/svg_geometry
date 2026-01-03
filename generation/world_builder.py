# generation/world_builder.py

import random
import math
from visual.environment import Environment

def build_world(seed=None, variant_id=0):
    """
    Constrói um mundo geométrico completo.
    
    Args:
        seed: semente para randomização
        variant_id: ID da variante (0=original, 1=espelhado, 2=rotacionado, etc.)
    
    Returns:
        Environment: ambiente com mundo completo
    """
    if seed is not None:
        random.seed(seed)

    env = Environment(400, 300)

    # Base: triângulo isósceles
    base_A = (200, 50)
    base_B = (100, 200)
    base_C = (300, 200)
    
    # Aplicar variações geométricas
    if variant_id == 0:
        # Original
        A = env.add_point(base_A[0], base_A[1], "A")
        B = env.add_point(base_B[0], base_B[1], "B")
        C = env.add_point(base_C[0], base_C[1], "C")
    elif variant_id == 1:
        # Espelhado horizontalmente
        center_x = 200
        A = env.add_point(2 * center_x - base_A[0], base_A[1], "A")
        B = env.add_point(2 * center_x - base_B[0], base_B[1], "B")
        C = env.add_point(2 * center_x - base_C[0], base_C[1], "C")
    elif variant_id == 2:
        # Rotacionado 180 graus em torno do centro
        center_x, center_y = 200, 125
        A = env.add_point(2 * center_x - base_A[0], 2 * center_y - base_A[1], "A")
        B = env.add_point(2 * center_x - base_B[0], 2 * center_y - base_B[1], "B")
        C = env.add_point(2 * center_x - base_C[0], 2 * center_y - base_C[1], "C")
    else:
        # Fallback para original
        A = env.add_point(base_A[0], base_A[1], "A")
        B = env.add_point(base_B[0], base_B[1], "B")
        C = env.add_point(base_C[0], base_C[1], "C")

    triangle = env.add_triangle(A, B, C)

    # Construção auxiliar: mediatriz
    # Adicionar ponto médio M de BC explicitamente
    M = env.add_point((B.x + C.x) / 2, (B.y + C.y) / 2, "M")
    env.add_perpendicular(triangle, A)

    return env
