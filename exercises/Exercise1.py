# [RESUMO DO PROBLEMA]
# Modelo de Programação Linear para maximizar o lucro ao fabricar P1 e P2:
#    Max Z = 1000*x1 + 1800*x2
# Sujeito às restrições:
#    20*x1 + 30*x2 ≤ 1200   (tempo de produção)
#    x1 ≤ 40               (demanda de P1)
#    x2 ≤ 30               (demanda de P2)
#    x1 ≥ 0, x2 ≥ 0

# [CÓDIGO COMPLETO EM PYTHON COM SOLUÇÃO E GRÁFICO]

# Instale o PuLP se necessário:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1) Definir o problema
model = pulp.LpProblem("Exemplo_01", pulp.LpMaximize)

# 2) Criar variáveis
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')

# 3) Definir a função objetivo
model += 1000 * x1 + 1800 * x2, "Lucro"

# 4) Adicionar restrições
model += 20 * x1 + 30 * x2 <= 1200, "Restricao_tempo"
model += x1 <= 40, "Restricao_demanda_P1"
model += x2 <= 30, "Restricao_demanda_P2"

# 5) Resolver o modelo
model.solve()

# 6) Mostrar resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 =", x1.varValue)
print("x2 =", x2.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# 7) Plotar a região factível e a solução ótima
x1_vals = np.linspace(0, 40, 200)
x2_from_time = (1200 - 20 * x1_vals) / 30

plt.figure(figsize=(8, 6))
plt.plot(x1_vals, x2_from_time, label='20x1 + 30x2 = 1200', color='blue')
plt.axvline(x=40, color='red', label='x1 = 40')
plt.hlines(y=30, xmin=0, xmax=40, color='green', label='x2 = 30')
x2_feasible = np.minimum(x2_from_time, 30)
x2_feasible = np.maximum(x2_feasible, 0)
plt.fill_between(x1_vals, x2_feasible, color='gray', alpha=0.3)
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')
plt.xlim(0, 45)
plt.ylim(0, 35)
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)
plt.show()
