import pulp  # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np  # Biblioteca para cálculos numéricos e manipulação de arrays
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Um sapateiro fabrica sapatos e cintos. As informações do problema são:
# - Se trabalhar exclusivamente com sapatos: produz 6 sapatos/hora.
# - Se trabalhar exclusivamente com cintos: produz 5 cintos/hora.
# - Cada sapato consome 2 unidades de couro; cada cinto consome 1 unidade de couro.
# - O total disponível de couro é de 6 unidades.
# - Lucro unitário: R$5,00 por sapato e R$2,00 por cinto.
#
# O objetivo é maximizar o lucro por hora, determinando a quantidade de sapatos (x1)
# e cintos (x2) que devem ser produzidos, respeitando as seguintes restrições:
#   1) Tempo de produção: a fração do tempo utilizada para produzir sapatos e cintos,
#      somada, não pode exceder 1 hora. Isto é, (x1/6 + x2/5) <= 1.
#   2) Consumo de couro: o couro total consumido (2*x1 + x2) não pode ultrapassar
#      as 6 unidades disponíveis.
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização
# -----------------------------------------------------------------------------
# Criamos um objeto de problema com o objetivo de maximizar o lucro por hora.
model = pulp.LpProblem("Exemplo_03", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# Definimos as variáveis:
#   x1: número de sapatos produzidos por hora.
#   x2: número de cintos produzidos por hora.
# As variáveis são contínuas e não podem assumir valores negativos (lowBound=0).
x1 = pulp.LpVariable('Sapatos', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Cintos', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# A função objetivo visa maximizar o lucro por hora, calculado como:
# Lucro = 5*x1 + 2*x2.
model += 5 * x1 + 2 * x2, "Lucro_por_hora"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de tempo:
# Se o sapateiro produzir x1 sapatos, ele utiliza x1/6 horas (6 sapatos/hora),
# e se produzir x2 cintos, ele utiliza x2/5 horas (5 cintos/hora). Assim,
# a soma dos tempos não pode exceder 1 hora.
model += (1 / 6) * x1 + (1 / 5) * x2 <= 1, "Restricao_de_tempo"

# Restrição de couro:
# Cada sapato utiliza 2 unidades de couro e cada cinto 1 unidade. Portanto,
# o total de couro consumido (2*x1 + x2) deve ser menor ou igual a 6 unidades.
model += 2 * x1 + x2 <= 6, "Restricao_de_couro"

# =============================================================================
# 5) Resolver o problema de otimização
# -----------------------------------------------------------------------------
# O método solve() do PuLP encontra a solução ótima que maximiza o lucro,
# respeitando as restrições impostas.
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
# Imprime o status da solução, os valores ótimos para as variáveis e o lucro máximo.
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 (Sapatos) =", x1.varValue)
print("x2 (Cintos)  =", x2.varValue)
print("Lucro máximo por hora = $", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima
# -----------------------------------------------------------------------------
# Para visualizar a região factível em 2D, definimos um intervalo de valores para x1
# e calculamos os limites de x2 para cada restrição:
# - Para a restrição de tempo:
#     x1/6 + x2/5 <= 1  =>  x2 <= 5*(1 - x1/6) = 5 - (5/6)*x1
# - Para a restrição de couro:
#     2*x1 + x2 <= 6  =>  x2 <= 6 - 2*x1
x1_vals = np.linspace(0, 6, 200)  # Vetor de 200 pontos entre 0 e 6

# Calcula os limites superiores de x2 para cada restrição:
x2_tempo = 5 - (5 / 6) * x1_vals
x2_couro = 6 - 2 * x1_vals

# Configura a figura do gráfico
plt.figure(figsize=(8, 6))

# Plota a curva da restrição de tempo (em azul)
plt.plot(x1_vals, x2_tempo, label='x1/6 + x2/5 = 1', color='blue')

# Plota a curva da restrição de couro (em vermelho)
plt.plot(x1_vals, x2_couro, label='2*x1 + x2 = 6', color='red')

# Determina a região factível, que é limitada pelo mínimo dos limites de x2 das restrições
x2_feasible = np.minimum(x2_tempo, x2_couro)
x2_feasible = np.maximum(x2_feasible, 0)  # Garante que x2 não seja negativo
plt.fill_between(x1_vals, x2_feasible, color='gray', alpha=0.3, label='Região Factível')

# Destaca a solução ótima encontrada com um marcador preto
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

# Configura os limites dos eixos para melhor visualização
plt.xlim(0, 6)
plt.ylim(0, 6)

# Adiciona rótulos e título
plt.xlabel('x1 (Sapatos por hora)')
plt.ylabel('x2 (Cintos por hora)')
plt.title('Região Factível (Exemplo 03) e Solução Ótima')
plt.legend()
plt.grid(True)

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico antes de exibi-lo, garantindo que a figura completa seja gravada.
# O caminho completo para o arquivo é especificado com uma string bruta para evitar
# problemas com as barras invertidas.
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise03.png')

# Exibe o gráfico na tela
plt.show()
