import pulp                    # Biblioteca para modelagem e resolução de PL
import numpy as np             # Para geração de pontos na plotagem
import matplotlib.pyplot as plt  # Para visualização da região factível

# =============================================================================
# Exemplo 03 – Sapateiro
# =============================================================================
# O sapateiro:
#   • Produz sapatos a uma taxa de 6 un/h
#   • Produz cintos a uma taxa de 5 un/h
# Consome couro:
#   • 2 unidades de couro por sapato
#   • 1 unidade de couro por cinto
# Disponível: 6 unidades de couro, 1 hora de trabalho
# Lucro unitário:
#   • Sapato: $5,00
#   • Cinto:  $2,00
#
# Variáveis de decisão:
#   x1 = número de sapatos produzidos por hora
#   x2 = número de cintos   produzidos por hora
#
# Função objetivo:
#   Max Z = 5*x1 + 2*x2
#
# Restrições:
#   • Tempo:   (1/6)*x1 + (1/5)*x2 ≤ 1       (horas totais ≤ 1h)
#   • Couro:   2*x1 + 1*x2 ≤ 6               (couro disponível)
#   • x1, x2 ≥ 0
# =============================================================================

# 1) Definir o problema como maximização
model = pulp.LpProblem("Exemplo3_Maximizar_Lucro_Sapateiro", pulp.LpMaximize)

# 2) Criar variáveis de decisão (contínuas, ≥ 0)
x1 = pulp.LpVariable('Sapatos', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Cintos',  lowBound=0, cat='Continuous')

# 3) Definir a função objetivo
model += 5 * x1 + 2 * x2, "Lucro_Total"

# 4) Adicionar restrições (divisões convertidas em multiplicações pelo inverso)
model += (1/6) * x1 + (1/5) * x2 <= 1,     "Restricao_Tempo"
model += 2 * x1 + 1 * x2     <= 6,         "Restricao_Couro"

# 5) Resolver com Simplex (solver padrão CBC)
model.solve()

# 6) Exibir resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print("Sapatos (x1) =", x1.varValue)
print("Cintos  (x2) =", x2.varValue)
print("Lucro Máximo = $", pulp.value(model.objective))

# 7) Visualizar região factível e solução ótima
x_vals = np.linspace(0, 6, 300)

# Limites das restrições em igualdade:
y_tempo = 5 * (1 - x_vals / 6)   # rearranjando (1/6)x1 + (1/5)x2 = 1 → x2 = 5*(1 - x1/6)
y_couro = 6 - 2 * x_vals         # 2x1 + x2 = 6 → x2 = 6 - 2x1

y_max = np.minimum(y_tempo, y_couro)
y_max = np.clip(y_max, 0, None)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_tempo, label='(1/6)x₁ + (1/5)x₂ = 1 (Tempo)', linewidth=2)
plt.plot(x_vals, y_couro, label='2x₁ + x₂ = 6 (Couro)',       linewidth=2)
plt.fill_between(x_vals, 0, y_max, color='gray', alpha=0.3, label='Região Factível')
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 6)
plt.ylim(0, 6)
plt.xlabel('Sapatos (x₁)')
plt.ylabel('Cintos  (x₂)')
plt.title('Exemplo 03 – Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# 8) Salvar o gráfico
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-02\q3\exercise3.png'
plt.savefig(output_path, dpi=300)
plt.show()
