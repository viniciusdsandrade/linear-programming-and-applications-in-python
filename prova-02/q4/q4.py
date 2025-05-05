import pulp  # Biblioteca para modelagem e resolução de PL
import numpy as np  # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo 04 – Metalúrgica
# =============================================================================
# A metalúrgica:
#   • Pode produzir por hora:
#       – 25 unidades de A
#       – 30 unidades de B
#       – 40 unidades de C
#   • Usa recursos por unidade:
#       – A: 40 do recurso I, 30 do recurso II
#       – B: 25 do recurso I, 15 do recurso II
#       – C: 18 do recurso I, 10 do recurso II
#   • Disponível por hora: 712 do recurso I, 450 do recurso II
#   • Lucro unitário: A = R$25,00; B = R$15,00; C = R$11,00
#
# Variáveis de decisão:
#   x1 = quantidade de A produzida
#   x2 = quantidade de B produzida
#   x3 = quantidade de C produzida
#
# Função objetivo:
#   Max Z = 25*x1 + 15*x2 + 11*x3
#
# Restrições:
#   • Tempo:   x1/25 + x2/30 + x3/40 ≤ 1
#   • Recurso I: 40*x1 + 25*x2 + 18*x3 ≤ 712
#   • Recurso II:30*x1 + 15*x2 + 10*x3 ≤ 450
#   • x1, x2, x3 ≥ 0
# =============================================================================

# 1) Definir o problema como maximização
model = pulp.LpProblem("Exemplo4_Maximizar_Lucro_Metalurgica", pulp.LpMaximize)

# 2) Criar variáveis de decisão (contínuas, ≥ 0)
x1 = pulp.LpVariable('A', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('B', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('C', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 25 * x1 + 15 * x2 + 11 * x3, "Lucro_Total"

# 4) Restrições
model += (1 / 25) * x1 + (1 / 30) * x2 + (1 / 40) * x3 <= 1, "Restricao_Tempo"
model += 40 * x1 + 25 * x2 + 18 * x3 <= 712, "Restricao_Recurso_I"
model += 30 * x1 + 15 * x2 + 10 * x3 <= 450, "Restricao_Recurso_II"

# 5) Resolver via Simplex (CBC por padrão)
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print("Produção de A (x1) =", x1.varValue)
print("Produção de B (x2) =", x2.varValue)
print("Produção de C (x3) =", x3.varValue)
print("Lucro Máximo = R$", pulp.value(model.objective))

# 7) Visualização da região factível (projeção em 2D x1 vs x2 para x3 = 0)
#    e solução ótima projetada

# Gerar grade para x1 e x2
x1_vals = np.linspace(0, 30, 300)
x2_vals = np.linspace(0, 30, 300)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Para cada (x1, x2) definiu x3=0, verificar restrições de tempo, I e II
time_feasible = (X1 / 25 + X2 / 30) <= 1
resI_feasible = (40 * X1 + 25 * X2) <= 712
resII_feasible = (30 * X1 + 15 * X2) <= 450
feasible = time_feasible & resI_feasible & resII_feasible

plt.figure(figsize=(8, 6))

# Preencher região factível
plt.contourf(X1, X2, feasible, levels=[-0.5, 0.5, 1.5], colors=['white', 'gray'], alpha=0.3)

# Plotar contornos das restrições (linhas de igualdade quando x3=0)
plt.contour(X1, X2, X1 / 25 + X2 / 30, levels=[1], colors='blue', linewidths=2, linestyles='--')
plt.contour(X1, X2, 40 * X1 + 25 * X2, levels=[712], colors='red', linewidths=2, linestyles='--')
plt.contour(X1, X2, 30 * X1 + 15 * X2, levels=[450], colors='green', linewidths=2, linestyles='--')

# Marcar solução ótima projetada em x3=0
opt_x1 = x1.varValue
opt_x2 = x2.varValue
plt.scatter(opt_x1, opt_x2, color='black', zorder=5, label='Ótimo (proj. x3=0)')

plt.xlim(0, 30)
plt.ylim(0, 30)
plt.xlabel('Produção de A (x₁)')
plt.ylabel('Produção de B (x₂)')
plt.title('Exemplo 04 – Região Factível (x₃=0) e Solução Ótima')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q4\exercise4.png'
plt.savefig(output_path, dpi=300)

plt.show()
