import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Duas fábricas (F1 e F2) produzem três tipos de papel: fino, médio e grosso.
#
# O contrato exige a produção diária de:
#   - 16 toneladas de papel fino
#   - 6 toneladas de papel médio
#   - 28 toneladas de papel grosso
#
# Custos de operação (por dia):
#   - Fábrica 1 (F1): R$ 1.000,00/dia
#   - Fábrica 2 (F2): R$ 2.000,00/dia
#
# Produção diária:
#   Fábrica 1:
#       - 8 toneladas de papel fino
#       - 1 tonelada de papel médio
#       - 2 toneladas de papel grosso
#
#   Fábrica 2:
#       - 2 toneladas de papel fino
#       - 1 tonelada de papel médio
#       - 7 toneladas de papel grosso
#
# Objetivo:
#   Determinar quantos dias cada fábrica deve operar para atender aos pedidos com o menor custo.
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x1 = número de dias que a Fábrica 1 opera (F1)
#   x2 = número de dias que a Fábrica 2 opera (F2)
#
# Função objetivo:
#   Min Z = 1000*x1 + 2000*x2
#
# Restrições de produção (para atender ou exceder os pedidos):
#   - Papel fino:   8*x1 + 2*x2 >= 16
#   - Papel médio:  x1 + x2   >= 6
#   - Papel grosso: 2*x1 + 7*x2 >= 28
#
# Não negatividade:
#   x1 >= 0, x2 >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Minimização)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exemplo_10", pulp.LpMinimize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# x1: número de dias que a Fábrica 1 opera
# x2: número de dias que a Fábrica 2 opera
# As variáveis são definidas como contínuas; se necessário, podem ser forçadas a inteiras.
x1 = pulp.LpVariable('Fabrica1_dias', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Fabrica2_dias', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# O objetivo é minimizar o custo total de operação:
#   Min Z = 1000*x1 + 2000*x2
model += 1000 * x1 + 2000 * x2, "Custo_Total"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Para atender aos pedidos, a produção deve ser, no mínimo:
#
# Papel fino: 8*x1 + 2*x2 >= 16
model += 8 * x1 + 2 * x2 >= 16, "Papel_Fino"

# Papel médio: x1 + x2 >= 6
model += x1 + x2 >= 6, "Papel_Medio"

# Papel grosso: 2*x1 + 7*x2 >= 28
model += 2 * x1 + 7 * x2 >= 28, "Papel_Grosso"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("x1 (Dias de Fábrica 1) =", x1.varValue)
print("x2 (Dias de Fábrica 2) =", x2.varValue)
print("Custo Mínimo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a plotagem, usamos x1 no eixo X e x2 no eixo Y. As restrições são:
#
# (1) Papel fino: 8*x1 + 2*x2 >= 16  --> x2 >= (16 - 8*x1)/2 = 8 - 4*x1
# (2) Papel médio: x1 + x2 >= 6       --> x2 >= 6 - x1
# (3) Papel grosso: 2*x1 + 7*x2 >= 28   --> x2 >= (28 - 2*x1)/7 = 4 - (2/7)*x1
#
# A região factível é a área em que x2 é maior ou igual ao maior desses valores (considerando x1, x2 >= 0).
x1_vals = np.linspace(0, 10, 300)  # Intervalo para x1 (0 a 10)

# Calcular as fronteiras das restrições:
x2_fino = 8 - 4 * x1_vals          # x2 >= 8 - 4*x1
x2_medio = 6 - x1_vals             # x2 >= 6 - x1
x2_grosso = 4 - (2 / 7) * x1_vals   # x2 >= 4 - (2/7)*x1

# Para cada valor de x1, o limite inferior efetivo para x2 é o máximo entre as três fronteiras e 0:
x2_feasible = np.maximum(np.maximum(x2_fino, x2_medio), x2_grosso)
x2_feasible = np.maximum(x2_feasible, 0)  # Garantir que x2 não seja negativo

# Criação da figura para a plotagem
plt.figure(figsize=(8, 6))

# Plotar as linhas das fronteiras das restrições
plt.plot(x1_vals, x2_fino, label='8x1 + 2x2 = 16 (Papel Fino)', color='blue')
plt.plot(x1_vals, x2_medio, label='x1 + x2 = 6 (Papel Médio)', color='red')
plt.plot(x1_vals, x2_grosso, label='2x1 + 7x2 = 28 (Papel Grosso)', color='green')

# Preencher a região factível (acima do maior limite inferior) até um limite de exibição (y=20)
plt.fill_between(x1_vals, x2_feasible, 20, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada pelo solver
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

# Configurar os limites dos eixos, rótulos e título
plt.xlim(0, 10)
plt.ylim(0, 20)
plt.xlabel('x1 (Dias de Fábrica 1)')
plt.ylabel('x2 (Dias de Fábrica 2)')
plt.title('Exemplo 10 - Região Factível e Solução Ótima (Minimização do Custo)')
plt.legend()
plt.grid(True)

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 2D no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
# com o nome 'exercise10.png'.
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise10.png')

# Exibir o gráfico
plt.show()
