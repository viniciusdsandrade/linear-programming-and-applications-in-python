import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# A indústria Alumilâminas S/A possui duas fábricas: uma em São Paulo e outra no Rio de Janeiro.
#
# Necessidades contratuais:
#   - Lâminas finas:   16 toneladas
#   - Lâminas médias:   6 toneladas
#   - Lâminas grossas:  28 toneladas
#
# Produção diária de cada fábrica:
#   Fábrica de São Paulo:
#       - Finas:   8 toneladas
#       - Médias:  1 tonelada
#       - Grossas: 2 toneladas
#       Custo diário: R$100.000,00
#
#   Fábrica do Rio de Janeiro:
#       - Finas:   2 toneladas
#       - Médias:  1 tonelada
#       - Grossas: 7 toneladas
#       Custo diário: R$200.000,00
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de dias de operação da fábrica de São Paulo
#   y = número de dias de operação da fábrica do Rio de Janeiro
#
# Função objetivo:
#   Min Z = 100000*x + 200000*y
#
# Restrições:
#   a) Lâminas finas:   8*x + 2*y >= 16
#   b) Lâminas médias:   x + y >= 6
#   c) Lâminas grossas:  2*x + 7*y >= 28
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Minimização do Custo)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio6_Minimizar_Custo", pulp.LpMinimize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable('Dias_SP', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Dias_RJ', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += 100000 * x + 200000 * y, "Custo_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Lâminas finas: 8*x + 2*y >= 16
model += 8 * x + 2 * y >= 16, "Restricao_Finas"

# Lâminas médias: x + y >= 6
model += x + y >= 6, "Restricao_Medias"

# Lâminas grossas: 2*x + 7*y >= 28
model += 2 * x + 7 * y >= 28, "Restricao_Grossas"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Dias de operação da fábrica de São Paulo =", x.varValue)
print("Dias de operação da fábrica do Rio de Janeiro =", y.varValue)
print("Custo Mínimo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a visualização, usamos x no eixo X e y no eixo Y.
# As restrições são:
# (1) Lâminas finas:   8*x + 2*y >= 16   --> y >= (16 - 8*x)/2 = 8 - 4*x
# (2) Lâminas médias:   x + y >= 6         --> y >= 6 - x
# (3) Lâminas grossas:  2*x + 7*y >= 28      --> y >= (28 - 2*x)/7 = 4 - (2/7)*x
#
# A região factível é a interseção dos conjuntos em que cada restrição é satisfeita.

x_vals = np.linspace(0, 10, 300)
y_finas   = 8 - 4 * x_vals
y_medias  = 6 - x_vals
y_grossas = 4 - (2/7) * x_vals

# Para cada valor de x, o limite inferior efetivo para y é o máximo entre as três expressões e 0:
y_feasible = np.maximum(np.maximum(y_finas, y_medias), y_grossas)
y_feasible = np.maximum(y_feasible, 0)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_finas, label='8x + 2y = 16 (Finas)')
plt.plot(x_vals, y_medias, label='x + y = 6 (Médias)')
plt.plot(x_vals, y_grossas, label='2x + 7y = 28 (Grossas)')
plt.fill_between(x_vals, y_feasible, 20, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 10)
plt.ylim(0, 20)
plt.xlabel('Dias de operação em São Paulo (x)')
plt.ylabel('Dias de operação no Rio de Janeiro (y)')
plt.title('Exercício 6 - Região Factível e Solução Ótima (Minimização do Custo)')
plt.legend()
plt.grid(True)

# Salvar o gráfico no diretório especificado
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q6\exercise6.png')
plt.show()
