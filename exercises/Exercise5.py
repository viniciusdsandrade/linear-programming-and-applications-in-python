# [RESUMO DO PROBLEMA]
# A empresa Óleos Unidos S.A. produz três tipos de combustíveis (A, B e C)
# usando dois insumos: extrato mineral e solvente, sem perdas no processo.
#
# Da tabela de proporções (por "lote" ou unidade de combustível):
#   Combustível A: 8 L de extrato mineral + 5 L de solvente (total = 13 L do combustível A)
#   Combustível B: 5 L de extrato mineral + 4 L de solvente (total = 9 L do combustível B)
#   Combustível C: 4 L de extrato mineral + 2 L de solvente (total = 6 L do combustível C)
#
# Disponibilidade:
#   - 120 L de extrato mineral
#   - 200 L de solvente
#
# Lucros por unidade (por "lote" de cada combustível):
#   A: R$ 20,00
#   B: R$ 22,00
#   C: R$ 18,00
#
# Objetivo: determinar as quantidades de A, B e C que maximizam o lucro.

# [MODELO DE PROGRAMAÇÃO LINEAR]
# Variáveis de decisão:
#   xA = quantidade (lotes) de Combustível A a produzir
#   xB = quantidade (lotes) de Combustível B a produzir
#   xC = quantidade (lotes) de Combustível C a produzir
#
# Função Objetivo:
#   Max Z = 20*xA + 22*xB + 18*xC
#
# Restrições (uso de recursos):
#   (1) Extrato mineral: 8*xA + 5*xB + 4*xC <= 120
#   (2) Solvente:        5*xA + 4*xB + 2*xC <= 200
#   (3) Não negatividade: xA, xB, xC >= 0

# [CÓDIGO COMPLETO EM PYTHON COM SOLUÇÃO + VISUALIZAÇÃO EM 3D]

# Se estiver em ambiente local e precisar instalar:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1) Definir o problema (Maximizar)
model = pulp.LpProblem("Exemplo_05", pulp.LpMaximize)

# 2) Criar variáveis
xA = pulp.LpVariable('A', lowBound=0, cat='Continuous')
xB = pulp.LpVariable('B', lowBound=0, cat='Continuous')
xC = pulp.LpVariable('C', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 20*xA + 22*xB + 18*xC, "Lucro"

# 4) Restrições
model += 8*xA + 5*xB + 4*xC <= 120,  "Extrato_mineral"
model += 5*xA + 4*xB + 2*xC <= 200,  "Solvente"

# 5) Resolver
model.solve()

# 6) Mostrar resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("xA =", xA.varValue)
print("xB =", xB.varValue)
print("xC =", xC.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# 7) Plotar a região factível em 3D
# Observando as restrições e valores possíveis:
#   Se só A => 8A <= 120 => A <= 15, e 5A <= 200 => A <= 40 => mais restritivo é 15
#   Se só B => 5B <= 120 => B <= 24, e 4B <= 200 => B <= 50 => mais restritivo é 24
#   Se só C => 4C <= 120 => C <= 30, e 2C <= 200 => C <= 100 => mais restritivo é 30
# Então vamos percorrer 0..20 em A, 0..25 em B, 0..35 em C, para garantir.

xA_range = np.arange(0, 21, 1)  # 0..20
xB_range = np.arange(0, 26, 1)  # 0..25
xC_range = np.arange(0, 36, 1)  # 0..35

feasible_points = []
for a in xA_range:
    for b in xB_range:
        for c in xC_range:
            cond1 = (8*a + 5*b + 4*c <= 120)
            cond2 = (5*a + 4*b + 2*c <= 200)
            if cond1 and cond2:
                feasible_points.append((a, b, c))

feasible_points = np.array(feasible_points)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot da região factível
ax.scatter(
    feasible_points[:,0],
    feasible_points[:,1],
    feasible_points[:,2],
    s=5, color='gray', alpha=0.3, label='Região Factível'
)

# Plot da solução ótima
ax.scatter(
    [xA.varValue], [xB.varValue], [xC.varValue],
    color='red', s=80, label='Solução Ótima'
)

ax.set_xlabel('xA (Combustível A)')
ax.set_ylabel('xB (Combustível B)')
ax.set_zlabel('xC (Combustível C)')
ax.set_title('Região Factível (Exemplo 05) e Solução Ótima')
ax.legend()
plt.show()
