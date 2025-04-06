import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# A empresa Have Fun S/A deseja minimizar o custo de produção por lata de bebida
# energética, determinando quantas doses de duas soluções devem ser utilizadas.
#
# Solução Red:
#   - Contribui com 8 g de extrato de guaraná e 1 g de cafeína por dose.
#   - Custa R$0,06 por dose.
#
# Solução Blue:
#   - Contribui com 6 g de extrato de guaraná e 2 g de cafeína por dose.
#   - Custa R$0,08 por dose.
#
# Restrições:
#   - Extrato de guaraná: 8*x + 6*y >= 48 (mínimo de 48 g)
#   - Cafeína (mínimo):    x + 2*y >= 12 (mínimo de 12 g)
#   - Cafeína (máximo):     x + 2*y <= 20 (máximo de 20 g)
#
# Variáveis de decisão:
#   x = número de doses da solução Red por lata.
#   y = número de doses da solução Blue por lata.
#
# Função Objetivo:
#   Minimizar C = 0.06*x + 0.08*y
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Minimização do Custo)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio7_Minimizar_Custo", pulp.LpMinimize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable('Solucao_Red', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Solucao_Blue', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 0.06 * x + 0.08 * y, "Custo_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de extrato de guaraná:
model += 8 * x + 6 * y >= 48, "Restricao_Guarana"

# Restrição de cafeína (mínimo):
model += x + 2 * y >= 12, "Restricao_Cafeina_Min"

# Restrição de cafeína (máximo):
model += x + 2 * y <= 20, "Restricao_Cafeina_Max"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de doses da Solução Red (x) =", x.varValue)
print("Número de doses da Solução Blue (y) =", y.varValue)
print("Custo Mínimo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a visualização, usamos x (doses de Red) no eixo X e y (doses de Blue) no eixo Y.
# As restrições são:
# (1) Extrato de Guaraná: 8*x + 6*y >= 48  --> y >= (48 - 8*x)/6
# (2) Cafeína (mínimo):    x + 2*y >= 12    --> y >= (12 - x)/2
# (3) Cafeína (máximo):     x + 2*y <= 20    --> y <= (20 - x)/2

x_vals = np.linspace(0, 10, 300)
y_guarana = (48 - 8 * x_vals) / 6
y_cafeina_min = (12 - x_vals) / 2
y_cafeina_max = (20 - x_vals) / 2

# Para cada valor de x, o limite inferior efetivo para y é o máximo entre as restrições mínimas
y_lower = np.maximum(y_guarana, y_cafeina_min)
# O limite superior para y é a restrição do máximo de cafeína
y_upper = y_cafeina_max

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_guarana, label='8x + 6y = 48 (Guaraná)')
plt.plot(x_vals, y_cafeina_min, label='x + 2y = 12 (Cafeína Mínima)')
plt.plot(x_vals, y_cafeina_max, label='x + 2y = 20 (Cafeína Máxima)')

# Preencher a região factível (entre os limites inferior e superior)
plt.fill_between(x_vals, y_lower, y_upper, where=(y_lower <= y_upper),
                 color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('Doses da Solução Red (x)')
plt.ylabel('Doses da Solução Blue (y)')
plt.title('Exercício 7 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# Salvar o gráfico no diretório especificado
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q7\exercise7.png')

plt.show()
