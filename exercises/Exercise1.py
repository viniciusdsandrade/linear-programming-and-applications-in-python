# [RESUMO DO PROBLEMA]
# Certa empresa fabrica dois produtos P1 e P2
# O lucro unitário do produto P1 é de R$ 1.000,00 e o
# lucro unitário de P2 é R$ 1.800,00
# A empresa precisa de 20 horas para fabricar uma unidade de P1 e de 30 horas para fabricar uma unidade de P2.
# O tempo anual de produção disponível para isso é de 1200 horas.
# A demanda esperada para cada produto é de 40 unidades para P1 e 30 unidades para P2
#
# Construa o modelo de programação linear que
#
# objetiva Maximizar o lucro


# Modelo de Programação Linear para maximizar o lucro ao fabricar P1 e P2:
#    Max Z = 1000*x1 + 1800*x2
# Sujeito às restrições:
#    20*x1 + 30*x2 ≤ 1200   (tempo de produção)
#    x1 ≤ 40               (demanda de P1)
#    x2 ≤ 30               (demanda de P2)
#    x1 ≥ 0, x2 ≥ 0

# [CÓDIGO COMPLETO EM PYTHON COM SOLUÇÃO E GRÁFICO]

import pulp                   # Importa a biblioteca PuLP para modelagem e solução de problemas de programação linear
import numpy as np            # Importa o NumPy para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Importa o Matplotlib para criação de gráficos

# ============================================================================
# 1) Definir o problema
# ----------------------------------------------------------------------------
# Criamos um problema de otimização chamado "Exemplo_01" que terá o objetivo de
# maximizar a função lucro. A opção 'pulp.LpMaximize' indica que o problema é
# de maximização.
model = pulp.LpProblem("Exemplo_01", pulp.LpMaximize)

# ============================================================================
# 2) Criar variáveis
# ----------------------------------------------------------------------------
# Neste passo definimos as variáveis de decisão:
# - x1: Quantidade a produzir do produto P1
# - x2: Quantidade a produzir do produto P2
# Ambas são definidas como variáveis contínuas com limite inferior igual a 0.
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')

# ============================================================================
# 3) Definir a função objetivo
# ----------------------------------------------------------------------------
# A função objetivo representa o lucro total que desejamos maximizar.
# Cada unidade de P1 gera um lucro de R$ 1.000,00 e cada unidade de P2 gera R$ 1.800,00.
# Assim, a função é definida como: Lucro = 1000*x1 + 1800*x2.
model += 1000 * x1 + 1800 * x2, "Lucro"

# ============================================================================
# 4) Adicionar restrições
# ----------------------------------------------------------------------------
# Aqui adicionamos as restrições do problema para refletir os limites reais da produção.

# Restrição de tempo de produção:
# Cada unidade de P1 requer 20 horas e cada unidade de P2 requer 30 horas, com um total
# máximo de 1200 horas disponíveis.
model += 20 * x1 + 30 * x2 <= 1200, "Restricao_tempo"

# Restrição de demanda para o produto P1:
# Não é possível produzir mais do que a demanda esperada, que é de 40 unidades.
model += x1 <= 40, "Restricao_demanda_P1"

# Restrição de demanda para o produto P2:
# Não é possível produzir mais do que a demanda esperada, que é de 30 unidades.
model += x2 <= 30, "Restricao_demanda_P2"

# ============================================================================
# 5) Resolver o modelo
# ----------------------------------------------------------------------------
# O método solve() é utilizado para encontrar a solução ótima (maximização do lucro)
# que satisfaz todas as restrições definidas.
model.solve()

# ============================================================================
# 6) Mostrar resultados
# ----------------------------------------------------------------------------
# Após a resolução, imprimimos o status da solução, os valores ótimos das variáveis
# x1 e x2, e o valor máximo do lucro obtido.
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 =", x1.varValue)
print("x2 =", x2.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# ============================================================================
# 7) Plotar a região factível e a solução ótima
# ----------------------------------------------------------------------------
# Nesta seção, utilizamos o Matplotlib para visualizar graficamente a região
# factível do problema e destacar a solução ótima encontrada.

# Geração de valores para x1: cria um vetor de 200 pontos entre 0 e 40 (limite de P1)
x1_vals = np.linspace(0, 40, 200)

# Cálculo dos valores correspondentes de x2 que satisfazem a restrição de tempo:
# Rearranjamos a equação da restrição: 20*x1 + 30*x2 = 1200  =>  x2 = (1200 - 20*x1) / 30
x2_from_time = (1200 - 20 * x1_vals) / 30

# Configura o tamanho da figura do gráfico
plt.figure(figsize=(8, 6))

# Plota a linha da restrição de tempo, representando a equação 20x1 + 30x2 = 1200
plt.plot(x1_vals, x2_from_time, label='20x1 + 30x2 = 1200', color='blue')

# Plota uma linha vertical que representa o limite de demanda para P1 (x1 = 40)
plt.axvline(x=40, color='red', label='x1 = 40')

# Plota uma linha horizontal que representa o limite de demanda para P2 (x2 = 30)
plt.hlines(y=30, xmin=0, xmax=40, color='green', label='x2 = 30')

# Define a região factível para x2, considerando que x2 não pode ultrapassar o valor
# calculado pela restrição de tempo e nem o valor máximo de 30 unidades.
x2_feasible = np.minimum(x2_from_time, 30)
x2_feasible = np.maximum(x2_feasible, 0)

# Preenche a área da região factível com uma cor cinza semitransparente
plt.fill_between(x1_vals, x2_feasible, color='gray', alpha=0.3)

# Destaca a solução ótima encontrada, colocando um ponto preto no gráfico
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

# Configura os limites dos eixos para melhor visualização
plt.xlim(0, 45)
plt.ylim(0, 35)

# Define os rótulos dos eixos x e y
plt.xlabel('x1')
plt.ylabel('x2')

# Define o título do gráfico
plt.title('Região Factível e Solução Ótima')

# Adiciona uma legenda para identificar os elementos do gráfico
plt.legend()

# Adiciona uma grade ao gráfico para facilitar a leitura dos valores
plt.grid(True)

# ============================================================================
# Salvar o gráfico
# ----------------------------------------------------------------------------
# Salva o gráfico no diretório especificado com o nome 'exercise01.png'.
# Atenção: plt.savefig() deve ser chamado antes de plt.show() para garantir que o
# gráfico seja salvo corretamente.
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise01.png')

# Exibe o gráfico na tela
plt.show()
