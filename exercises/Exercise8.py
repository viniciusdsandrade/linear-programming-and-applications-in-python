import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D
from mpl_toolkits.mplot3d import Axes3D  # Módulo para gráficos 3D (caso queira usar)

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma companhia fabrica dois produtos: P1 e P2. Ambos usam os mesmos recursos
# produtivos: matéria-prima, forjaria e polimento.
#
# Cada unidade de P1 requer:
#   - 4 horas de forja
#   - 2 horas de polimento
#   - 100 unidades de matéria-prima
#   - preço (receita) de R$ 1.900,00
#
# Cada unidade de P2 requer:
#   - 2 horas de forja
#   - 3 horas de polimento
#   - 200 unidades de matéria-prima
#   - preço (receita) de R$ 2.100,00
#
# As disponibilidades diárias são:
#   - Forja: 20 horas
#   - Polimento: 10 horas
#   - Matéria-prima: 500 unidades
#
# Objetivo:
#   Determinar quantidades x1 (P1) e x2 (P2) que maximizem a receita total.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#   Variáveis de decisão:
#       x1 >= 0  (unidades de P1)
#       x2 >= 0  (unidades de P2)
#
#   Função Objetivo (maximizar receita):
#       Max Z = 1900*x1 + 2100*x2
#
#   Restrições:
#       (1) Forja: 4*x1 + 2*x2 <= 20
#       (2) Polimento: 2*x1 + 3*x2 <= 10
#       (3) Matéria-prima: 100*x1 + 200*x2 <= 500
#       (4) x1 >= 0, x2 >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximizar)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exemplo_08", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# x1: quantidade a produzir de P1
# x2: quantidade a produzir de P2
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# Max Z = 1900*x1 + 2100*x2
model += 1900 * x1 + 2100 * x2, "Receita"

# =============================================================================
# 4) Adicionar as restrições
# -----------------------------------------------------------------------------
# Forja: 4*x1 + 2*x2 <= 20
model += 4 * x1 + 2 * x2 <= 20, "Restricao_Forja"

# Polimento: 2*x1 + 3*x2 <= 10
model += 2 * x1 + 3 * x2 <= 10, "Restricao_Polimento"

# Matéria-prima: 100*x1 + 200*x2 <= 500
model += 100 * x1 + 200 * x2 <= 500, "Restricao_MateriaPrima"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 (P1) =", x1.varValue)
print("x2 (P2) =", x2.varValue)
print("Receita máxima = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para o gráfico, definimos um intervalo para x1 e calculamos os limites de x2
# com base em cada restrição. Em seguida, preenchemos a região factível.

x1_vals = np.linspace(0, 6, 200)  # Intervalo para x1 (0 a 6, com 200 pontos)

# Isolar x2 em cada restrição:
# Forja: 4*x1 + 2*x2 <= 20  =>  x2 <= (20 - 4*x1) / 2
x2_forja = (20 - 4 * x1_vals) / 2

# Polimento: 2*x1 + 3*x2 <= 10 => x2 <= (10 - 2*x1) / 3
x2_polimento = (10 - 2 * x1_vals) / 3

# Matéria-prima: 100*x1 + 200*x2 <= 500 => x2 <= (500 - 100*x1) / 200 => 2.5 - 0.5*x1
x2_materia = 2.5 - 0.5 * x1_vals

# Garantir que x2 não seja negativo
x2_min_forja = np.maximum(0, x2_forja)
x2_min_polimento = np.maximum(0, x2_polimento)
x2_min_materia = np.maximum(0, x2_materia)

# A fronteira factível de x2 é o menor valor dentre as três restrições
x2_feasible = np.minimum(x2_min_forja, np.minimum(x2_min_polimento, x2_min_materia))

# Criação da figura
plt.figure(figsize=(8, 6))

# Plotar as linhas de cada restrição
plt.plot(x1_vals, x2_forja, label='4x1 + 2x2 = 20 (Forja)', color='blue')
plt.plot(x1_vals, x2_polimento, label='2x1 + 3x2 = 10 (Polimento)', color='green')
plt.plot(x1_vals, x2_materia, label='100x1 + 200x2 = 500 (Matéria-prima)', color='red')

# Preencher a região factível
plt.fill_between(x1_vals, x2_feasible, color='gray', alpha=0.3, label='Região Factível')

# Plotar a solução ótima
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

# Ajustar os limites dos eixos
plt.xlim(0, 6)
plt.ylim(0, 6)

# Rótulos e título do gráfico
plt.xlabel('x1 (P1)')
plt.ylabel('x2 (P2)')
plt.title('Região Factível (Exemplo 08) e Solução Ótima')
plt.legend()
plt.grid(True)

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 2D no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
# com o nome 'exercise08.png'.
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise08.png'
)

# Exibe o gráfico na tela
plt.show()
