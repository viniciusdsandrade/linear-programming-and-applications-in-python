import pulp  # biblioteca de otimização Linear Programming (LP) em Python :contentReference[oaicite:4]{index=4}
import numpy as np  # para geração de pontos na plotagem
import matplotlib.pyplot as plt  # para visualização da região factível :contentReference[oaicite:5]{index=5}

# 1) Definir o problema (Maximização)
model = pulp.LpProblem("Exemplo2_Maximizar_Receita", pulp.LpMaximize)

# 2) Variáveis de decisão contínuas (≥ 0)
x1 = pulp.LpVariable('TipoI', lowBound=0, cat='Continuous')  # equipes Tipo I :contentReference[oaicite:6]{index=6}
x2 = pulp.LpVariable('TipoII', lowBound=0, cat='Continuous')  # equipes Tipo II
x3 = pulp.LpVariable('TipoIII', lowBound=0, cat='Continuous')  # equipes Tipo III

# 3) Função objetivo
model += 2000 * x1 + 3000 * x2 + 2800 * x3, "Receita_Total"

# 4) Restrições de recursos
model += 2 * x1 + 4 * x2 + 3 * x3 <= 25, "Restricao_Engenheiros"
model += 6 * x1 + 8 * x2 + 9 * x3 <= 40, "Restricao_Tecnicos"

# 5) Resolver via Simplex (CBC por padrão no PuLP)
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print(f"x₁ (Tipo I) = {x1.varValue}")
print(f"x₂ (Tipo II) = {x2.varValue}")
print(f"x₃ (Tipo III) = {x3.varValue}")
print("Receita Máxima = R$", pulp.value(model.objective))

# Gera valores de x1 no intervalo de 0 a 15
x_vals = np.linspace(0, 15, 400)

# Calcula os limites de x2 impostos por cada restrição:
# 2 x1 + 4 x2 = 25 → x2 = (25 - 2 x1)/4
y_eng = (25 - 2 * x_vals) / 4
# 6 x1 + 8 x2 = 40 → x2 = (40 - 6 x1)/8
y_tec = (40 - 6 * x_vals) / 8

# Região factível: x2 ≤ min(y_eng, y_tec), x_vals ≥ 0
y_max = np.minimum(y_eng, y_tec)
y_max = np.clip(y_max, 0, None)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_eng, label='2x₁ + 4x₂ = 25 (Engenheiros)', linewidth=2)
plt.plot(x_vals, y_tec, label='6x₁ + 8x₂ = 40 (Técnicos)', linewidth=2)
plt.fill_between(x_vals, 0, y_max, color='gray', alpha=0.3,
                 label='Região Factível')  # :contentReference[oaicite:10]{index=10}
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 15)
plt.ylim(0, 10)
plt.xlabel('x₁ (Tipo I)');
plt.ylabel('x₂ (Tipo II e III combinados)')
plt.title('Exemplo 02 – Região Factível e Solução Ótima')
plt.legend();
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q2\exercise2.png'
plt.savefig(output_path, dpi=300)

plt.show()
