# symbolic/ddar_adapter.py

import numpy as np
from ddar import DDAR
from parse import AGPoint, AGPredicate
from visual.environment import Point

def extract_points_from_env(env):
    """Extrai pontos do ambiente visual e retorna dicionário label -> AGPoint"""
    points_dict = {}
    for shape in env.shapes:
        if isinstance(shape, Point) and shape.label:
            points_dict[shape.label] = AGPoint(
                name=shape.label,
                value=np.array([shape.x, shape.y], dtype=float)
            )
    return points_dict

def fact_to_predicate(fact, points_dict):
    """
    Converte fato simbólico (tupla) para AGPredicate.
    fact: tupla, ex: ('cong', 'A', 'B', 'A', 'C')
    """
    pred_name = fact[0]
    args = fact[1:]
    
    # Converter strings de labels para AGPoints
    point_args = [points_dict[arg] if isinstance(arg, str) and arg in points_dict else arg 
                  for arg in args]
    
    # Separar pontos e constantes
    points = []
    constants = []
    for arg in point_args:
        if isinstance(arg, (int, float)):
            constants.append(arg)
        else:
            points.append(arg)
    
    return AGPredicate(name=pred_name, points=points, constants=constants)

class DDARAdapter:
    def __init__(self, points_dict):
        """
        points_dict: dicionário label -> AGPoint
        """
        self.points_dict = points_dict
        points_list = list(points_dict.values())
        self.ddar = DDAR(points_list)
        self.added_facts = []  # fatos adicionados como givens
        self.given_predicates = []  # AGPredicates dos givens
        
    def add_fact(self, fact):
        """
        fact: tupla simbólica, ex: ('cong', 'A', 'B', 'A', 'C')
        Converte para AGPredicate e força no DDAR.
        """
        self.added_facts.append(fact)
        try:
            pred = fact_to_predicate(fact, self.points_dict)
            self.ddar.force_pred(pred)
            self.given_predicates.append(pred)
        except Exception as e:
            # Se houver erro ao forçar (ex: pontos não numéricos), apenas armazena
            pass

    def run(self):
        """
        Executa a dedução closure no DDAR.
        """
        self.ddar.deduction_closure(verbose=False, progress_dot=False)

    def _predicate_equal(self, pred1, pred2):
        """Compara dois AGPredicates para igualdade."""
        if pred1.name != pred2.name:
            return False
        if pred1.constants != pred2.constants:
            return False
        if len(pred1.points) != len(pred2.points):
            return False
        # Comparar pontos por nome
        for p1, p2 in zip(pred1.points, pred2.points):
            if str(p1) != str(p2):  # Comparar por nome
                return False
        return True

    def _check_deduced_fact(self, fact):
        """
        Verifica se um fato foi deduzido pelo DDAR.
        Retorna True se o fato é verdadeiro e não está nos givens.
        """
        try:
            pred = fact_to_predicate(fact, self.points_dict)
            # Verificar se não está nos givens
            for given_pred in self.given_predicates:
                if self._predicate_equal(given_pred, pred):
                    return False
            # Verificar se foi deduzido
            result = self.ddar.check_pred(pred)
            return result
        except Exception as e:
            # Silenciosamente falhar - o fato pode não ser válido para esse estado
            return False

    def _generate_candidate_facts(self):
        """
        Gera candidatos para fatos deduzidos baseados nos pontos disponíveis.
        Retorna lista de tuplas (pred_name, args).
        
        eqangle(a1, a2, b1, b2, c1, c2, d1, d2) significa:
        ângulo entre direção (a1,a2) e (b1,b2) = ângulo entre (c1,c2) e (d1,d2)
        
        Para ângulo ∠ABC (vértice B, entre AB e BC):
        eqangle(A, B, B, C, ...) representa direção AB e direção BC
        """
        candidates = []
        points = list(self.points_dict.keys())
        
        # Gerar candidatos para eqangle (igualdade de ângulos)
        if len(points) >= 3:
            # Testar várias combinações de triplas
            for i, A in enumerate(points):
                for j, B in enumerate(points):
                    if i == j:
                        continue
                    for k, C in enumerate(points):
                        if k == i or k == j:
                            continue
                        # eqangle(A, B, B, C, A, C, C, B) - ∠ABC = ∠ACB
                        # (direção AB → BC) = (direção AC → CB)
                        candidates.append(("eqangle", A, B, B, C, A, C, C, B))
                        # eqangle(B, A, A, C, B, C, C, A) - ∠BAC = ∠BCA
                        candidates.append(("eqangle", B, A, A, C, B, C, C, A))
                        # eqangle(C, A, A, B, C, B, B, A) - ∠CAB = ∠CBA
                        candidates.append(("eqangle", C, A, A, B, C, B, B, A))
        
        return candidates

    def all_facts(self):
        """
        Retorna lista de fatos conhecidos (givens + deduzidos).
        Descobre fatos deduzidos testando candidatos.
        """
        all_known = list(self.added_facts)
        
        # Gerar e testar candidatos
        candidates = self._generate_candidate_facts()
        for candidate in candidates:
            if self._check_deduced_fact(candidate):
                # Evitar duplicatas
                if candidate not in all_known:
                    all_known.append(candidate)
        
        return all_known

    def get_proof(self, target_fact):
        """
        Retorna a prova mínima via traceback.
        Por enquanto, retorna lista vazia.
        TODO: implementar traceback real do DDAR
        """
        # TODO: implementar traceback real do DDAR
        # Por enquanto, se o fato foi deduzido, retornar os givens como "prova"
        if self._check_deduced_fact(target_fact):
            return self.added_facts.copy()
        return []
