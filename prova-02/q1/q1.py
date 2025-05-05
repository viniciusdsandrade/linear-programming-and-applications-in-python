import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma empresa fabrica dois produtos, P1 e P2:
#   Lucro unitário:       P1 = R$ 1.000,00;   P2 = R$ 1.800,00
#   Tempo de fabricação:  P1 = 20 h/un;       P2 = 30 h/un
#   Capacidade anual:     1200 horas
#   Demanda máxima:       P1 <= 40 un;        P2 <= 30 un
#
# Modelo:
#   x1 = quant. produzida de P1
#   x2 = quant. produzida de P2
#   Max Z = 1000 x1 + 1800 x2
#   20 x1 + 30 x2 <= 1200
#   x1 <= 40
#   x2 <= 30
#   x1, x2 >= 0
# =============================================================================

# 1) Definir o problema (Maximização do lucro)
model = pulp.LpProblem("Prova2_Q1_Maximizar_Lucro", pulp.LpMaximize)

# 2) Criar variáveis de decisão (contínuas)
x1 = pulp.LpVariable('P1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('P2', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 1000 * x1 + 1800 * x2, "Lucro_Total"

# 4) Restrições
model += 20 * x1 + 30 * x2 <= 1200, "Restricao_Tempo"
model += x1 <= 40,                   "Restricao_Demanda_P1"
model += x2 <= 30,                   "Restricao_Demanda_P2"

# 5) Resolver com Simplex
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print("Quantidade P1 (x1) =", x1.varValue)
print("Quantidade P2 (x2) =", x2.varValue)
print("Lucro Máximo = R$", pulp.value(model.objective))

# 7) Plotar região factível e solução ótima
x_vals = np.linspace(0, 50, 400)

# Limites das restrições transformadas em igualdades:
y_tempo = (1200 - 20 * x_vals) / 30    # 20 x1 + 30 x2 = 1200  → x2 = (1200 - 20 x1)/30
y_demanda_p2 = np.full_like(x_vals, 30) # x2 = 30
# Para x1 <= 40, usaremos uma linha vertical; mas na região factível, basta x_vals ≤ 40

# Região factível: 0 ≤ x2 ≤ min(y_tempo, 30), e 0 ≤ x1 ≤ 40
y_max = np.minimum(y_tempo, y_demanda_p2)
y_max = np.clip(y_max, 0, None)

plt.figure(figsize=(8, 6))

# Plotar restrições
plt.plot(x_vals, y_tempo, label='20x₁ + 30x₂ = 1200 (Tempo)', linewidth=2)
plt.axhline(30,   label='x₂ = 30 (Demanda P2)',    linewidth=2, linestyle='--')
plt.axvline(40,   label='x₁ = 40 (Demanda P1)',    linewidth=2, linestyle='--')

# Preencher região factível
plt.fill_between(x_vals, 0, y_max, where=(x_vals <= 40), color='gray', alpha=0.3)

# Marcar solução ótima
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

# Configurações do gráfico
plt.xlim(0, 50)
plt.ylim(0, 35)
plt.xlabel('Quantidade P1 (x₁)')
plt.ylabel('Quantidade P2 (x₂)')
plt.title('Prova 2 – Q1: Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q1\exercise1.png'
plt.savefig(output_path, dpi=300)

# Exibir
plt.show()
