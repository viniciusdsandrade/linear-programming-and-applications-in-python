import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Um alfaiate possui:
#   - 16 metros de algodão,
#   - 11 metros de seda,
#   - 15 metros de lã.
#
# Para produzir um terno são necessários:
#   - 2 m de algodão, 1 m de seda e 1 m de lã.
#
# Para produzir um vestido são necessários:
#   - 1 m de algodão, 2 m de seda e 3 m de lã.
#
# Os preços de venda são:
#   - Terno: R$300,00
#   - Vestido: R$500,00
#
# Objetivo:
#   Determinar quantos ternos (x) e vestidos (y) produzir para maximizar o lucro.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de ternos
#   y = número de vestidos
#
# Função objetivo:
#   Max Z = 300*x + 500*y
#
# Restrições:
#   - Algodão: 2*x + y <= 16
#   - Seda:    x + 2*y <= 11
#   - Lã:      x + 3*y <= 15
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Lucro)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio1_Maximizar_Lucro", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# x: número de ternos produzidos
# y: número de vestidos produzidos
# As variáveis são definidas como contínuas; se necessário, podem ser forçadas a inteiras.
x = pulp.LpVariable('Ternos', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Vestidos', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# O objetivo é maximizar o lucro total:
#   Max Z = 300*x + 500*y
model += 300 * x + 500 * y, "Lucro_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de algodão: 2*x + y <= 16
model += 2 * x + y <= 16, "Restricao_Algodao"

# Restrição de seda: x + 2*y <= 11
model += x + 2 * y <= 11, "Restricao_Seda"

# Restrição de lã: x + 3*y <= 15
model += x + 3 * y <= 15, "Restricao_La"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Ternos a Produzir =", x.varValue)
print("Número de Vestidos a Produzir =", y.varValue)
print("Lucro Máximo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a plotagem, usamos x (ternos) no eixo X e y (vestidos) no eixo Y.
# As restrições transformadas para igualdade são:
# (1) Algodão:   y = 16 - 2*x
# (2) Seda:      y = (11 - x)/2
# (3) Lã:        y = (15 - x)/3
#
# Para cada valor de x, a região factível é definida pelo menor limite superior de y.
x_vals = np.linspace(0, 10, 300)

# Calcular os limites de y para cada restrição:
y_algodao = 16 - 2 * x_vals       # y <= 16 - 2*x
y_seda = (11 - x_vals) / 2        # y <= (11 - x)/2
y_la = (15 - x_vals) / 3          # y <= (15 - x)/3

# A região factível será o conjunto onde y é menor ou igual ao menor desses valores:
y_max = np.minimum(np.minimum(y_algodao, y_seda), y_la)
y_max = np.maximum(y_max, 0)  # Garantir que y não seja negativo

# Criação da figura para a plotagem
plt.figure(figsize=(8, 6))

# Plotar as linhas das restrições
plt.plot(x_vals, y_algodao, label='2x + y = 16 (Algodão)', color='blue')
plt.plot(x_vals, y_seda, label='x + 2y = 11 (Seda)', color='red')
plt.plot(x_vals, y_la, label='x + 3y = 15 (Lã)', color='green')

# Preencher a região factível (abaixo do menor limite superior)
plt.fill_between(x_vals, 0, y_max, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x.varValue, y.varValue, color='black', zorder=5, label='Solução Ótima')

# Configurar os limites dos eixos, rótulos e título
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('Número de Ternos (x)')
plt.ylabel('Número de Vestidos (y)')
plt.title('Exercício 1 - Região Factível e Solução Ótima (Maximização do Lucro)')
plt.legend()
plt.grid(True)

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 2D no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
# com o nome 'exercise1.png'.
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q1\exercise1.png')

# Exibir o gráfico
plt.show()
