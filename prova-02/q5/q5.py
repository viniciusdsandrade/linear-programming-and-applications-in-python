import pulp                    # Biblioteca para modelagem e resolução de PL
import numpy as np             # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo 05 – Óleos Unidos S.A.
# =============================================================================
# Mistura de dois insumos (extrato mineral e solvente) para produzir três
# combustíveis A, B e C sem perdas de material:
#
# Proporção por litro de produto:
#   • Combustível A: 8 L extrato mineral, 5 L solvente
#   • Combustível B: 5 L extrato mineral, 4 L solvente
#   • Combustível C: 4 L extrato mineral, 2 L solvente
#
# Disponibilidade total:
#   • Extrato mineral: 120 L
#   • Solvente:         200 L
#
# Lucro unitário (R$):
#   • A = 20 ;  B = 22 ;  C = 18
#
# Variáveis de decisão:
#   xA = litros de A a produzir
#   xB = litros de B a produzir
#   xC = litros de C a produzir
#
# Função objetivo:
#   Max Z = 20*xA + 22*xB + 18*xC
#
# Restrições:
#   8*xA + 5*xB + 4*xC ≤ 120   (extrato mineral)
#   5*xA + 4*xB + 2*xC ≤ 200   (solvente)
#   xA, xB, xC ≥ 0
# =============================================================================

# 1) Definir o problema como maximização
model = pulp.LpProblem("Exemplo5_Maximizar_Lucro_OleosUnidos", pulp.LpMaximize)

# 2) Criar variáveis de decisão (contínuas, ≥ 0)
xA = pulp.LpVariable('A', lowBound=0, cat='Continuous')
xB = pulp.LpVariable('B', lowBound=0, cat='Continuous')
xC = pulp.LpVariable('C', lowBound=0, cat='Continuous')

# 3) Definir a função objetivo
model += 20 * xA + 22 * xB + 18 * xC, "Lucro_Total"

# 4) Adicionar restrições de insumos
model += 8 * xA + 5 * xB + 4 * xC <= 120, "Restricao_ExtratoMineral"
model += 5 * xA + 4 * xB + 2 * xC <= 200, "Restricao_Solvente"

# 5) Resolver via Simplex (CBC por padrão)
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print("Produção A (xA) =", xA.varValue, "L")
print("Produção B (xB) =", xB.varValue, "L")
print("Produção C (xC) =", xC.varValue, "L")
print("Lucro Máximo = R$", pulp.value(model.objective))

# 7) Visualização da região factível projetada em 2D (xA vs xB para xC = 0)
# Gerar valores de xA e xB
xA_vals = np.linspace(0, 20, 400)
xB_vals = np.linspace(0, 30, 400)
X_A, X_B = np.meshgrid(xA_vals, xB_vals)

# Consid. xC = 0 → restrições:
mineral_feasible = (8*X_A + 5*X_B) <= 120
solvente_feasible = (5*X_A + 4*X_B) <= 200
feasible = mineral_feasible & solvente_feasible

plt.figure(figsize=(8,6))
plt.contourf(X_A, X_B, feasible, levels=[-0.5,0.5,1.5], colors=['white','gray'], alpha=0.3)

# Linhas de igualdade das restrições com xC = 0
plt.contour(X_A, X_B, 8*X_A + 5*X_B, levels=[120], colors='blue', linewidths=2, linestyles='--')
plt.contour(X_A, X_B, 5*X_A + 4*X_B, levels=[200], colors='red',  linewidths=2, linestyles='--')

# Marcar solução ótima (projeção em xC=0)
opt_xA, opt_xB, _ = xA.varValue, xB.varValue, xC.varValue
plt.scatter(opt_xA, opt_xB, color='black', zorder=5, label='Ótimo (xC projetado = 0)')

plt.xlim(0, max(xA_vals))
plt.ylim(0, max(xB_vals))
plt.xlabel('Litros de A (xA)')
plt.ylabel('Litros de B (xB)')
plt.title('Exemplo 05 – Região Factível (xC=0) e Solução Ótima')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q5\exercise5.png'
plt.savefig(output_path, dpi=300)

plt.show()
