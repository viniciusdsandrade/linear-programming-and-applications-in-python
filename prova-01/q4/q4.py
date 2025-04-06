import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma companhia produz dois tipos de camisas:
#   Manga longa: Lucro de R$5,00 por camisa.
#   Manga curta: Lucro de R$3,50 por camisa.
#
# Informações adicionais:
#   - Uma camisa de manga longa consome 50% a mais de mão-de-obra do que a de manga curta.
#   - Se toda a mão-de-obra fosse utilizada para camisas de manga curta, a produção seria de 400 unidades por dia.
#       -> Total de mão-de-obra disponível equivale a 400 unidades (em termos de camisas curtas).
#   - Restrição de mercado: máximo de 150 camisas de manga longa e 300 camisas de manga curta.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de camisas de manga longa a produzir
#   y = número de camisas de manga curta a produzir
#
# Função objetivo:
#   Max Z = 5*x + 3.5*y
#
# Restrições:
#   a) Mão-de-obra:
#         1.5*x + y <= 400
#
#   b) Mercado para manga longa:
#         x <= 150
#
#   c) Mercado para manga curta:
#         y <= 300
#
# Não negatividade:
#         x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Lucro)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio4_Maximizar_Lucro", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable('Manga_Longa', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Manga_Curta', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 5 * x + 3.5 * y, "Lucro_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de mão-de-obra:
model += 1.5 * x + y <= 400, "Restricao_Mao_de_Obra"

# Restrição de mercado:
model += x <= 150, "Restricao_Mercado_Manga_Longa"
model += y <= 300, "Restricao_Mercado_Manga_Curta"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Camisas de Manga Longa =", x.varValue)
print("Número de Camisas de Manga Curta =", y.varValue)
print("Lucro Máximo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a visualização, usamos x no eixo X (camisas de manga longa) e y no eixo Y (camisas de manga curta).
# As restrições importantes:
# (1) Mão-de-obra:   1.5*x + y <= 400  -> y <= 400 - 1.5*x
# (2) Mercado longa:  x <= 150
# (3) Mercado curta:  y <= 300

x_vals = np.linspace(0, 160, 300)
y_mao_de_obra = 400 - 1.5 * x_vals

# A região factível é definida pelo menor valor entre as restrições:
y_feasible = np.minimum(y_mao_de_obra, 300)
y_feasible = np.maximum(y_feasible, 0)  # Garantindo não-negatividade

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_mao_de_obra, label='1.5x + y = 400 (Mão-de-obra)')
plt.axvline(x=150, color='red', linestyle='--', label='x = 150 (Manga Longa)')
plt.axhline(y=300, color='green', linestyle='--', label='y = 300 (Manga Curta)')
plt.fill_between(x_vals, 0, y_feasible, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 160)
plt.ylim(0, 320)
plt.xlabel('Camisas de Manga Longa (x)')
plt.ylabel('Camisas de Manga Curta (y)')
plt.title('Exercício 4 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# Salvar o gráfico (altere o caminho se necessário)
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q4\exercise4.png')
plt.show()
