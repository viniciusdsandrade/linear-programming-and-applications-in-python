import pulp  # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np  # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D
from mpl_toolkits.mplot3d import Axes3D  # Necessário para criar gráficos 3D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Uma metalúrgica produz três componentes para geladeira: A, B e C.
#
# Informações de produção:
# - Em 1 hora, se a metalúrgica produzir somente A, produzirá 25 unidades.
#   Se produzir somente B, produzirá 30 unidades; e se produzir somente C,
#   produzirá 40 unidades.
#
# Consumo de recursos para cada componente:
#   - Componente A: consome 40 unidades do recurso I e 30 do recurso II.
#   - Componente B: consome 25 unidades do recurso I e 15 do recurso II.
#   - Componente C: consome 18 unidades do recurso I e 10 do recurso II.
#
# Disponibilidades dos recursos:
#   - Recurso I: 712 unidades.
#   - Recurso II: 450 unidades.
#
# Lucro unitário de cada componente:
#   - A: R$25,00
#   - B: R$15,00
#   - C: R$11,00
#
# Objetivo:
# Determinar a quantidade de cada componente a ser produzida em 1 hora, de modo a
# maximizar o lucro total, respeitando as restrições de tempo e de recursos.
#
# Modelagem do problema:
# Variáveis de decisão:
#   xA = quantidade de componente A produzida em 1 hora
#   xB = quantidade de componente B produzida em 1 hora
#   xC = quantidade de componente C produzida em 1 hora
#
# Função objetivo:
#   Max Z = 25*xA + 15*xB + 11*xC
#
# Restrições:
#   (1) Tempo de produção:
#       (xA / 25) + (xB / 30) + (xC / 40) <= 1
#       -> Cada termo representa a fração de hora utilizada para produzir
#          a quantidade respectiva de cada componente.
#
#   (2) Recurso I:
#       40*xA + 25*xB + 18*xC <= 712
#
#   (3) Recurso II:
#       30*xA + 15*xB + 10*xC <= 450
#
#   (4) Não negatividade:
#       xA, xB, xC >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização
# -----------------------------------------------------------------------------
# Cria-se um objeto de problema com o nome "Exemplo_04", com o objetivo de maximizar
# a função lucro.
model = pulp.LpProblem("Exemplo_04", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# Define-se as variáveis:
#   xA: Quantidade de componente A produzida em 1 hora.
#   xB: Quantidade de componente B produzida em 1 hora.
#   xC: Quantidade de componente C produzida em 1 hora.
# Todas as variáveis são contínuas e possuem limite inferior 0.
xA = pulp.LpVariable('A', lowBound=0, cat='Continuous')
xB = pulp.LpVariable('B', lowBound=0, cat='Continuous')
xC = pulp.LpVariable('C', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# A função objetivo é maximizar o lucro total por hora, dado por:
# Lucro = 25*xA + 15*xB + 11*xC.
model += 25 * xA + 15 * xB + 11 * xC, "Lucro"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de tempo:
# Cada componente tem uma taxa de produção específica. Se a produção fosse
# exclusiva, o tempo total seria:
#   xA/25 para A, xB/30 para B e xC/40 para C.
# A soma dessas frações não pode exceder 1 hora.
model += (1 / 25) * xA + (1 / 30) * xB + (1 / 40) * xC <= 1, "Restricao_Tempo"

# Restrição de Recurso I:
# O consumo total de recurso I pela produção deve ser menor ou igual a 712 unidades.
model += 40 * xA + 25 * xB + 18 * xC <= 712, "Restricao_Rec_I"

# Restrição de Recurso II:
# O consumo total de recurso II pela produção deve ser menor ou igual a 450 unidades.
model += 30 * xA + 15 * xB + 10 * xC <= 450, "Restricao_Rec_II"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
# Utiliza-se o método solve() para encontrar a solução ótima que maximiza o lucro,
# respeitando todas as restrições impostas.
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
# Imprime-se o status da solução (por exemplo, "Ótimo"), os valores ótimos das variáveis,
# e o lucro máximo obtido.
print("Status da solução:", pulp.LpStatus[model.status])
print("xA (A) =", xA.varValue)
print("xB (B) =", xB.varValue)
print("xC (C) =", xC.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 3D
# -----------------------------------------------------------------------------
# Para visualizar a região factível, definimos intervalos razoáveis para xA, xB e xC.
# Os intervalos foram escolhidos com base nas restrições de tempo e recursos:
#   - Se a produção fosse exclusiva:
#       xA <= 25, xB <= 30, xC <= 40 (pela restrição de tempo).
#   - Considerando os recursos, escolhemos:
#       xA de 0 a 20, xB de 0 a 30, xC de 0 a 40.
xA_range = np.arange(0, 21, 1)  # Intervalo para xA: 0 a 20
xB_range = np.arange(0, 31, 1)  # Intervalo para xB: 0 a 30
xC_range = np.arange(0, 41, 1)  # Intervalo para xC: 0 a 40

# Lista para armazenar os pontos que satisfazem todas as restrições
feasible_points = []

# Varre todos os pontos definidos pelos intervalos de xA, xB e xC
for a in xA_range:
    for b in xB_range:
        for c in xC_range:
            # Verifica se o ponto satisfaz a restrição de tempo
            cond_tempo = (a / 25) + (b / 30) + (c / 40) <= 1
            # Verifica se o ponto satisfaz a restrição de Recurso I
            cond_rI = 40 * a + 25 * b + 18 * c <= 712
            # Verifica se o ponto satisfaz a restrição de Recurso II
            cond_rII = 30 * a + 15 * b + 10 * c <= 450
            # Se todas as condições forem satisfeitas, o ponto é factível
            if cond_tempo and cond_rI and cond_rII:
                feasible_points.append((a, b, c))

# Converte a lista de pontos factíveis para um array NumPy para facilitar a plotagem
feasible_points = np.array(feasible_points)

# Cria a figura para o gráfico 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plota os pontos que compõem a região factível em cinza
ax.scatter(
    feasible_points[:, 0],  # Valores de xA
    feasible_points[:, 1],  # Valores de xB
    feasible_points[:, 2],  # Valores de xC
    s=5,  # Tamanho dos marcadores
    color='gray',  # Cor dos pontos
    alpha=0.3,  # Transparência para visualização
    label='Região Factível'
)

# Destaca a solução ótima encontrada com um marcador vermelho maior
ax.scatter(
    [xA.varValue], [xB.varValue], [xC.varValue],
    color='red', s=80, label='Solução Ótima'
)

# Configura os rótulos dos eixos
ax.set_xlabel('xA (A por hora)')
ax.set_ylabel('xB (B por hora)')
ax.set_zlabel('xC (C por hora)')

# Define o título do gráfico
ax.set_title('Região Factível (Exemplo 04) e Solução Ótima')

# Adiciona a legenda ao gráfico
ax.legend()

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 3D com o nome 'exercise04.png' no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise04.png')

# Exibe o gráfico na tela
plt.show()
