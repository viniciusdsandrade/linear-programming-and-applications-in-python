import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Um fabricante produz dois tipos de produtos:
#   Produto 1: Lucro R$2,00/unidade, 3 horas de máquina/unidade, 9 unidades de matéria-prima/unidade.
#   Produto 2: Lucro R$5,00/unidade, 4 horas de máquina/unidade, 7 unidades de matéria-prima/unidade.
#
# Recursos disponíveis:
#   - Horas de máquina: 200 horas
#   - Matéria-prima: 300 unidades
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de unidades do produto1 a produzir
#   y = número de unidades do produto2 a produzir
#
# Função objetivo:
#   Max Z = 2*x + 5*y
#
# Restrições:
#   a) Horas de máquina: 3*x + 4*y <= 200
#   b) Matéria-prima:     9*x + 7*y <= 300
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Lucro)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio3_Maximizar_Lucro", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable('Produto1', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Produto2', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 2 * x + 5 * y, "Lucro_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Horas de máquina:
model += 3 * x + 4 * y <= 200, "Restricao_Horas_Maquina"

# Matéria-prima:
model += 9 * x + 7 * y <= 300, "Restricao_Materia_Prima"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Unidades do Produto1 =", x.varValue)
print("Número de Unidades do Produto2 =", y.varValue)
print("Lucro Máximo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a visualização, usamos x no eixo X e y no eixo Y.
# As restrições são:
# (1) Horas de máquina:   3*x + 4*y <= 200  --> y <= (200 - 3*x)/4
# (2) Matéria-prima:       9*x + 7*y <= 300  --> y <= (300 - 9*x)/7

x_vals = np.linspace(0, 100, 300)
y_maquina = (200 - 3 * x_vals) / 4
y_materia = (300 - 9 * x_vals) / 7

# Para cada valor de x, o limite superior de y é o menor entre as duas restrições:
y_feasible = np.minimum(y_maquina, y_materia)
y_feasible = np.maximum(y_feasible, 0)  # Garantir que y não seja negativo

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_maquina, label='3x + 4y = 200 (Horas de Máquina)')
plt.plot(x_vals, y_materia, label='9x + 7y = 300 (Matéria-Prima)')
plt.fill_between(x_vals, 0, y_feasible, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, max(x_vals))
plt.ylim(0, max(y_feasible))
plt.xlabel('Unidades do Produto1 (x)')
plt.ylabel('Unidades do Produto2 (y)')
plt.title('Exercício 3 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q3\exercise3.png')

plt.show()
