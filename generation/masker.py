# generation/masker.py

def mask_environment(env, proof_facts, givens, goal):
    """
    Remove construções auxiliares do ambiente visual.
    Mantém apenas o que é necessário para o problema (givens explícitos mínimos).
    
    Estratégia: identificar pontos/construções auxiliares
    - Pontos que aparecem em fatos sobre construções (coll com ponto médio, perp) são auxiliares
    - Perpendiculares são sempre auxiliares
    - Linhas que conectam pontos auxiliares são auxiliares
    """
    # Identificar pontos auxiliares
    # Pontos que aparecem em coll, perp, ou cong com ponto médio são auxiliares
    aux_labels = set()
    
    for fact in givens:
        pred_name = fact[0]
        if pred_name == "coll":
            # coll(B, M, C) - M é auxiliar
            # Se há 3 pontos colineares e um deles é ponto médio, é auxiliar
            args = fact[1:]
            if len(args) == 3:
                # O ponto do meio em coll pode ser ponto médio (auxiliar)
                aux_labels.add(args[1])  # M é o ponto do meio
        elif pred_name == "perp":
            # perp(A, M, B, C) - M é auxiliar (ponto médio)
            args = fact[1:]
            if len(args) >= 2:
                aux_labels.add(args[1])  # Segundo ponto é geralmente auxiliar
        elif pred_name == "cong" and len(fact) >= 5:
            # cong(B, M, M, C) - M aparece duas vezes, é ponto médio (auxiliar)
            args = fact[1:]
            if args[1] == args[2]:  # M aparece no meio
                aux_labels.add(args[1])
    
    # Labels necessários para o problema: goal + pontos básicos (não auxiliares)
    necessary_labels = set()
    
    # Labels do goal (sempre necessários, excluindo auxiliares)
    for item in goal[1:]:
        if isinstance(item, str) and item not in aux_labels:
            necessary_labels.add(item)
    
    # Labels dos givens básicos (cong sem ponto médio)
    for fact in givens:
        pred_name = fact[0]
        if pred_name == "cong":
            args = fact[1:]
            # cong(A, B, A, C) - A, B, C são básicos (não são ponto médio)
            # Verificar se não é cong(B, M, M, C) - esse é ponto médio
            if len(args) >= 4 and args[1] != args[2]:  # Não é ponto médio
                for arg in args:
                    if isinstance(arg, str) and arg not in aux_labels:
                        necessary_labels.add(arg)
    
    # Filtrar shapes: manter apenas os necessários (sem auxiliares)
    filtered = []
    for shape in env.shapes:
        # Pontos: manter apenas os não-auxiliares
        if hasattr(shape, "label") and shape.label:
            if shape.label in necessary_labels:
                filtered.append(shape)
        # Linhas: manter se ambos os pontos são necessários (não auxiliares)
        elif hasattr(shape, "start") and hasattr(shape, "end"):
            start_label = getattr(shape.start, "label", None)
            end_label = getattr(shape.end, "label", None)
            if (start_label and start_label in necessary_labels and
                end_label and end_label in necessary_labels):
                filtered.append(shape)
        # Triângulos: manter se todos os pontos são necessários
        elif hasattr(shape, "p1") and hasattr(shape, "p2") and hasattr(shape, "p3"):
            p1_label = getattr(shape.p1, "label", None)
            p2_label = getattr(shape.p2, "label", None)
            p3_label = getattr(shape.p3, "label", None)
            if (p1_label and p1_label in necessary_labels and
                p2_label and p2_label in necessary_labels and
                p3_label and p3_label in necessary_labels):
                filtered.append(shape)
        # Perpendiculares: sempre remover (são construções auxiliares)
        elif hasattr(shape, "perpendicular_line"):
            pass  # Não adicionar
        # Outros shapes sem labels: manter
        else:
            filtered.append(shape)
    
    env.shapes = filtered
    
    # Retornar contagem de auxiliares removidos
    aux_count = len(aux_labels)
    return aux_count
