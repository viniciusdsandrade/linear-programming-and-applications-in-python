import pulp  # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np  # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma empresa de transportes recebeu a proposta de transportar 600 funcionários de uma
# indústria para uma nova fábrica, de uma só vez.
#
# Recursos disponíveis:
#   - Ônibus grandes (G): até 8 disponíveis, cada um com 60 lugares, com custo de R$ 190,00 por viagem.
#   - Ônibus pequenos (P): até 12 disponíveis, cada um com 40 lugares, com custo de R$ 140,00 por viagem.
#   - Motoristas: somente 13 motoristas estão disponíveis, ou seja, a soma de ônibus usados (G + P)
#     não pode ultrapassar 13.
#
# Objetivo:
#   Minimizar o custo total do transporte, garantindo que pelo menos 600 funcionários sejam transportados.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   xG = número de ônibus grandes a serem usados (variável inteira, 0 <= xG <= 8)
#   xP = número de ônibus pequenos a serem usados (variável inteira, 0 <= xP <= 12)
#
# Função objetivo (Minimizar o custo):
#   Min Z = 190 * xG + 140 * xP
#
# Restrições:
#   1) Capacidade total: 60 * xG + 40 * xP >= 600   (para transportar pelo menos 600 pessoas)
#   2) Limite de ônibus grandes: xG <= 8
#   3) Limite de ônibus pequenos: xP <= 12
#   4) Limite de motoristas: xG + xP <= 13
#   5) Não negatividade e integridade: xG, xP inteiros e >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Minimização)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exemplo_09", pulp.LpMinimize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# xG: número de ônibus grandes a serem usados (tipo inteiro)
# xP: número de ônibus pequenos a serem usados (tipo inteiro)
xG = pulp.LpVariable('Onibus_Grande', lowBound=0, cat='Integer')
xP = pulp.LpVariable('Onibus_Pequeno', lowBound=0, cat='Integer')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# Min Z = 190 * xG + 140 * xP
model += 190 * xG + 140 * xP, "Custo_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# (1) Capacidade: 60*xG + 40*xP >= 600 (garante o transporte de pelo menos 600 funcionários)
model += 60 * xG + 40 * xP >= 600, "Capacidade_Total"

# (2) Limite de ônibus grandes: xG <= 8
model += xG <= 8, "Max_Onibus_Grandes"

# (3) Limite de ônibus pequenos: xP <= 12
model += xP <= 12, "Max_Onibus_Pequenos"

# (4) Limite de motoristas: xG + xP <= 13
model += xG + xP <= 13, "Max_Motoristas"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("xG (Ônibus Grandes) =", xG.varValue)
print("xP (Ônibus Pequenos) =", xP.varValue)
print("Custo Mínimo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Como as variáveis são inteiras, a região factível real é discreta, mas para visualização
# utilizamos uma aproximação contínua das restrições.
#
# Definimos um grid para xG (0 a 8) e xP (0 a 12) para plotar as fronteiras das restrições.
xG_vals = np.linspace(0, 8, 200)  # Valores contínuos para xG de 0 a 8
xP_vals = np.linspace(0, 12, 200)  # Valores contínuos para xP de 0 a 12

# Calculando as fronteiras:
# 1) Capacidade: 60*xG + 40*xP = 600 => xP = (600 - 60*xG)/40 = 15 - 1.5*xG
xP_capacidade = 15 - 1.5 * xG_vals

# 2) Motoristas: xG + xP = 13 => xP = 13 - xG
xP_motoristas = 13 - xG_vals

# As restrições xG <= 8 e xP <= 12 são limites verticais/horizontais.
#
# A região factível deve satisfazer:
#   - xP >= (15 - 1.5*xG)   [capacidade, pois 60*xG+40*xP>=600]
#   - xP <= (13 - xG)       [motoristas, pois xG+xP<=13]
#   - xG <= 8 e xP <= 12
#   - xG >= 0, xP >= 0
#
# Para preenchimento, para cada xG calculamos os limites inferiores e superiores para xP:
xP_feasible_min = np.maximum(15 - 1.5 * xG_vals, 0)  # xP deve ser maior ou igual a essa fronteira e não negativo
xP_feasible_max = np.minimum(13 - xG_vals, 12)  # xP deve ser menor ou igual a essa fronteira e não ultrapassar 12

# Montar o polígono da região factível
feasible_upper = []
feasible_lower = []
for i, xg in enumerate(xG_vals):
    lower = xP_feasible_min[i]
    upper = xP_feasible_max[i]
    if lower <= upper:
        feasible_lower.append(lower)
        feasible_upper.append(upper)
    else:
        feasible_lower.append(np.nan)
        feasible_upper.append(np.nan)

feasible_lower = np.array(feasible_lower)
feasible_upper = np.array(feasible_upper)

# Criação da figura
plt.figure(figsize=(8, 6))

# Plot das fronteiras:
plt.plot(xG_vals, xP_capacidade, label='60xG + 40xP = 600', color='blue')
plt.plot(xG_vals, xP_motoristas, label='xG + xP = 13', color='green')
plt.axvline(x=8, color='red', label='xG = 8')
plt.axhline(y=12, color='orange', label='xP = 12')

# Preencher a região factível
plt.fill_between(xG_vals, feasible_lower, feasible_upper, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada
plt.scatter(xG.varValue, xP.varValue, color='black', zorder=5, label='Solução Ótima')

# Configurar os eixos e rótulos
plt.xlim(0, 8.5)
plt.ylim(0, 12.5)
plt.xlabel('xG (Ônibus Grandes)')
plt.ylabel('xP (Ônibus Pequenos)')
plt.title('Região Factível (Exemplo 09) e Solução Ótima (Minimização do Custo)')
plt.legend()
plt.grid(True)

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 2D no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
# com o nome 'exercise09.png'.
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise09.png')

# Exibir o gráfico na tela
plt.show()
