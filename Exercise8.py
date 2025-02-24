# Se precisar instalar PuLP:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1) Definir o problema
model = pulp.LpProblem("Exemplo_08", pulp.LpMaximize)

# 2) Variáveis de decisão
x1 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')  # P1
x2 = pulp.LpVariable("x2", lowBound=0, cat='Continuous')  # P2

# 3) Função objetivo
model += 1900*x1 + 2100*x2, "Receita"

# 4) Restrições
model += 4*x1 + 2*x2 <= 20,    "Forja"          # 20 horas de forja
model += 2*x1 + 3*x2 <= 10,    "Polimento"      # 10 horas de polimento
model += 100*x1 + 200*x2 <= 500, "MateriaPrima" # 500 unidades de matéria-prima

# 5) Resolver o modelo
model.solve()

# 6) Mostrar resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 =", x1.varValue)
print("x2 =", x2.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# 7) Plotando a região factível em 2D
#    Para cada x1, calculamos os limites de x2 impostos pelas restrições
x1_vals = np.linspace(0, 5, 200)  # gerando pontos de 0 a 5 (pois além de 5 fica inviável em algumas restrições)

# Restrições isolando x2:
# 1) 4x1 + 2x2 <= 20 => x2 <= (20 - 4x1)/2 = 10 - 2x1
def f_forja(x1):
    return 10 - 2*x1

# 2) 2x1 + 3x2 <= 10 => x2 <= (10 - 2x1)/3
def f_polimento(x1):
    return (10 - 2*x1)/3

# 3) 100x1 + 200x2 <= 500 => x2 <= (500 - 100x1)/200 = 2.5 - 0.5*x1
def f_materia(x1):
    return 2.5 - 0.5*x1

# Geramos cada curva e depois pegamos o "mínimo" entre elas, respeitando x2 >= 0
x2_forja = [f_forja(x) for x in x1_vals]
x2_polimento = [f_polimento(x) for x in x1_vals]
x2_materia = [f_materia(x) for x in x1_vals]

# Para a região factível, x2 deve ser <= cada uma dessas e >= 0
x2_feasible = []
for i, xv in enumerate(x1_vals):
    cand_forja     = x2_forja[i]
    cand_polimento = x2_polimento[i]
    cand_materia   = x2_materia[i]
    # O menor valor dentre as 3 restrições
    min_all = min(cand_forja, cand_polimento, cand_materia)
    # Garante não negatividade
    feasible_val = max(0, min_all)
    x2_feasible.append(feasible_val)

# Plot das retas de cada restrição
plt.figure(figsize=(8,6))
plt.plot(x1_vals, x2_forja, label='4x1 + 2x2 = 20 (Forja)', color='blue')
plt.plot(x1_vals, x2_polimento, label='2x1 + 3x2 = 10 (Polimento)', color='red')
plt.plot(x1_vals, x2_materia, label='100x1 + 200x2 = 500 (Matéria-prima)', color='green')

# Preenchendo a região factível (cinza)
plt.fill_between(x1_vals, x2_feasible, color='gray', alpha=0.3)

# Marcando a solução ótima
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 6)
plt.ylim(0, 6)
plt.xlabel('x1 (Unidades de P1)')
plt.ylabel('x2 (Unidades de P2)')
plt.title('Exemplo 08 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)
plt.show()
