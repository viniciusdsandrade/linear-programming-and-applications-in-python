import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# A Esportes Radicais S/A produz paraquedas e asa-deltas em duas linhas de montagem:
#
# Linha de montagem 1:
#   - Cada produto (paraquedas ou asa-delta) requer 10 horas.
#   - Total disponível: 100 horas.
#
# Linha de montagem 2:
#   - Paraquedas requer 3 horas.
#   - Asa-delta requer 7 horas.
#   - Total disponível: 42 horas.
#
# Lucros:
#   - Paraquedas: R$60,00 por unidade.
#   - Asa-delta: R$40,00 por unidade.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de paraquedas a produzir.
#   y = número de asa-deltas a produzir.
#
# Função objetivo:
#   Max Z = 60*x + 40*y
#
# Restrições:
#   a) Linha de montagem 1:
#         10*x + 10*y <= 100
#
#   b) Linha de montagem 2:
#         3*x + 7*y <= 42
#
# Não negatividade:
#         x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Lucro)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio5_Maximizar_Lucro", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable('Paraquedas', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Asa_Delta', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 60 * x + 40 * y, "Lucro_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Linha de montagem 1: 10*x + 10*y <= 100
model += 10 * x + 10 * y <= 100, "Restricao_Linha1"

# Linha de montagem 2: 3*x + 7*y <= 42
model += 3 * x + 7 * y <= 42, "Restricao_Linha2"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Paraquedas a produzir =", x.varValue)
print("Número de Asa-Deltas a produzir =", y.varValue)
print("Lucro Máximo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a visualização, usamos x (paraquedas) no eixo X e y (asa-deltas) no eixo Y.
# As restrições são:
# (1) Linha de montagem 1: 10*x + 10*y <= 100  --> y <= (100 - 10*x)/10 = 10 - x
# (2) Linha de montagem 2: 3*x + 7*y <= 42     --> y <= (42 - 3*x)/7

x_vals = np.linspace(0, 15, 300)
y_linha1 = 10 - x_vals
y_linha2 = (42 - 3 * x_vals) / 7

# Para cada valor de x, o limite superior de y é o menor valor entre as duas restrições:
y_feasible = np.minimum(y_linha1, y_linha2)
y_feasible = np.maximum(y_feasible, 0)  # Assegurando que y não seja negativo

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_linha1, label='10x + 10y = 100 (Linha 1)')
plt.plot(x_vals, y_linha2, label='3x + 7y = 42 (Linha 2)')
plt.fill_between(x_vals, 0, y_feasible, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, max(x_vals))
plt.ylim(0, max(y_feasible)+1)
plt.xlabel('Número de Paraquedas (x)')
plt.ylabel('Número de Asa-Deltas (y)')
plt.title('Exercício 5 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# Salvar o gráfico no caminho especificado
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q5\exercise5.png')
plt.show()
