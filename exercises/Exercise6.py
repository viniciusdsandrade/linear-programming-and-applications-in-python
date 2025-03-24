import pulp  # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np  # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D
from mpl_toolkits.mplot3d import Axes3D  # Necessário para criar gráficos 3D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# A refinaria produz três tipos de gasolina (verde, azul e comum) utilizando três insumos:
#   - Gasolina pura: 9.600.000 L disponíveis por semana
#   - Octana: 4.800.000 L disponíveis por semana
#   - Aditivo: 2.200.000 L disponíveis por semana
#
# Cada litro de gasolina é produzido através da mistura dos insumos conforme as seguintes
# especificações (por litro produzido):
#   - Gasolina Verde: 0,22 L de gasolina pura, 0,50 L de octana e 0,28 L de aditivo
#   - Gasolina Azul:  0,52 L de gasolina pura, 0,34 L de octana e 0,20 L de aditivo
#   - Gasolina Comum: 0,74 L de gasolina pura, 0,20 L de octana e 0,06 L de aditivo
#
# Regras de produção (restrições de mercado):
#   - A quantidade de gasolina comum (xc) deve ser, no mínimo, 16 vezes a quantidade de gasolina verde (xv)
#   - A quantidade de gasolina azul (xa) deve ser no máximo 600.000 L por semana
#
# Lucro (margem de contribuição) por litro:
#   - Gasolina Verde: $0,30
#   - Gasolina Azul:  $0,25
#   - Gasolina Comum: $0,20
#
# Objetivo:
# Maximizar a margem total de contribuição para o lucro.
#
# Modelagem do problema:
# Variáveis de decisão (em litros/semana):
#   xv = volume de gasolina verde produzido
#   xa = volume de gasolina azul produzido
#   xc = volume de gasolina comum produzido
#
# Função objetivo:
#   Max Z = 0.30*xv + 0.25*xa + 0.20*xc
#
# Restrições de recursos:
#   (1) Gasolina pura: 0.22*xv + 0.52*xa + 0.74*xc <= 9.600.000
#   (2) Octana:        0.50*xv + 0.34*xa + 0.20*xc <= 4.800.000
#   (3) Aditivo:       0.28*xv + 0.14*xa + 0.06*xc <= 2.200.000
#
# Restrições de mercado:
#   (4) Demanda:      xc >= 16*xv
#   (5) Azul:         xa <= 600.000
#
# Não negatividade:
#   xv, xa, xc >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização
# -----------------------------------------------------------------------------
# Cria um objeto do problema com o objetivo de maximizar a margem de contribuição.
model = pulp.LpProblem("Exemplo_06", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
# Definimos as variáveis:
#   xv: litros de gasolina verde produzidos por semana.
#   xa: litros de gasolina azul produzidos por semana.
#   xc: litros de gasolina comum produzidos por semana.
# As variáveis são contínuas e não podem ser negativas.
xv = pulp.LpVariable('GasolinaVerde', lowBound=0, cat='Continuous')
xa = pulp.LpVariable('GasolinaAzul', lowBound=0, cat='Continuous')
xc = pulp.LpVariable('GasolinaComum', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
# A função objetivo é maximizar a margem total de contribuição:
#   Margem = 0.30*xv + 0.25*xa + 0.20*xc
model += 0.30 * xv + 0.25 * xa + 0.20 * xc, "MargemContribuicao"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de gasolina pura:
model += 0.22 * xv + 0.52 * xa + 0.74 * xc <= 9_600_000, "GasolinaPura"

# Restrição de octana:
model += 0.50 * xv + 0.34 * xa + 0.20 * xc <= 4_800_000, "Octana"

# Restrição de aditivo:
model += 0.28 * xv + 0.14 * xa + 0.06 * xc <= 2_200_000, "Aditivo"

# Restrição de demanda: gasolina comum deve ser pelo menos 16 vezes a gasolina verde
model += xc - 16 * xv >= 0, "Comum_minimo_16_vezes_Verde"

# Restrição de produção de gasolina azul:
model += xa <= 600_000, "Azul_max_600mil"

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
# Utiliza o método solve() para encontrar a solução ótima que maximiza a margem
# de contribuição, respeitando todas as restrições.
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
# Imprime o status da solução, os valores ótimos das variáveis e a margem total de contribuição.
print("Status da solução:", pulp.LpStatus[model.status])
print("xv (Gasolina Verde) =", xv.varValue)
print("xa (Gasolina Azul)  =", xa.varValue)
print("xc (Gasolina Comum) =", xc.varValue)
print("Margem total de contribuição = $", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 3D
# -----------------------------------------------------------------------------
# Devido aos grandes números envolvidos, a visualização da região factível é feita por amostragem
# com intervalos maiores para não sobrecarregar o processamento. Os intervalos escolhidos são:
#   - xv_range: de 0 até aproximadamente 8,5 milhões com passo de 500.000 litros.
#   - xa_range: de 0 até aproximadamente 650.000 com passo de 100.000 litros (limitado por xa <= 600.000).
#   - xc_range: de 0 até aproximadamente 13,5 milhões com passo de 500.000 litros.
xv_range = np.arange(0, 8_500_000, 500_000)  # Ex: 0, 500k, 1M, ... até ~8M
xa_range = np.arange(0, 650_000, 100_000)  # Ex: 0, 100k, 200k, ... até 600k
xc_range = np.arange(0, 13_500_000, 500_000)  # Ex: 0, 500k, 1M, ... até ~13M

feasible_points = []  # Lista para armazenar pontos factíveis (amostrados)

# Verifica, para cada combinação de xv, xa e xc, se as restrições são satisfeitas
for v in xv_range:
    for a in xa_range:
        for c in xc_range:
            cond_gasolina = 0.22 * v + 0.52 * a + 0.74 * c <= 9_600_000
            cond_octana = 0.50 * v + 0.34 * a + 0.20 * c <= 4_800_000
            cond_aditivo = 0.28 * v + 0.14 * a + 0.06 * c <= 2_200_000
            cond_comum = c >= 16 * v  # xc deve ser pelo menos 16 vezes xv
            cond_azul = a <= 600_000  # xa deve ser no máximo 600,000
            if cond_gasolina and cond_octana and cond_aditivo and cond_comum and cond_azul:
                feasible_points.append((v, a, c))

# Converte a lista em um array NumPy para facilitar a plotagem
feasible_points = np.array(feasible_points)

# Cria a figura para o gráfico 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plota os pontos da região factível (amostrados) em cinza com transparência
ax.scatter(
    feasible_points[:, 0],  # Valores de xv (Gasolina Verde)
    feasible_points[:, 1],  # Valores de xa (Gasolina Azul)
    feasible_points[:, 2],  # Valores de xc (Gasolina Comum)
    s=5,
    color='gray',
    alpha=0.3,
    label='Região Factível (amostrada)'
)

# Destaca a solução ótima encontrada (calculada pelo solver) com um ponto vermelho
ax.scatter(
    [xv.varValue],
    [xa.varValue],
    [xc.varValue],
    color='red',
    s=80,
    label='Solução Ótima (Exacta)'
)

# Configura os rótulos dos eixos e o título do gráfico
ax.set_xlabel('xv (Gasolina Verde)')
ax.set_ylabel('xa (Gasolina Azul)')
ax.set_zlabel('xc (Gasolina Comum)')
ax.set_title('Região Factível (Exemplo 06) e Solução Ótima')
ax.legend()

# =============================================================================
# 8) Salvar o gráfico no diretório especificado
# -----------------------------------------------------------------------------
# Salva o gráfico 3D no diretório:
# 'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result'
# com o nome 'exercise06.png'
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise06.png')

# Exibe o gráfico na tela
plt.show()
