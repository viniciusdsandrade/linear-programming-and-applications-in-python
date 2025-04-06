import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# O sapateiro busca maximizar seu lucro por hora.
#
# Lucros:
#   - Sapato: 5 unidades monetárias por unidade.
#   - Cinto:  2 unidades monetárias por unidade.
#
# Restrições:
#   a) Couro: 2 unidades por sapato e 1 por cinto, total disponível 6 unidades:
#         2*x + y <= 6
#   b) Capacidade de produção:
#         - Máximo de 6 sapatos por hora: x <= 6
#         - Máximo de 5 cintos por hora:   y <= 5
#
# Variáveis de decisão:
#   x = número de sapatos produzidos por hora.
#   y = número de cintos produzidos por hora.
#
# Função Objetivo:
#   Maximizar Z = 5*x + 2*y
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Lucro por Hora)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio8_Maximizar_Lucro", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable("Sapatos", lowBound=0, cat="Continuous")
y = pulp.LpVariable("Cintos", lowBound=0, cat="Continuous")

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 5 * x + 2 * y, "Lucro_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
model += 2 * x + y <= 6, "Restricao_Couro"    # Consumo de couro
model += x <= 6, "Restricao_Sapatos"            # Capacidade máxima de sapatos
model += y <= 5, "Restricao_Cintos"             # Capacidade máxima de cintos

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Sapatos por hora =", x.varValue)
print("Número de Cintos por hora =", y.varValue)
print("Lucro Máximo por hora =", pulp.value(model.objective))

# =============================================================================
# 6) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para visualização, usamos x no eixo X e y no eixo Y.
#
# Restrição do couro: 2*x + y <= 6  -->  y <= 6 - 2*x
# Limites de produção: x <= 6 e y <= 5

x_vals = np.linspace(0, 6, 300)
y_couro = 6 - 2 * x_vals

# O limite superior para y é o mínimo entre a restrição do couro e o limite de cintos (y <= 5)
y_feasible = np.minimum(y_couro, 5)
y_feasible = np.maximum(y_feasible, 0)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_couro, label='2x + y = 6 (Couro)')
plt.axhline(5, color='red', linestyle='--', label='y = 5 (Máx de cintos)')
plt.fill_between(x_vals, 0, y_feasible, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 6)
plt.ylim(0, 6)
plt.xlabel('Sapatos (x)')
plt.ylabel('Cintos (y)')
plt.title('Exercício 8 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# Salvar o gráfico no diretório especificado
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q8\exercise8.png')
plt.show()
