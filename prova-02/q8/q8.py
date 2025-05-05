import pulp                    # Biblioteca para modelagem e resolução de PL
import numpy as np             # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo 08 – Produção de P1 e P2
# =============================================================================
# Dados do problema:
#   • P1: 4 h forja, 2 h polimento, 100 un mat-prima; venda R$ 1 900
#   • P2: 2 h forja, 3 h polimento, 200 un mat-prima; venda R$ 2 100
#
# Recursos disponíveis por dia:
#   • Forja:       20 h
#   • Polimento:   10 h
#   • Matéria-prima: 500 unidades
#
# Variáveis de decisão:
#   x1 = unidades de P1
#   x2 = unidades de P2
#
# Objetivo:
#   Max Z = 1900*x1 + 2100*x2
#
# Restrições:
#   4*x1 + 2*x2 ≤ 20      (forja)
#   2*x1 + 3*x2 ≤ 10      (polimento)
#   100*x1 + 200*x2 ≤ 500 (matéria-prima)
# =============================================================================

# 1) Definir o modelo de maximização
model = pulp.LpProblem("Exemplo08_Prod_P1_P2", pulp.LpMaximize)

# 2) Criar variáveis de decisão
x1 = pulp.LpVariable('P1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('P2', lowBound=0, cat='Continuous')

# 3) Definir a função objetivo
model += 1900 * x1 + 2100 * x2, "Receita_Total"

# 4) Adicionar as restrições
model += 4 * x1 + 2 * x2 <= 20,      "Restricao_Forja"
model += 2 * x1 + 3 * x2 <= 10,      "Restricao_Polimento"
model += 100 * x1 + 200 * x2 <= 500, "Restricao_MateriaPrima"

# 5) Resolver (Simplex via CBC)
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print(f"P1 (x1) = {x1.varValue:.0f}")
print(f"P2 (x2) = {x2.varValue:.0f}")
print(f"Receita Máxima = R$ {pulp.value(model.objective):.2f}")

# 7) Visualização da região factível e solução ótima
# Gerar valores de x1 no intervalo 0 até um pouco acima do ótimo
x_vals = np.linspace(0, x1.varValue * 1.5, 300)

# Cálculo de x2 nos limites de cada restrição:
y_forja      = (20  - 4  * x_vals) / 2
y_polimento  = (10  - 2  * x_vals) / 3
y_materia    = (500 - 100 * x_vals) / 200

# Região factível: x2 ≤ min(dos três limites), não-negativo
y_max = np.minimum(np.minimum(y_forja, y_polimento), y_materia)
y_max = np.clip(y_max, 0, None)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_forja,     label='4x₁ + 2x₂ = 20 (Forja)',         linewidth=2)
plt.plot(x_vals, y_polimento, label='2x₁ + 3x₂ = 10 (Polimento)',     linewidth=2)
plt.plot(x_vals, y_materia,   label='100x₁ + 200x₂ = 500 (Mat-Prima)', linewidth=2)

# Preencher a região factível
plt.fill_between(x_vals, 0, y_max, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

# Configurações do gráfico
plt.xlim(0, max(x_vals))
plt.ylim(0, max(y_max) * 1.1)
plt.xlabel('Quantidade de P1 (x₁)')
plt.ylabel('Quantidade de P2 (x₂)')
plt.title('Exemplo 08 – Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q8\exercise8.png'
plt.savefig(output_path, dpi=300)

plt.show()
