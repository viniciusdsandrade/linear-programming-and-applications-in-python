# -----------------------------------------
# Exemplo 02 - Programação Linear
# Visualização em 3D (x1, x2, x3)
# -----------------------------------------

# (Se precisar instalar)
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Necessário para plot 3D

# 1) Definir o problema (Maximizar)
model = pulp.LpProblem("Exemplo_02", pulp.LpMaximize)

# 2) Criar variáveis
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 2000 * x1 + 3000 * x2 + 2800 * x3, "Receita"

# 4) Restrições
model += 2 * x1 + 4 * x2 + 3 * x3 <= 25, "Restricao_Engenheiros"
model += 6 * x1 + 8 * x2 + 9 * x3 <= 40, "Restricao_Tecnicos"

# 5) Resolver
model.solve()

# 6) Mostrar resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 =", x1.varValue)
print("x2 =", x2.varValue)
print("x3 =", x3.varValue)
print("Receita máxima = R$", pulp.value(model.objective))

# 7) Plotar região factível em 3D
#    (varre uma malha 0<= x1 <= ~7, 0<= x2 <= ~6, 0<= x3 <= ~5 para mostrar pontos que satisfazem as restrições)
x1_range = np.arange(0, 7, 0.25)  # passo de 0.25 para não ficar muito pesado
x2_range = np.arange(0, 6, 0.25)
x3_range = np.arange(0, 5, 0.25)

feasible_points = []

for xv1 in x1_range:
    for xv2 in x2_range:
        for xv3 in x3_range:
            c1 = (2 * xv1 + 4 * xv2 + 3 * xv3 <= 25)
            c2 = (6 * xv1 + 8 * xv2 + 9 * xv3 <= 40)
            if c1 and c2:
                feasible_points.append((xv1, xv2, xv3))

# Converter em array para poder plotar
feasible_points = np.array(feasible_points)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot dos pontos factíveis
ax.scatter(
    feasible_points[:, 0],
    feasible_points[:, 1],
    feasible_points[:, 2],
    s=5,  # tamanho do marcador
    color='gray',
    alpha=0.3,
    label='Região Factível'
)

# Plot da solução ótima
ax.scatter(
    [x1.varValue], [x2.varValue], [x3.varValue],
    color='red', s=80, label='Solução Ótima'
)

ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('x3')
ax.set_title('Região Factível (Exemplo 02) e Solução Ótima')
ax.legend()
plt.show()
