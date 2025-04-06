import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma fábrica de utensílios de cozinha fabrica:
#   • Panelas de pressão, com lucro de R$3,00 por unidade.
#   • Frigideiras, com lucro de R$4,00 por unidade.
#
# Cada item necessita de 1 hora de moldagem e há no máximo 6 horas de trabalho por dia.
# A demanda de mercado permite produzir, no máximo, 4 unidades de cada item por dia.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de panelas de pressão produzidas por dia.
#   y = número de frigideiras produzidas por dia.
#
# Função Objetivo:
#   Maximizar Z = 3*x + 4*y
#
# Restrições:
#   1) Tempo de moldagem: x + y <= 6
#   2) Demanda de mercado: x <= 4 e y <= 4
#   3) Não negatividade: x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Lucro)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio10_Maximizar_Lucro", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable("Panelas", lowBound=0, cat="Continuous")
y = pulp.LpVariable("Frigideiras", lowBound=0, cat="Continuous")

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 3 * x + 4 * y, "Lucro_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
model += x + y <= 6, "Restricao_Tempo"  # Tempo de moldagem
model += x <= 4, "Restricao_Panelas"      # Demanda de panelas
model += y <= 4, "Restricao_Frigideiras"   # Demanda de frigideiras

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Panelas de Pressão =", x.varValue)
print("Número de Frigideiras =", y.varValue)
print("Lucro Máximo =", pulp.value(model.objective))

# =============================================================================
# 6) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# A região factível é definida por:
#   • x + y <= 6   (linha: y = 6 - x)
#   • x <= 4       (linha vertical: x = 4)
#   • y <= 4       (linha horizontal: y = 4)

x_vals = np.linspace(0, 6, 300)
y_tempo = 6 - x_vals         # Representa a reta x + y = 6
y_limite = np.full_like(x_vals, 4)  # y = 4

# A região factível para y é o mínimo entre a restrição do tempo e o limite de mercado para y:
y_feasible = np.minimum(y_tempo, y_limite)
y_feasible = np.maximum(y_feasible, 0)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_tempo, label='x + y = 6 (Tempo de Moldagem)')
plt.axhline(4, color='red', linestyle='--', label='y = 4 (Máx Frigideiras)')
plt.axvline(4, color='green', linestyle='--', label='x = 4 (Máx Panelas)')
plt.fill_between(x_vals, 0, y_feasible, color='gray', alpha=0.3, label='Região Factível')
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 6)
plt.ylim(0, 6)
plt.xlabel('Panelas de Pressão (x)')
plt.ylabel('Frigideiras (y)')
plt.title('Exercício 10 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# Salvar o gráfico no diretório especificado
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q10\exercise10.png')
plt.show()