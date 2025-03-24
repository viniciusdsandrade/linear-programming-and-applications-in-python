import pulp  # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np  # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D
from mpl_toolkits.mplot3d import Axes3D  # Necessário para criar gráficos 3D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# A empresa Óleos Unidos S.A. fabrica três tipos de combustíveis especiais (A, B e C)
# utilizando dois insumos: extrato mineral e solvente. O processo de produção não
# apresenta perdas, ou seja, a quantidade de insumos utilizada resulta exatamente
# na quantidade produzida do combustível, conforme as seguintes proporções (por lote):
#
#   - Combustível A: 8 L de extrato mineral + 5 L de solvente  => Total de 13 L
#   - Combustível B: 5 L de extrato mineral + 4 L de solvente  => Total de 9 L
#   - Combustível C: 4 L de extrato mineral + 2 L de solvente  => Total de 6 L
#
# Recursos disponíveis:
#   - 120 L de extrato mineral
#   - 200 L de solvente
#
# Lucros por lote produzido:
#   - A: R$20,00
#   - B: R$22,00
#   - C: R$18,00
#
# Objetivo:
# Determinar a quantidade de lotes de combustíveis A, B e C a serem produzidos para
# maximizar o lucro total, respeitando as restrições de insumos.
#
# Modelagem do problema:
# Variáveis de decisão:
#   xA = quantidade de lotes de combustível A a produzir
#   xB = quantidade de lotes de combustível B a produzir
#   xC = quantidade de lotes de combustível C a produzir
#
# Função Objetivo:
#   Max Z = 20*xA + 22*xB + 18*xC
#
# Restrições:
#   (1) Extrato mineral: 8*xA + 5*xB + 4*xC <= 120
#   (2) Solvente:        5*xA + 4*xB + 2*xC <= 200
#   (3) Não negatividade: xA, xB, xC >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização
# -----------------------------------------------------------------------------
# Cria um objeto do problema "Exemplo_05" com o objetivo de maximizar o lucro.
model = pulp.LpProblem("Exemplo_05", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# Define as variáveis:
#   xA: número de lotes de combustível A a produzir.
#   xB: número de lotes de combustível B a produzir.
#   xC: número de lotes de combustível C a produzir.
# Todas as variáveis são contínuas e não podem assumir valores negativos (lowBound=0).
xA = pulp.LpVariable('A', lowBound=0, cat='Continuous')
xB = pulp.LpVariable('B', lowBound=0, cat='Continuous')
xC = pulp.LpVariable('C', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# A função objetivo visa maximizar o lucro total por lote:
# Lucro = 20*xA + 22*xB + 18*xC
model += 20 * xA + 22 * xB + 18 * xC, "Lucro"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de extrato mineral:
# Cada lote de combustível A consome 8 L, B consome 5 L e C consome 4 L.
# O total consumido não pode exceder 120 L.
model += 8 * xA + 5 * xB + 4 * xC <= 120, "Extrato_mineral"

# Restrição de solvente:
# Cada lote de combustível A consome 5 L, B consome 4 L e C consome 2 L.
# O total consumido não pode exceder 200 L.
model += 5 * xA + 4 * xB + 2 * xC <= 200, "Solvente"

# =============================================================================
# 5) Resolver o problema de otimização
# -----------------------------------------------------------------------------
# O método solve() encontra a solução ótima que maximiza o lucro,
# respeitando as restrições impostas.
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
# Imprime o status da solução (por exemplo, "Ótimo"), os valores ótimos das variáveis
# e o lucro máximo obtido.
print("Status da solução:", pulp.LpStatus[model.status])
print("xA (Combustível A) =", xA.varValue)
print("xB (Combustível B) =", xB.varValue)
print("xC (Combustível C) =", xC.varValue)
print("Lucro máximo = R$", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 3D
# -----------------------------------------------------------------------------
# Para visualizar a região factível, definimos intervalos para as variáveis com base
# nas restrições:
#   - Se produzir somente A: 8*xA <= 120  -> xA <= 15
#   - Se produzir somente B: 5*xB <= 120  -> xB <= 24
#   - Se produzir somente C: 4*xC <= 120  -> xC <= 30
#
# Para abranger uma gama um pouco maior, definimos:
xA_range = np.arange(0, 21, 1)  # xA de 0 a 20
xB_range = np.arange(0, 26, 1)  # xB de 0 a 25
xC_range = np.arange(0, 36, 1)  # xC de 0 a 35

# Lista para armazenar os pontos factíveis que satisfazem todas as restrições
feasible_points = []

# Varre os intervalos de xA, xB e xC e verifica as condições de cada restrição
for a in xA_range:
    for b in xB_range:
        for c in xC_range:
            # Restrição de extrato mineral: 8*a + 5*b + 4*c <= 120
            cond1 = (8 * a + 5 * b + 4 * c <= 120)
            # Restrição de solvente: 5*a + 4*b + 2*c <= 200
            cond2 = (5 * a + 4 * b + 2 * c <= 200)
            if cond1 and cond2:
                feasible_points.append((a, b, c))

# Converte a lista em um array NumPy para facilitar a plotagem
feasible_points = np.array(feasible_points)

# Cria uma figura para o gráfico 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plota os pontos da região factível (em cinza com transparência)
ax.scatter(
    feasible_points[:, 0],  # Coordenada xA
    feasible_points[:, 1],  # Coordenada xB
    feasible_points[:, 2],  # Coordenada xC
    s=5,  # Tamanho dos pontos
    color='gray',  # Cor dos pontos
    alpha=0.3,  # Transparência para melhor visualização
    label='Região Factível'
)

# Destaca a solução ótima encontrada com um marcador vermelho
ax.scatter(
    [xA.varValue], [xB.varValue], [xC.varValue],
    color='red', s=80, label='Solução Ótima'
)

# Configura os rótulos dos eixos e o título do gráfico
ax.set_xlabel('xA (Combustível A)')
ax.set_ylabel('xB (Combustível B)')
ax.set_zlabel('xC (Combustível C)')
ax.set_title('Região Factível (Exemplo 05) e Solução Ótima')
ax.legend()

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 3D no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
# com o nome 'exercise05.png'.
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise05.png')

# Exibe o gráfico na tela
plt.show()
