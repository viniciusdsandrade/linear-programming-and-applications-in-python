import pulp                    # Biblioteca para modelagem e resolução de PL
import numpy as np             # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo 09 – Transporte de 600 funcionários
# =============================================================================
# Ônibus disponíveis:
#   G: capacidade 60 pessoas, custo R$ 190 por viagem, total de 8 ônibus
#   P: capacidade 40 pessoas, custo R$ 140 por viagem, total de 12 ônibus
# Motoristas disponíveis: 13
# Funcionários a transportar: 600
#
# Variáveis:
#   xG = número de ônibus G usados (inteiro, 0 ≤ xG ≤ 8)
#   xP = número de ônibus P usados (inteiro, 0 ≤ xP ≤ 12)
#
# Objetivo:
#   Minimizar Custo = 190*xG + 140*xP
#
# Restrições:
#   60*xG + 40*xP ≥ 600     (capacidade total ≥ 600 passageiros)
#   xG + xP ≤ 13            (motoristas)
# =============================================================================

# 1) Definir o modelo de minimização
model = pulp.LpProblem("Exemplo09_Minimizar_Custo_Transporte", pulp.LpMinimize)

# 2) Definir variáveis inteiras
xG = pulp.LpVariable('Onibus_G', lowBound=0, upBound=8, cat='Integer')
xP = pulp.LpVariable('Onibus_P', lowBound=0, upBound=12, cat='Integer')

# 3) Função objetivo
model += 190 * xG + 140 * xP, "Custo_Total"

# 4) Restrições
model += 60 * xG + 40 * xP >= 600, "Capacidade_Passageiros"
model += xG + xP <= 13,            "Motoristas_Disponiveis"

# 5) Resolver
model.solve()

# 6) Resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print(f"Ônibus G usados (xG) = {xG.varValue}")
print(f"Ônibus P usados (xP) = {xP.varValue}")
print(f"Custo Mínimo = R$ {pulp.value(model.objective):.2f}")

# 7) Plotagem da região factível e solução ótima
xG_vals = np.arange(0, 9)   # 0 a 8
xP_vals = np.arange(0, 13)  # 0 a 12
XG, XP = np.meshgrid(xG_vals, xP_vals)

# Verificar factibilidade
cap_ok = (60 * XG + 40 * XP) >= 600
drv_ok = (XG + XP) <= 13
feasible = cap_ok & drv_ok

plt.figure(figsize=(8, 6))
plt.scatter(XG[feasible], XP[feasible], color='lightgray', label='Região Factível')
plt.plot(xG_vals, (600 - 60 * xG_vals) / 40, label='60xG + 40xP = 600', linewidth=2)
plt.plot(xG_vals, 13 - xG_vals,            label='xG + xP = 13',       linewidth=2)

# Subir o contorno de xP para inteiro dentro dos limites
plt.scatter(xG.varValue, xP.varValue, color='red', s=100, label='Solução Ótima')

plt.xlim(0, 8)
plt.ylim(0, 12)
plt.xlabel('Número de Ônibus G (xG)')
plt.ylabel('Número de Ônibus P (xP)')
plt.title('Exemplo 09 – Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q9\exercise9.png'
plt.savefig(output_path, dpi=300)

plt.show()
