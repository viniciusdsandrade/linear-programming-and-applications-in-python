import pulp  # Biblioteca para modelagem e resolução de PL
import numpy as np  # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo – Afia Bem Ltda. (Facas P, M e G)
# =============================================================================
# Dados do problema:
# • Máquinas (tempo diário disponível em segundos):
#     Corte:     4 h = 4*3600 = 14400 s
#     Modelagem: 6 h = 6*3600 = 21600 s
#     Afiação:   6 h = 6*3600 = 21600 s
#     Cabo:      8 h = 8*3600 = 28800 s
#     Montagem:  8 h = 8*3600 = 28800 s
#
# • Tempos por faca (segundos):
#     Máquina    |  Padrão (P) | Médio (M) | Grande (G)
#     Corte      |    10       |    10     |    12
#     Modelagem  |    10       |   15.5    |    17
#     Afiação    |    12       |    16     |    19
#     Cabo       |    19       |    21     |    24
#     Montagem   |    19       |    21     |    22
#
# • Chapa metálica:
#     Área por faca: P = 25 cm², M = 32 cm², G = 45 cm²
#     1 chapa = 2,00 m² = 20000 cm²
#     Disponibilidade: 2.5 chapas = 2.5 * 20000 = 50000 cm²
#
# • Lucro unitário (R$): P = 3.00; M = 4.00; G = 4.70
#
# Variáveis:
#   xP, xM, xG ≥ 0 — quantidades de facas Padrão, Média e Grande
#
# Objetivo:
#   Max Z = 3*xP + 4*xM + 4.7*xG
#
# Restrições:
#   10*xP + 10*xM + 12*xG ≤ 14400    (Corte)
#   10*xP + 15.5*xM + 17*xG ≤ 21600   (Modelagem)
#   12*xP + 16*xM + 19*xG ≤ 21600     (Afiação)
#   19*xP + 21*xM + 24*xG ≤ 28800     (Cabo)
#   19*xP + 21*xM + 22*xG ≤ 28800     (Montagem)
#   25*xP + 32*xM + 45*xG ≤ 50000     (Chapa)
# =============================================================================

# 1) Definir problema
model = pulp.LpProblem("AfiaBem_Facas", pulp.LpMaximize)

# 2) Decisão
xP = pulp.LpVariable('Padrao', lowBound=0, cat='Continuous')
xM = pulp.LpVariable('Medio', lowBound=0, cat='Continuous')
xG = pulp.LpVariable('Grande', lowBound=0, cat='Continuous')

# 3) Objetivo
model += 3.0 * xP + 4.0 * xM + 4.7 * xG, "Lucro_Total"

# 4) Restrições de máquina
model += 10 * xP + 10 * xM + 12 * xG <= 14400, "Corte"
model += 10 * xP + 15.5 * xM + 17 * xG <= 21600, "Modelagem"
model += 12 * xP + 16 * xM + 19 * xG <= 21600, "Afiacao"
model += 19 * xP + 21 * xM + 24 * xG <= 28800, "Cabo"
model += 19 * xP + 21 * xM + 22 * xG <= 28800, "Montagem"

# 5) Restrição de chapa
model += 25 * xP + 32 * xM + 45 * xG <= 50000, "Chapa"

# 6) Resolver
model.solve()

# 7) Resultados
print("Status:", pulp.LpStatus[model.status])
print(f"Padrão (xP) = {xP.varValue:.1f}")
print(f"Médio  (xM) = {xM.varValue:.1f}")
print(f"Grande (xG) = {xG.varValue:.1f}")
print(f"Lucro Máximo = R$ {pulp.value(model.objective):.2f}")

# 8) Gráfico 2D: projeção xP vs xM (assumindo xG = 0)
xP_vals = np.linspace(0, xP.varValue * 1.2, 300)
xM_vals = np.linspace(0, xM.varValue * 1.2, 300)
X, Y = np.meshgrid(xP_vals, xM_vals)

# com xG = 0, restrições de chapa e corte:
corte_feasible = (10 * X + 10 * Y) <= 14400
model_feasible = (10 * X + 15.5 * Y) <= 21600
afiacao_feasible = (12 * X + 16 * Y) <= 21600
cabo_feasible = (19 * X + 21 * Y) <= 28800
mont_feasible = (19 * X + 21 * Y) <= 28800
chapa_feasible = (25 * X + 32 * Y) <= 50000

feasible = corte_feasible & model_feasible & afiacao_feasible & cabo_feasible & mont_feasible & chapa_feasible

plt.figure(figsize=(8, 6))
plt.contourf(X, Y, feasible, levels=[-0.5, 0.5, 1.5], colors=['white', 'gray'], alpha=0.3)
plt.contour(X, Y, 10 * X + 10 * Y, levels=[14400], colors='blue', linestyles='--')
plt.contour(X, Y, 25 * X + 32 * Y, levels=[50000], colors='red', linestyles='--')
plt.scatter(xP.varValue, xM.varValue, color='black', zorder=5, label='Ótimo (proj. xG=0)')

plt.xlim(0, max(xP_vals))
plt.ylim(0, max(xM_vals))
plt.xlabel('Facas Padrão (xP)')
plt.ylabel('Facas Média (xM)')
plt.title('Região Factível e Solução Ótima (xG = 0)')
plt.legend()
plt.grid(True)

# 9) Salvar gráfico
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q7\exercise07.png',
            dpi=300)
plt.show()
