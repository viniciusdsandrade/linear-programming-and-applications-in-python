import pulp                    # Biblioteca para modelagem e resolução de PL
import numpy as np             # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo 06 – Refinaria de Gasolinas
# =============================================================================
# Três tipos de gasolina (verde, azul, comum) produzidos a partir de:
#   • Gasolina pura: 9.600.000 L/sem
#   • Octana:         4.800.000 L/sem
#   • Aditivo:        2.200.000 L/sem
#
# Insumos por litro de produto:
#   Gasolina Verde:  0.22 L pura, 0.50 L octana, 0.28 L aditivo
#   Gasolina Azul:   0.52 L pura, 0.34 L octana, 0.14 L aditivo
#   Gasolina Comum:  0.74 L pura, 0.20 L octana, 0.06 L aditivo
#
# Regras de mercado:
#   • Comum ≥ 16 × Verde
#   • Azul ≤ 600 000 L/sem
#
# Margem unitária (R$/L):
#   • Verde = 0.30;  Azul = 0.25;  Comum = 0.20
#
# Variáveis de decisão:
#   xV = litros de gasolina verde
#   xA = litros de gasolina azul
#   xC = litros de gasolina comum
#
# Função objetivo:
#   Max Z = 0.30*xV + 0.25*xA + 0.20*xC
#
# Restrições:
#   0.22*xV + 0.52*xA + 0.74*xC ≤ 9_600_000   (pura)
#   0.50*xV + 0.34*xA + 0.20*xC ≤ 4_800_000   (octana)
#   0.28*xV + 0.14*xA + 0.06*xC ≤ 2_200_000   (aditivo)
#   xC ≥ 16*xV
#   xA ≤ 600_000
#   xV, xA, xC ≥ 0
# =============================================================================

# 1) Definir o problema (maximização)
model = pulp.LpProblem("Ex06_Maximizar_Lucro_Refinaria", pulp.LpMaximize)

# 2) Variáveis de decisão
xV = pulp.LpVariable('Gasolina_Verde', lowBound=0, cat='Continuous')
xA = pulp.LpVariable('Gasolina_Azul',  lowBound=0, cat='Continuous')
xC = pulp.LpVariable('Gasolina_Comum', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 0.30 * xV + 0.25 * xA + 0.20 * xC, "Margem_Total"

# 4) Restrições de insumo
model += 0.22 * xV + 0.52 * xA + 0.74 * xC <= 9_600_000, "Restricao_Pura"
model += 0.50 * xV + 0.34 * xA + 0.20 * xC <= 4_800_000, "Restricao_Octana"
model += 0.28 * xV + 0.14 * xA + 0.06 * xC <= 2_200_000, "Restricao_Aditivo"

# 5) Restrições de planejamento de mercado
model += xC >= 16 * xV,    "Comum_vs_Verde"
model += xA <= 600_000,    "Max_Azul"

# 6) Resolver (Simplex via CBC)
model.solve()

# 7) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print(f"Gasolina Verde (xV) = {xV.varValue:.0f} L")
print(f"Gasolina Azul  (xA) = {xA.varValue:.0f} L")
print(f"Gasolina Comum (xC) = {xC.varValue:.0f} L")
print(f"Margem Máxima   = R$ {pulp.value(model.objective):.2f}")

# 8) Visualização 2D: projeção xC vs xV com xA fixado no valor ótimo
opt_xA = xA.varValue

# Determinar domínio de xV baseado nos recursos e na regra xC ≥ 16*xV:
# Para cada recurso, calculamos o máximo xV tal que ainda exista xC ≥ 16*xV viável:
max_v1 = (9_600_000 - 0.52*opt_xA) / (0.22 + 0.74*16)
max_v2 = (4_800_000 - 0.34*opt_xA) / (0.50 + 0.20*16)
max_v3 = (2_200_000 - 0.14*opt_xA) / (0.28 + 0.06*16)
xV_max = min(max_v1, max_v2, max_v3, xV.varValue * 2)

xV_vals = np.linspace(0, xV_max, 400)

# Funções limites de xC dadas xV e xA=opt_xA:
y1 = (9_600_000 - 0.52*opt_xA - 0.22*xV_vals) / 0.74
y2 = (4_800_000 - 0.34*opt_xA - 0.50*xV_vals) / 0.20
y3 = (2_200_000 - 0.14*opt_xA - 0.28*xV_vals) / 0.06

y_max = np.minimum(np.minimum(y1, y2), y3)
y_min = 16 * xV_vals

mask = y_max >= y_min

plt.figure(figsize=(8,6))
plt.plot(xV_vals, y1, label='0.22xV +0.52xA+0.74xC=9.6M', linewidth=2)
plt.plot(xV_vals, y2, label='0.50xV +0.34xA+0.20xC=4.8M', linewidth=2)
plt.plot(xV_vals, y3, label='0.28xV +0.14xA+0.06xC=2.2M', linewidth=2)
plt.plot(xV_vals, y_min,'--', label='xC = 16·xV', linewidth=2)

plt.fill_between(xV_vals[mask], y_min[mask], y_max[mask], color='gray', alpha=0.3, label='Região Factível')

# Marcar solução ótima
plt.scatter(xV.varValue, xC.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlabel('Gasolina Verde (L)')
plt.ylabel('Gasolina Comum (L)')
plt.title('Exemplo 06 – Região Factível e Solução Ótima (xA fixo)')
plt.legend()
plt.grid(True)

# 9) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q6\exercise6.png'
plt.savefig(output_path, dpi=300)

plt.show()
