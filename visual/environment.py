import math
from typing import List, Tuple, Union

class Point:
    def __init__(self, x: float, y: float, label: str = ""):
        self.x = x
        self.y = y
        self.label = label
    
    def to_svg(self) -> str:
        svg = f'<circle cx="{self.x}" cy="{self.y}" r="2" fill="black"/>'
        if self.label:
            svg += f'\n  <text x="{self.x + 5}" y="{self.y - 5}" font-family="Arial" font-size="12" fill="black">{self.label}</text>'
        return svg

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    
    def to_svg(self) -> str:
        return f'<line x1="{self.start.x}" y1="{self.start.y}" x2="{self.end.x}" y2="{self.end.y}" stroke="black" stroke-width="1"/>'

class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius
    
    def to_svg(self) -> str:
        return f'<circle cx="{self.center.x}" cy="{self.center.y}" r="{self.radius}" fill="none" stroke="black" stroke-width="1"/>'

class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def to_svg(self) -> str:
        points = f"{self.p1.x},{self.p1.y} {self.p2.x},{self.p2.y} {self.p3.x},{self.p3.y}"
        return f'<polygon points="{points}" fill="none" stroke="black" stroke-width="1"/>'

class Angle:
    def __init__(self, vertex: Point, point1: Point, point2: Point, radius: float = 20, color: str = "blue", label: str = ""):
        self.vertex = vertex
        self.point1 = point1
        self.point2 = point2
        self.radius = radius
        self.color = color
        self.label = label
    
    def _calculate_angle(self, p1: Point, vertex: Point, p2: Point) -> float:
        """Calcula o ângulo em radianos entre três pontos"""
        # Vetores do vértice para os outros pontos
        v1_x = p1.x - vertex.x
        v1_y = p1.y - vertex.y
        v2_x = p2.x - vertex.x
        v2_y = p2.y - vertex.y
        
        # Ângulos dos vetores
        angle1 = math.atan2(v1_y, v1_x)
        angle2 = math.atan2(v2_y, v2_x)
        
        return angle1, angle2
    
    def to_svg(self) -> str:
        angle1, angle2 = self._calculate_angle(self.point1, self.vertex, self.point2)
        
        # Garantir que o arco seja desenhado no sentido correto
        start_angle = angle1
        end_angle = angle2
        
        # Ajustar para o menor arco
        diff = end_angle - start_angle
        if diff > math.pi:
            end_angle -= 2 * math.pi
        elif diff < -math.pi:
            end_angle += 2 * math.pi
        
        # Converter para graus
        start_degrees = math.degrees(start_angle)
        end_degrees = math.degrees(end_angle)
        
        # Pontos do arco
        start_x = self.vertex.x + self.radius * math.cos(start_angle)
        start_y = self.vertex.y + self.radius * math.sin(start_angle)
        end_x = self.vertex.x + self.radius * math.cos(end_angle)
        end_y = self.vertex.y + self.radius * math.sin(end_angle)
        
        # Determinar se é um arco grande
        large_arc = 1 if abs(end_angle - start_angle) > math.pi else 0
        sweep = 1 if end_angle > start_angle else 0
        
        svg = f'<path d="M {start_x:.2f} {start_y:.2f} A {self.radius} {self.radius} 0 {large_arc} {sweep} {end_x:.2f} {end_y:.2f}" '
        svg += f'fill="none" stroke="{self.color}" stroke-width="1.5"/>'
        
        # Adicionar label se fornecido
        if self.label:
            # Posição do label no meio do arco
            mid_angle = (start_angle + end_angle) / 2
            label_radius = self.radius + 10
            label_x = self.vertex.x + label_radius * math.cos(mid_angle)
            label_y = self.vertex.y + label_radius * math.sin(mid_angle)
            svg += f'\n  <text x="{label_x:.2f}" y="{label_y:.2f}" font-family="Arial" font-size="10" fill="{self.color}" text-anchor="middle">{self.label}</text>'
        
        return svg

class Perpendicular:
    def __init__(self, triangle: Triangle, vertex: Point):
        self.triangle = triangle
        self.vertex = vertex
        self.perpendicular_line = self._calculate_perpendicular()
    
    def _calculate_perpendicular(self) -> Line:
        # Encontrar o lado oposto ao vértice
        if self.vertex == self.triangle.p1:
            opposite_start = self.triangle.p2
            opposite_end = self.triangle.p3
        elif self.vertex == self.triangle.p2:
            opposite_start = self.triangle.p1
            opposite_end = self.triangle.p3
        else:  # self.vertex == self.triangle.p3
            opposite_start = self.triangle.p1
            opposite_end = self.triangle.p2
        
        # Calcular o ponto médio do lado oposto
        mid_x = (opposite_start.x + opposite_end.x) / 2
        mid_y = (opposite_start.y + opposite_end.y) / 2
        mid_point = Point(mid_x, mid_y)
        
        return Line(self.vertex, mid_point)
    
    def to_svg(self) -> str:
        return f'<line x1="{self.perpendicular_line.start.x}" y1="{self.perpendicular_line.start.y}" x2="{self.perpendicular_line.end.x}" y2="{self.perpendicular_line.end.y}" stroke="red" stroke-width="1" stroke-dasharray="5,5"/>'

class Environment:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.shapes: List[Union[Point, Line, Circle, Triangle, Perpendicular, Angle]] = []
    
    def add_point(self, x: float, y: float, label: str = "") -> Point:
        point = Point(x, y, label)
        self.shapes.append(point)
        return point
    
    def add_line(self, start: Point, end: Point) -> Line:
        line = Line(start, end)
        self.shapes.append(line)
        return line
    
    def add_circle(self, center: Point, radius: float) -> Circle:
        circle = Circle(center, radius)
        self.shapes.append(circle)
        return circle
    
    def add_triangle(self, p1: Point, p2: Point, p3: Point) -> Triangle:
        triangle = Triangle(p1, p2, p3)
        self.shapes.append(triangle)
        return triangle
    
    def add_angle(self, vertex: Point, point1: Point, point2: Point, radius: float = 20, color: str = "blue", label: str = "") -> Angle:
        angle = Angle(vertex, point1, point2, radius, color, label)
        self.shapes.append(angle)
        return angle
    
    def add_perpendicular(self, triangle: Triangle, vertex: Point) -> Perpendicular:
        perpendicular = Perpendicular(triangle, vertex)
        self.shapes.append(perpendicular)
        return perpendicular
    
    def generate_svg(self) -> str:
        svg_content = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n'
        
        for shape in self.shapes:
            svg_content += f"  {shape.to_svg()}\n"
        
        svg_content += '</svg>'
        return svg_content
    
    def save_svg(self, filename: str):
        with open(filename, 'w') as f:
            f.write(self.generate_svg())
    
    def clone(self):
        """
        Cria uma cópia profunda do Environment.
        Retorna novo Environment com shapes independentes.
        """
        import copy
        return copy.deepcopy(self)

# Demonstração: Triângulo isósceles ABC com AB=AC
# # Prova que ângulo ABC = ângulo BCA

# print("PROVA: Em um triângulo isósceles ABC com AB=AC, os ângulos da base são iguais (∠ABC = ∠BCA)")
# print("=" * 80)

# # Configuração do ambiente
# env = Environment(400, 300)

# # Passo 1: Construir o triângulo isósceles ABC
# print("\nPasso 1: Construindo o triângulo isósceles ABC onde AB = AC")

# # Definindo os pontos para formar um triângulo isósceles
# # A no topo, B e C na base, com AB = AC
# A = env.add_point(200, 50, "A")   # Vértice superior
# B = env.add_point(100, 200, "B")  # Vértice inferior esquerdo
# C = env.add_point(300, 200, "C")  # Vértice inferior direito

# # Verificando que AB = AC (distâncias iguais)
# dist_AB = math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
# dist_AC = math.sqrt((A.x - C.x)**2 + (A.y - C.y)**2)
# print(f"Distância AB = {dist_AB:.2f}")
# print(f"Distância AC = {dist_AC:.2f}")
# print(f"Confirmado: AB = AC (triângulo isósceles)")

# # Adicionando o triângulo
# triangle = env.add_triangle(A, B, C)

# # Adicionando os ângulos da base para visualização
# env.add_angle(B, A, C, radius=25, color="green", label="∠ABC")
# env.add_angle(C, B, A, radius=25, color="green", label="∠BCA")
# env.add_angle(A, B, C, radius=30, color="orange", label="∠BAC")

# print("\nPasso 2: Adicionando a mediatriz do vértice A ao meio da base BC")

# # Passo 2: Adicionar mediatriz de A ao ponto médio de BC
# env.add_perpendicular(triangle, A)

# # Calculando o ponto médio de BC para referência
# mid_BC_x = (B.x + C.x) / 2
# mid_BC_y = (B.y + C.y) / 2
# mid_BC = env.add_point(mid_BC_x, mid_BC_y, "M")

# print(f"Ponto médio M de BC: ({mid_BC_x}, {mid_BC_y})")
# print("A mediatriz AM (linha vermelha tracejada) divide o triângulo em dois triângulos congruentes:")
# print("- Triângulo ABM ≅ Triângulo ACM")
# print("- Isso ocorre porque:")
# print("  * AB = AC (dado - lados iguais)")
# print("  * AM = AM (lado comum)")
# print("  * BM = CM (M é ponto médio de BC)")
# print("- Pela congruência LLL, os triângulos são congruentes")
# print("- Portanto: ∠ABM = ∠ACM, ou seja, ∠ABC = ∠BCA")
# print("- Os ângulos verdes mostram que ∠ABC = ∠BCA (ângulos da base iguais)")

# # Gerando e exibindo o SVG
# svg_output = env.generate_svg()
# print(f"\nSVG gerado com {len(env.shapes)} elementos geométricos:")
# print(svg_output)

# print("\nCONCLUSÃO: A mediatriz do vértice A ao ponto médio da base BC demonstra")
# print("que os ângulos da base de um triângulo isósceles são iguais. ∎")
