import pulp  # Biblioteca para modelagem e resolução de PL
import numpy as np  # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exercício – Fabricação de Panelas de Pressão e Frigideiras
# =============================================================================
# Uma fábrica produz dois itens:
#   • panela de pressão (x) → lucro de R$ 3,00 por unidade
#   • frigideira       (y) → lucro de R$ 4,00 por unidade
#
# Cada unidade demanda 1 hora de máquina para moldagem, e há somente 6 horas
# disponíveis por dia. A demanda de mercado limita a 4 unidades de cada item.
#
# Variáveis de decisão:
#   x = nº de panelas de pressão a produzir
#   y = nº de frigideiras a produzir
#
# Função objetivo:
#   Max Z =  3·x + 4·y
#
# Restrições:
#   1·x + 1·y ≤ 6    (horas de máquina disponíveis)
#   x ≤ 4            (demanda máxima de panelas)
#   y ≤ 4            (demanda máxima de frigideiras)
#   x, y ≥ 0
# =============================================================================

# 1) Definir o problema como maximização
model = pulp.LpProblem("Maximizar_Lucro_Panelas_Frigideiras", pulp.LpMaximize)

# 2) Criar variáveis de decisão (contínuas, ≥ 0)
x = pulp.LpVariable('panelas_pressao', lowBound=0, upBound=4, cat='Continuous')
y = pulp.LpVariable('frigideiras', lowBound=0, upBound=4, cat='Continuous')

# 3) Definir a função objetivo
model += 3 * x + 4 * y, "Lucro_Total"

# 4) Adicionar restrições
model += x + y <= 6, "Horas_de_Maquina"
# (as restrições de demanda já foram impostas pelos bounds upBound nas variáveis)

# 5) Resolver via Simplex (solver padrão CBC)
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print(f"Produzir panelas de pressão (x) = {x.varValue:.0f} un.")
print(f"Produzir frigideiras       (y) = {y.varValue:.0f} un.")
print(f"Lucro Máximo = R$ {pulp.value(model.objective):.2f}")

# =============================================================================
# SOLUÇÃO ÓTIMA (comentário):
# A solução encontrada é x = 2 panelas de pressão e y = 4 frigideiras,
# atingindo o lucro máximo de R$ 22,00 por dia. Esse plano utiliza todas
# as 6 horas disponíveis de máquina e respeita a demanda máxima de cada item.
# =============================================================================

# 7) Visualização da região factível (x vs y)
# Gerar uma grade de valores de x e y
x_vals = np.linspace(0, 4, 100)
y_vals = np.linspace(0, 4, 100)
X, Y = np.meshgrid(x_vals, y_vals)

# Definir a região factível: x + y ≤ 6
feasible = (X + Y) <= 6

plt.figure(figsize=(6, 6))
plt.contourf(X, Y, feasible, levels=[-0.5, 0.5, 1.5], alpha=0.3)
# Desenhar as linhas de igualdade das restrições
plt.contour(X, Y, X + Y, levels=[6], colors='blue', linestyles='--', linewidths=2)
# Marcar a solução ótima
opt_x, opt_y = x.varValue, y.varValue
plt.scatter(opt_x, opt_y, color='red', zorder=5, label='Ótimo (2, 4)')

plt.xlim(0, 4)
plt.ylim(0, 4)
plt.xlabel('Panelas de pressão (x)')
plt.ylabel('Frigideiras (y)')
plt.title('Região Factível e Ponto Ótimo')
plt.legend()
plt.grid(True)
plt.show()
