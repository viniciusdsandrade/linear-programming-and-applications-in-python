import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1) Definição do modelo de minimização
model = pulp.LpProblem("Exemplo10_Minimizar_Custo_Papel", pulp.LpMinimize)

# 2) Variáveis de decisão (dias de operação)
d1 = pulp.LpVariable('Dias_Fabrica1', lowBound=0, cat='Continuous')
d2 = pulp.LpVariable('Dias_Fabrica2', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 1000 * d1 + 2000 * d2, "Custo_Total"

# 4) Restrições de demanda
model +=  8 * d1 +  2 * d2 >= 16, "Minimo_Fino"
model +=  1 * d1 +  1 * d2 >=  6, "Minimo_Medio"
model +=  2 * d1 +  7 * d2 >= 28, "Minimo_Grosso"

# 5) Resolver via Simplex
model.solve()

# 6) Exibir resultados
print("Status:", pulp.LpStatus[model.status])
print(f"Dias Fábrica 1 = {d1.varValue:.2f}")
print(f"Dias Fábrica 2 = {d2.varValue:.2f}")
print(f"Custo Mínimo   = R$ {pulp.value(model.objective):.2f}")

# 7) Plotagem da região factível
x = np.linspace(0, d1.varValue * 1.5, 300)
y1 = (16 - 8 * x) / 2    # 8d1 + 2d2 =16 → d2 = (16 -8 x)/2
y2 = (6  - 1 * x) / 1    # 1d1 + 1d2 =6  → d2 = 6 - x
y3 = (28 - 2 * x) / 7    # 2d1 + 7d2 =28 → d2 = (28 -2 x)/7

# Região factível: d2 ≥ max(demandas inversas)
y_min = np.maximum(np.maximum(y1, y2), y3)
y_max = np.clip(y_min, 0, None)

plt.figure(figsize=(8,6))
plt.plot(x, y1, label='8d₁ + 2d₂ = 16 (Fino)', linewidth=2)
plt.plot(x, y2, label='d₁ + d₂ = 6 (Médio)',    linewidth=2)
plt.plot(x, y3, label='2d₁ + 7d₂ = 28 (Grosso)',linewidth=2)

plt.fill_between(x, y_min, y_min + 0.1, color='gray', alpha=0.3, label='Região Factível')
plt.scatter(d1.varValue, d2.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, max(x))
plt.ylim(0, max(y_min)*1.1)
plt.xlabel('Dias Fábrica 1 (d₁)')
plt.ylabel('Dias Fábrica 2 (d₂)')
plt.title('Exemplo 10 – Região Factível e Solução Ótima')
plt.legend(); plt.grid(True)

# 8) Salvar o gráfico
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q10\exercise10.png',
    dpi=300
)
plt.show()
