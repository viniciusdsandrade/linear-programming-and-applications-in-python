import pulp                    # Biblioteca para modelagem e resolução de PL
import numpy as np             # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exercício – Fabricação de Panelas de Pressão e Frigideiras
# Salvando gráfico em:
# C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-04
# =============================================================================

# 1) Definir o problema como maximização
model = pulp.LpProblem("Maximizar_Lucro_Panelas_Frigideiras", pulp.LpMaximize)

# 2) Criar variáveis de decisão (contínuas, ≥ 0, ≤ demanda)
x = pulp.LpVariable('panelas_pressao', lowBound=0, upBound=4, cat='Continuous')
y = pulp.LpVariable('frigideiras',      lowBound=0, upBound=4, cat='Continuous')

# 3) Definir a função objetivo
model += 3 * x + 4 * y, "Lucro_Total"

# 4) Restrições
model += x + y <= 6, "Horas_de_Maquina"  # 1 h/un, só 6 h/dia

# 5) Resolver
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print(f"Produzir panelas de pressão (x) = {x.varValue:.0f} un.")
print(f"Produzir frigideiras       (y) = {y.varValue:.0f} un.")
print(f"Lucro Máximo = R$ {pulp.value(model.objective):.2f}")

# Comentário:
# Plano ótimo: x = 2 panelas, y = 4 frigideiras → Lucro = R$22,00

# 7) Plot da região factível
x_vals = np.linspace(0, 4, 100)
y_vals = np.linspace(0, 4, 100)
X, Y = np.meshgrid(x_vals, y_vals)
feasible = (X + Y) <= 6

plt.figure(figsize=(6, 6))
plt.contourf(X, Y, feasible, levels=[-0.5, 0.5, 1.5], alpha=0.3)
plt.contour(X, Y, X + Y, levels=[6], colors='blue', linestyles='--', linewidths=2)

# Marcar solução ótima
opt_x, opt_y = x.varValue, y.varValue
plt.scatter(opt_x, opt_y, color='red', zorder=5, label=f'Ótimo ({opt_x:.0f}, {opt_y:.0f})')

plt.xlim(0, 4)
plt.ylim(0, 4)
plt.xlabel('Panelas de pressão (x)')
plt.ylabel('Frigideiras (y)')
plt.title('Região Factível e Ponto Ótimo')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico no diretório especificado
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-04\regiao_factivel_exercise_10.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Gráfico salvo em: {output_path}")

plt.show()
