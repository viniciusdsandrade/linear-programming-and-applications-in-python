import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma rede de televisão local deseja maximizar o número total de telespectadores
# exibindo dois programas:
#
# Programa A:
#   - 20 minutos de música, 1 minuto de propaganda, 30.000 telespectadores por exibição.
#
# Programa B:
#   - 10 minutos de música, 1 minuto de propaganda, 10.000 telespectadores por exibição.
#
# Restrições:
#   - Propaganda: cada exibição (A ou B) tem 1 minuto de propaganda, totalizando x+y minutos,
#         e deve haver no mínimo 5 minutos por semana: x + y >= 5.
#   - Música: 20*x + 10*y <= 80 minutos, ou, simplificando: 2*x + y <= 8.
#
# Variáveis de decisão:
#   x = número de vezes por semana que o programa A é exibido.
#   y = número de vezes por semana que o programa B é exibido.
#
# Função Objetivo:
#   Maximizar Z = 30000*x + 10000*y
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização dos Telespectadores)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio9_Maximizar_Telespectadores", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable("Programa_A", lowBound=0, cat="Continuous")
y = pulp.LpVariable("Programa_B", lowBound=0, cat="Continuous")

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 30000 * x + 10000 * y, "Total_Telespectadores"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de propaganda: x + y >= 5
model += x + y >= 5, "Restricao_Propaganda"

# Restrição de música: 2*x + y <= 8
model += 2 * x + y <= 8, "Restricao_Musica"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

print("Status da Solução:", pulp.LpStatus[model.status])
print("Programa A deve ser exibido =", x.varValue, "vezes por semana")
print("Programa B deve ser exibido =", y.varValue, "vezes por semana")
print("Número máximo de telespectadores =", pulp.value(model.objective))

# =============================================================================
# 6) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a visualização, usamos x no eixo X e y no eixo Y.
#
# As restrições são:
# (1) Propaganda: x + y >= 5  --> y >= 5 - x
# (2) Música:     2*x + y <= 8 --> y <= 8 - 2*x

x_vals = np.linspace(0, 10, 300)
y_propaganda = 5 - x_vals
y_musica = 8 - 2 * x_vals

# A região factível é delimitada por y >= (5 - x) e y <= (8 - 2*x)
y_lower = np.maximum(5 - x_vals, 0)
y_upper = 8 - 2 * x_vals

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_propaganda, label='x + y = 5 (Propaganda)')
plt.plot(x_vals, y_musica, label='2x + y = 8 (Música)')
plt.fill_between(x_vals, y_lower, y_upper, where=(y_lower <= y_upper), color='gray', alpha=0.3, label='Região Factível')

plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('Programa A (x)')
plt.ylabel('Programa B (y)')
plt.title('Exercício 9 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# Salvar o gráfico no diretório especificado
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q9\exercise9.png')
plt.show()