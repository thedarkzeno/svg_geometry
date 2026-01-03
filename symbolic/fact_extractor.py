# symbolic/fact_extractor.py

import math
from visual.environment import (
    Point, Line, Triangle, Circle, Perpendicular
)

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def extract_facts(env):
    """
    Extrai fatos simbólicos do ambiente visual.
    Retorna lista de tuplas no formato AlphaGeometry.
    """
    facts = []
    
    # Criar dicionário de pontos por label
    points_dict = {}
    for shape in env.shapes:
        if isinstance(shape, Point) and shape.label:
            points_dict[shape.label] = shape

    # Segmentos (linhas) - DDAR constrói automaticamente, mas marcamos para referência
    for shape in env.shapes:
        if isinstance(shape, Line):
            a = shape.start.label
            b = shape.end.label
            # Linhas são construídas automaticamente pelo DDAR
            pass

    # Triângulos
    for shape in env.shapes:
        if isinstance(shape, Triangle):
            A = shape.p1.label
            B = shape.p2.label
            C = shape.p3.label
            
            # Congruência de lados (isósceles): cong(A, B, A, C) significa AB = AC
            ab = distance(shape.p1, shape.p2)
            ac = distance(shape.p1, shape.p3)
            if abs(ab - ac) < 1e-6:
                facts.append(("cong", A, B, A, C))

    # Perpendicular e ponto médio
    for shape in env.shapes:
        if isinstance(shape, Perpendicular):
            # shape.perpendicular_line vai do vértice até o ponto médio
            A = shape.perpendicular_line.start.label  # vértice
            
            # Encontrar os pontos B e C do lado oposto
            triangle = shape.triangle
            if shape.vertex == triangle.p1:
                B, C = triangle.p2.label, triangle.p3.label
            elif shape.vertex == triangle.p2:
                B, C = triangle.p1.label, triangle.p3.label
            else:  # shape.vertex == triangle.p3
                B, C = triangle.p1.label, triangle.p2.label
            
            # Encontrar o ponto médio M no ambiente (pode ter label "M" ou precisamos encontrar pelas coordenadas)
            # O ponto médio tem coordenadas calculadas do midpoint de B e C
            M = None
            mid_x = shape.perpendicular_line.end.x
            mid_y = shape.perpendicular_line.end.y
            
            # Procurar ponto com essas coordenadas no ambiente
            for pt_shape in env.shapes:
                if isinstance(pt_shape, Point) and pt_shape.label:
                    if (abs(pt_shape.x - mid_x) < 1e-6 and 
                        abs(pt_shape.y - mid_y) < 1e-6):
                        M = pt_shape.label
                        break
            
            # Se não encontrou, usar "M" (assumindo que foi adicionado no world_builder)
            if M is None:
                M = "M"
            
            # Verificar se M está no points_dict antes de usar
            if M not in points_dict:
                continue
            
            # coll(B, M, C): M está na linha BC
            facts.append(("coll", B, M, C))
            
            # cong(B, M, M, C): BM = MC (M é ponto médio)
            bm = distance(points_dict[B], points_dict[M])
            mc = distance(points_dict[M], points_dict[C])
            if abs(bm - mc) < 1e-6:
                facts.append(("cong", B, M, M, C))
            
            # perp(A, M, B, C): linha AM é perpendicular a linha BC
            facts.append(("perp", A, M, B, C))

    return facts
