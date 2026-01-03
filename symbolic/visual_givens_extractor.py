# symbolic/visual_givens_extractor.py

def extract_visual_givens(env):
    """
    Extrai objetos visuais presentes no SVG do problema.
    
    Args:
        env: Environment (já mascarado, só contém o problema)
    
    Returns:
        list: lista de identificadores visuais (ex: ["A", "B", "C", "AB", "AC", "BC"])
    """
    visual_givens = []
    
    # Coletar pontos
    points = {}
    for shape in env.shapes:
        if hasattr(shape, "label") and shape.label:
            points[shape.label] = shape
            visual_givens.append(shape.label)
    
    # Coletar segmentos/linhas
    segments = set()
    for shape in env.shapes:
        if hasattr(shape, "start") and hasattr(shape, "end"):
            start_label = getattr(shape.start, "label", None)
            end_label = getattr(shape.end, "label", None)
            if start_label and end_label:
                # Ordenar labels para consistência
                seg = tuple(sorted([start_label, end_label]))
                segments.add(seg)
    
    # Adicionar segmentos formatados
    for seg in sorted(segments):
        visual_givens.append(f"{seg[0]}{seg[1]}")
    
    # Coletar triângulos
    for shape in env.shapes:
        if hasattr(shape, "p1") and hasattr(shape, "p2") and hasattr(shape, "p3"):
            p1_label = getattr(shape.p1, "label", None)
            p2_label = getattr(shape.p2, "label", None)
            p3_label = getattr(shape.p3, "label", None)
            if p1_label and p2_label and p3_label:
                visual_givens.append(f"{p1_label}{p2_label}{p3_label}")
    
    return sorted(visual_givens)

