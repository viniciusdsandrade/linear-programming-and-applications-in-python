import pulp                   # Biblioteca para modelagem e solução de problemas de programação linear
import numpy as np            # Biblioteca para cálculos numéricos e manipulação de arrays
import matplotlib.pyplot as plt  # Biblioteca para geração de gráficos 2D
from mpl_toolkits.mplot3d import Axes3D  # Módulo necessário para criação de gráficos 3D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma empresa de informática possui 25 engenheiros e 40 técnicos. Ela venceu uma
# concorrência para instalar o sistema de computação de um "edifício inteligente".
# Para isso, a empresa definiu três tipos de equipes com composições diferentes:
#
#   Tipo I: 2 engenheiros e 6 técnicos
#   Tipo II: 4 engenheiros e 8 técnicos
#   Tipo III: 3 engenheiros e 9 técnicos
#
# Cada equipe gera, diariamente, uma receita:
#   - Equipe Tipo I: R$ 2000,00
#   - Equipe Tipo II: R$ 3000,00
#   - Equipe Tipo III: R$ 2800,00
#
# O objetivo é determinar quantas equipes de cada tipo a empresa deve empregar para
# maximizar a receita, sem exceder o número disponível de engenheiros e técnicos.
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização
# -----------------------------------------------------------------------------
# Cria um objeto do tipo problema de programação linear, especificando que
# o objetivo é maximizar a função receita.
model = pulp.LpProblem("Exemplo_02", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# As variáveis representam a quantidade de equipes de cada tipo a ser empregada.
# x1: Número de equipes do Tipo I
# x2: Número de equipes do Tipo II
# x3: Número de equipes do Tipo III
# Todas as variáveis são contínuas e possuem limite inferior igual a 0.
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# A função objetivo é maximizar a receita total obtida pela formação das equipes.
# Receita total = 2000*x1 + 3000*x2 + 2800*x3
model += 2000 * x1 + 3000 * x2 + 2800 * x3, "Receita"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# As restrições refletem a disponibilidade de mão de obra da empresa.

# Restrição de engenheiros:
# Cada equipe do Tipo I consome 2 engenheiros, do Tipo II consome 4 e do Tipo III consome 3.
# O total de engenheiros disponíveis é 25.
model += 2 * x1 + 4 * x2 + 3 * x3 <= 25, "Restricao_Engenheiros"

# Restrição de técnicos:
# Cada equipe do Tipo I consome 6 técnicos, do Tipo II consome 8 e do Tipo III consome 9.
# O total de técnicos disponíveis é 40.
model += 6 * x1 + 8 * x2 + 9 * x3 <= 40, "Restricao_Tecnicos"

# =============================================================================
# 5) Resolver o problema de otimização
# -----------------------------------------------------------------------------
# O método solve() encontra a solução ótima que maximiza a receita, respeitando
# as restrições impostas.
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
# Imprime o status da solução, os valores ótimos das variáveis e a receita máxima.
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 =", x1.varValue)
print("x2 =", x2.varValue)
print("x3 =", x3.varValue)
print("Receita máxima = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 3D
# -----------------------------------------------------------------------------
# Para ilustrar a região factível, vamos varrer uma malha de pontos em torno dos
# possíveis valores de x1, x2 e x3. Os intervalos escolhidos (0<=x1<=~7, 0<=x2<=~6,
# 0<=x3<=~5) são uma aproximação que abrange a região de interesse.
x1_range = np.arange(0, 7, 0.25)  # Valores para x1 com incremento de 0.25
x2_range = np.arange(0, 6, 0.25)  # Valores para x2 com incremento de 0.25
x3_range = np.arange(0, 5, 0.25)  # Valores para x3 com incremento de 0.25

# Lista para armazenar os pontos que satisfazem as restrições
feasible_points = []

# Percorre todos os pontos possíveis dentro dos intervalos definidos
for xv1 in x1_range:
    for xv2 in x2_range:
        for xv3 in x3_range:
            # Verifica se o ponto satisfaz a restrição de engenheiros
            c1 = (2 * xv1 + 4 * xv2 + 3 * xv3 <= 25)
            # Verifica se o ponto satisfaz a restrição de técnicos
            c2 = (6 * xv1 + 8 * xv2 + 9 * xv3 <= 40)
            # Se ambos os critérios forem satisfeitos, adiciona o ponto à lista
            if c1 and c2:
                feasible_points.append((xv1, xv2, xv3))

# Converte a lista de pontos factíveis em um array NumPy para facilitar o plot
feasible_points = np.array(feasible_points)

# Cria uma figura para o gráfico 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plota os pontos que compõem a região factível
ax.scatter(
    feasible_points[:, 0],  # Coordenada x1
    feasible_points[:, 1],  # Coordenada x2
    feasible_points[:, 2],  # Coordenada x3
    s=5,                    # Tamanho do marcador
    color='gray',           # Cor dos pontos
    alpha=0.3,              # Transparência para melhor visualização
    label='Região Factível'
)

# Destaca a solução ótima encontrada com um marcador maior e de cor vermelha
ax.scatter(
    [x1.varValue], [x2.varValue], [x3.varValue],
    color='red', s=80, label='Solução Ótima'
)

# Configura os rótulos dos eixos
ax.set_xlabel('x1 (Equipes Tipo I)')
ax.set_ylabel('x2 (Equipes Tipo II)')
ax.set_zlabel('x3 (Equipes Tipo III)')

# Define o título do gráfico
ax.set_title('Região Factível (Exemplo 02) e Solução Ótima')

# Antes de chamar plt.show(), salvamos o gráfico no diretório estipulado.
# Certifique-se de que o diretório já existe e que você possui permissão para gravar.
plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise02.png')

# Exibe o gráfico na tela
plt.show()
