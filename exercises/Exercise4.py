# [RESUMO DO PROBLEMA]
# A metalúrgica produz três componentes: A, B e C.
#   - Em 1 hora, se produzir SOMENTE A, faz 25 unidades;
#     se produzir SOMENTE B, faz 30 unidades;
#     se produzir SOMENTE C, faz 40 unidades.
# Cada componente consome duas espécies de recurso (I e II):
#   A: 40 de I, 30 de II
#   B: 25 de I, 15 de II
#   C: 18 de I, 10 de II
# Há disponibilidade total de 712 unidades do recurso I e 450 do recurso II.
# O lucro unitário de A, B, C é R$ 25, R$ 15 e R$ 11, respectivamente.
# OBJETIVO: Maximizar o lucro total de 1 hora de produção.

# [MODELO DE PROGRAMAÇÃO LINEAR]
# Variáveis:
#   xA = quantidade de A produzida em 1 hora
#   xB = quantidade de B produzida em 1 hora
#   xC = quantidade de C produzida em 1 hora
#
# Função Objetivo:
#   Max Z = 25*xA + 15*xB + 11*xC
#
# Restrições:
#   (1) Tempo: (xA / 25) + (xB / 30) + (xC / 40) <= 1
#   (2) Recurso I: 40*xA + 25*xB + 18*xC <= 712
#   (3) Recurso II: 30*xA + 15*xB + 10*xC <= 450
#   (4) xA, xB, xC >= 0

# [CÓDIGO COMPLETO EM PYTHON COM SOLUÇÃO + VISUALIZAÇÃO EM 3D]

# Se estiver em ambiente local e precisar instalar:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1) Definir o problema
model = pulp.LpProblem("Exemplo_04", pulp.LpMaximize)

# 2) Criar variáveis
xA = pulp.LpVariable('A', lowBound=0, cat='Continuous')  # Quant. de A produzida em 1h
xB = pulp.LpVariable('B', lowBound=0, cat='Continuous')  # Quant. de B produzida em 1h
xC = pulp.LpVariable('C', lowBound=0, cat='Continuous')  # Quant. de C produzida em 1h

# 3) Função objetivo
model += 25 * xA + 15 * xB + 11 * xC, "Lucro"

# 4) Restrições
# (xA / 25) + (xB / 30) + (xC / 40) <= 1  -> evite usar / direto, use multiplicação por inverso
model += (1 / 25) * xA + (1 / 30) * xB + (1 / 40) * xC <= 1, "Restricao_Tempo"
model += 40 * xA + 25 * xB + 18 * xC <= 712, "Restricao_Rec_I"
model += 30 * xA + 15 * xB + 10 * xC <= 450, "Restricao_Rec_II"

# 5) Resolver o modelo
model.solve()

# 6) Mostrar resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("xA (A) =", xA.varValue)
print("xB (B) =", xB.varValue)
print("xC (C) =", xC.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# 7) Plotar a região factível em 3D
#    Observando as restrições, vamos definir intervalos razoáveis para xA, xB, xC.
#    - Tempo (xA/25 + xB/30 + xC/40 <= 1) -> se só produzir A, xA <= 25; B <= 30; C <= 40
#    - Recurso I (40A + 25B + 18C <= 712) -> se só produzir A, A <= 17.8 (~17)
#    - Recurso II (30A + 15B + 10C <= 450) -> se só produzir A, A <= 15
#    Tomando o mais restritivo para A (15 ou 17?), ficamos em ~15-17, mas para segurança usaremos 20.
#    Para B, se só B => xB <= 30 (tempo) e 25*30=750>712 => xB<=28.48 do Recurso I -> ~28
#    Para C, se só C => xC <= 40 (tempo) e 18*40=720>712 => ~39, e Recurso II => 10*40=400 <=450 ok
#    Para não exagerar, vamos de 0..30 p/ xB e 0..40 p/ xC, 0..20 p/ xA.

xA_range = np.arange(0, 21, 1)  # 0..20
xB_range = np.arange(0, 31, 1)  # 0..30
xC_range = np.arange(0, 41, 1)  # 0..40

feasible_points = []

for a in xA_range:
    for b in xB_range:
        for c in xC_range:
            # Checar se satisfaz
            cond_tempo = (a / 25) + (b / 30) + (c / 40) <= 1
            cond_rI = 40 * a + 25 * b + 18 * c <= 712
            cond_rII = 30 * a + 15 * b + 10 * c <= 450
            if cond_tempo and cond_rI and cond_rII:
                feasible_points.append((a, b, c))

feasible_points = np.array(feasible_points)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot dos pontos factíveis
ax.scatter(
    feasible_points[:, 0],
    feasible_points[:, 1],
    feasible_points[:, 2],
    s=5,
    color='gray',
    alpha=0.3,
    label='Região Factível'
)

# Plot da solução ótima em vermelho
ax.scatter(
    [xA.varValue], [xB.varValue], [xC.varValue],
    color='red', s=80, label='Solução Ótima'
)

ax.set_xlabel('xA (A por hora)')
ax.set_ylabel('xB (B por hora)')
ax.set_zlabel('xC (C por hora)')
ax.set_title('Região Factível (Exemplo 04) e Solução Ótima')
ax.legend()
plt.show()
