# [RESUMO DO PROBLEMA]
# Uma empresa de transportes precisa levar 600 funcionários de uma só vez.
#
#   - Possui até 8 ônibus grandes (G), cada um com 60 lugares e custo R$ 190/viagem
#   - Possui até 12 ônibus pequenos (P), cada um com 40 lugares e custo R$ 140/viagem
#   - Há um total de 13 motoristas disponíveis (ou seja, xG + xP <= 13).
#   - Precisamos transportar exatamente (ou no mínimo) 600 funcionários.
#
# OBJETIVO: Minimizar o custo total de transporte.
#
# [MODELO DE PROGRAMAÇÃO LINEAR]
# Variáveis de decisão:
#   xG = número de ônibus grandes a serem usados
#   xP = número de ônibus pequenos a serem usados
#
# Função Objetivo (Minimizar custo):
#   Min Z = 190*xG + 140*xP
#
# Restrições:
#   1) Capacidade total ≥ 600 passageiros:    60*xG + 40*xP >= 600
#   2) Limite de ônibus grandes:             xG <= 8
#   3) Limite de ônibus pequenos:            xP <= 12
#   4) Limite de motoristas:                 xG + xP <= 13
#   5) xG >= 0, xP >= 0
#   6) xG e xP inteiros (faz sentido ser inteiro, pois não podemos usar "meio ônibus")

# [CÓDIGO COMPLETO EM PYTHON + PLOTAGEM 2D]

# Se estiver em ambiente local e precisar instalar:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1) Definir o problema (Minimização)
model = pulp.LpProblem("Exemplo_09", pulp.LpMinimize)

# 2) Criar variáveis
#    Normalmente, queremos xG e xP como inteiros (Integer), pois não se usam frações de ônibus.
#    Caso o solver seja demorado ou não seja crucial, podemos usar cat='Continuous'
#    só pra demonstração. Mas o ideal aqui é cat='Integer'.
xG = pulp.LpVariable('Onibus_Grande', lowBound=0, cat='Integer')
xP = pulp.LpVariable('Onibus_Pequeno', lowBound=0, cat='Integer')

# 3) Função objetivo: Minimizar custo
model += 190*xG + 140*xP, "Custo"

# 4) Restrições
model += 60*xG + 40*xP >= 600, "Capacidade"   # transportar 600 pessoas
model += xG <= 8,              "MaxOnibusG"
model += xP <= 12,             "MaxOnibusP"
model += xG + xP <= 13,        "MaxMotoristas"

# 5) Resolver o modelo
model.solve()

# 6) Mostrar resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print("xG (Ônibus Grandes) =", xG.varValue)
print("xP (Ônibus Pequenos) =", xP.varValue)
print("Custo Mínimo = R$", pulp.value(model.objective))

# 7) Plotar a região factível em 2D (trabalharemos como se fossem contínuos para ver o polígono).
#    Para mostrar a solução (xG, xP) encontrada. A região ainda é discreta por xG, xP inteiros,
#    mas podemos exibir o polígono das restrições e ver onde ficam os pontos inteiros.

# Construir um grid para xG e xP
xG_vals = np.linspace(0, 8, 200)   # entre 0 e 8
xP_vals = np.linspace(0, 12, 200)  # entre 0 e 12

# Vamos identificar as retas de fronteira:

# 1) 60*xG + 40*xP = 600 => xP = (600 - 60*xG)/40 = 15 - 1.5*xG
#    mas a restrição é >= 600 => xP >= 15 - 1.5*xG
xP_cap = 15 - 1.5*xG_vals  # (fronteira)

# 2) xG + xP = 13 => xP = 13 - xG
xP_motoristas = 13 - xG_vals

# 3) xG <= 8 => vertical
# 4) xP <= 12 => horizontal

# Para "preencher" a região, precisamos achar o polígono de interseção
# Lembremos:
#   xG >= 0
#   xP >= 0
#   xG <= 8
#   xP <= 12
#   xG + xP <= 13 -> xP <= 13 - xG
#   60*xG + 40*xP >= 600 -> xP >= 15 - 1.5*xG

# Vamos construir a curva de xP_cap e recortar acima de 0 e xP>=0 etc.

plt.figure(figsize=(8,6))

# Plot da fronteira 60*xG + 40*xP = 600
plt.plot(xG_vals, xP_cap, label='60xG + 40xP = 600', color='blue')

# Plot da fronteira xG + xP = 13
plt.plot(xG_vals, xP_motoristas, label='xG + xP = 13', color='green')

# As linhas xG=8 e xP=12 são fronteiras verticais/horizontais
plt.axvline(x=8, color='red', label='xG = 8')
plt.axhline(y=12, color='orange', label='xP = 12')

# Precisamos preencher a região factível.
# A região factível deve satisfazer simultaneamente:
#   xP >= 15 - 1.5*xG  (capacidade)
#   xP <= 13 - xG      (motoristas)
#   0 <= xG <= 8
#   0 <= xP <= 12

# Para cada xG no array, calculamos o min e max de xP permitido.
xP_feasible_min = np.maximum(15 - 1.5*xG_vals, 0)             # pois xP >= 0 e >= 15 -1.5xG
xP_feasible_max = np.minimum(13 - xG_vals, 12)                # pois xP <= (13-xG) e <=12
# Precisamos também que xP_feasible_max >= xP_feasible_min
# E xG até 8 (o array já respeita xG_vals até 8)
# Se xP_feasible_max < xP_feasible_min => inviável

# Montar a "faixa" e preencher
feasible_upper = []
feasible_lower = []
for i, xg in enumerate(xG_vals):
    y_lower = xP_feasible_min[i]
    y_upper = xP_feasible_max[i]
    if y_lower <= y_upper:
        feasible_upper.append(y_upper)
        feasible_lower.append(y_lower)
    else:
        feasible_upper.append(np.nan)
        feasible_lower.append(np.nan)

feasible_upper = np.array(feasible_upper)
feasible_lower = np.array(feasible_lower)

plt.fill_between(xG_vals, feasible_lower, feasible_upper, color='gray', alpha=0.3,
                 label='Região Factível')

# Marcar a solução ótima
plt.scatter(xG.varValue, xP.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 8.5)
plt.ylim(0, 12.5)
plt.xlabel('xG (Quantidade de ônibus grandes)')
plt.ylabel('xP (Quantidade de ônibus pequenos)')
plt.title('Exemplo 09 - Região Factível e Solução Ótima (Min. Custo)')
plt.legend()
plt.grid(True)
plt.show()
