# [RESUMO DO PROBLEMA]
# A refinaria produz três tipos de gasolina (verde, azul e comum) a partir de
# três insumos:
#   - Gasolina pura (9.600.000 L/semana disponíveis)
#   - Octana (4.800.000 L/semana disponíveis)
#   - Aditivo (2.200.000 L/semana disponíveis)
#
# Especificações de consumo por litro de cada tipo de gasolina:
#   - Verde: 0,22 L gasolina pura + 0,50 L octana + 0,28 L aditivo
#   - Azul:  0,52 L gasolina pura + 0,34 L octana + 0,14 L aditivo
#   - Comum: 0,74 L gasolina pura + 0,20 L octana + 0,06 L aditivo
#
# Restrições de produção baseadas em demanda:
#   - A quantidade de gasolina comum >= 16 * quantidade de gasolina verde
#   - A quantidade de gasolina azul <= 600.000 L/semana
#
# Lucro (margem de contribuição) por litro:
#   - Verde: $0,30
#   - Azul:  $0,25
#   - Comum: $0,20
#
# Objetivo: maximizar a margem de contribuição total.

# [MODELO DE PROGRAMAÇÃO LINEAR]
# Variáveis de decisão (em litros/semana):
#   xv = volume de gasolina verde produzido
#   xa = volume de gasolina azul produzido
#   xc = volume de gasolina comum produzido
#
# Função objetivo:
#   Max Z = 0.30*xv + 0.25*xa + 0.20*xc
#
# Restrições de recursos:
#   (1) 0.22*xv + 0.52*xa + 0.74*xc <= 9.600.000  (gasolina pura)
#   (2) 0.50*xv + 0.34*xa + 0.20*xc <= 4.800.000  (octana)
#   (3) 0.28*xv + 0.14*xa + 0.06*xc <= 2.200.000  (aditivo)
#
# Restrições de demanda:
#   (4) xc >= 16*xv
#   (5) xa <= 600.000
#
# Não negatividade:
#   xv, xa, xc >= 0

# [CÓDIGO COMPLETO EM PYTHON COM SOLUÇÃO + VISUALIZAÇÃO EM 3D]

# Se precisar instalar PuLP:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1) Definir o problema
model = pulp.LpProblem("Exemplo_06", pulp.LpMaximize)

# 2) Criar variáveis
xv = pulp.LpVariable('GasolinaVerde', lowBound=0, cat='Continuous')
xa = pulp.LpVariable('GasolinaAzul', lowBound=0, cat='Continuous')
xc = pulp.LpVariable('GasolinaComum', lowBound=0, cat='Continuous')

# 3) Função objetivo
model += 0.30 * xv + 0.25 * xa + 0.20 * xc, "MargemContribuicao"

# 4) Restrições de recursos
model += 0.22 * xv + 0.52 * xa + 0.74 * xc <= 9_600_000, "GasolinaPura"
model += 0.50 * xv + 0.34 * xa + 0.20 * xc <= 4_800_000, "Octana"
model += 0.28 * xv + 0.14 * xa + 0.06 * xc <= 2_200_000, "Aditivo"

# 5) Restrições de mercado
model += xc - 16 * xv >= 0, "Comum_minimo_16_vezes_Verde"
model += xa <= 600_000, "Azul_max_600mil"

# 6) Resolver o modelo
model.solve()

# 7) Exibir resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("xv (Gasolina Verde) =", xv.varValue)
print("xa (Gasolina Azul)  =", xa.varValue)
print("xc (Gasolina Comum) =", xc.varValue)
print("Margem total de contribuição = $", pulp.value(model.objective))

# 8) Visualização em 3D (CUIDADO COM O TAMANHO DA MALHA)
#    Para demonstrar, vamos usar intervalos razoavelmente grandes e passos robustos.
#    Caso contrário, podemos ter um loop muito extenso e demorado.

# Vamos analisar limites teóricos:
#   - Se só produzir verde (xv):
#       0.22*xv <= 9.600.000 => xv <= ~43.636.363
#       0.50*xv <= 4.800.000 => xv <= 9.600.000
#       0.28*xv <= 2.200.000 => xv <= ~7.857.142
#     => O mais restritivo é ~7.857.142
#
#   - Se só produzir azul (xa):
#       0.52*xa <= 9.600.000 => xa <= ~18.461.538
#       0.34*xa <= 4.800.000 => xa <= ~14.117.647
#       0.14*xa <= 2.200.000 => xa <= ~15.714.285
#     => O mais restritivo ~14.117.647
#     MAS há restrição xa <= 600.000, que é muito menor que 14 milhões => use 600k
#
#   - Se só produzir comum (xc):
#       0.74*xc <= 9.600.000 => xc <= ~12.972.972
#       0.20*xc <= 4.800.000 => xc <= 24.000.000
#       0.06*xc <= 2.200.000 => xc <= ~36.666.666
#     => O mais restritivo é ~12.972.972
#
# Ademais, xc >= 16*xv. Se xv for grande, xc tem de ser ainda maior.
#
# Vamos usar escalas em centenas de milhares para xv e xc, e 50.000 para xa:
#   xv_range: 0..8.0 milhões com passo 100.000 => 81 pontos (0, 100k, 200k, ...)
#   xa_range: 0..600.000 com passo 50.000 => 13 pontos (0, 50k, 100k, ..., 600k)
#   xc_range: 0..13.0 milhões com passo 100.000 => 131 pontos
#
# O total de combinações seria 81*13*131 = 137.403. Grande, mas ainda possível
# dependendo do computador. Para DEMO, isso pode ser pesado.
#
# Aqui vamos mostrar o conceito com passos maiores para não travar (Ex: 500k):
#   xv_range de 0..8.0 milhões com passo 500k => 17 pontos
#   xa_range de 0..600.000 com passo 100k => 7 pontos
#   xc_range de 0..13.0 milhões com passo 500k => 27 pontos
#   => total = 17 * 7 * 27 = 3.213 pontos => factível como exemplo.
#
# Se precisar de mais precisão, reduzir os passos, mas o tempo de execução aumenta.

xv_range = np.arange(0, 8_500_000, 500_000)  # 0, 500k, 1M, 1.5M, ... ~ 8M
xa_range = np.arange(0, 650_000, 100_000)  # 0, 100k, 200k, ... 600k
xc_range = np.arange(0, 13_500_000, 500_000)  # 0, 500k, 1M, ... 13M

feasible_points = []

for v in xv_range:
    for a in xa_range:
        for c in xc_range:
            # Checar se satisfaz a soma e as restrições
            cond_pura = 0.22 * v + 0.52 * a + 0.74 * c <= 9_600_000
            cond_octana = 0.50 * v + 0.34 * a + 0.20 * c <= 4_800_000
            cond_aditivo = 0.28 * v + 0.14 * a + 0.06 * c <= 2_200_000
            cond_comum = c >= 16 * v  # xc >= 16*xv
            cond_azul = a <= 600_000
            if cond_pura and cond_octana and cond_aditivo and cond_comum and cond_azul:
                feasible_points.append((v, a, c))

feasible_points = np.array(feasible_points)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot dos pontos factíveis
# Com tantas combinações, mesmo 3k pontos, pode ficar lento.
# Vamos plotar e deixar alpha pequeno para ver densidade.
ax.scatter(
    feasible_points[:, 0],
    feasible_points[:, 1],
    feasible_points[:, 2],
    s=5, color='gray', alpha=0.3,
    label='Região Factível (amostrada)'
)

# Plot da solução ótima
ax.scatter(
    [xv.varValue], [xa.varValue], [xc.varValue],
    color='red', s=80, label='Solução Ótima (Exacta pelo Solver)'
)

ax.set_xlabel('xv (Gasolina Verde)')
ax.set_ylabel('xa (Gasolina Azul)')
ax.set_zlabel('xc (Gasolina Comum)')
ax.set_title('Região Factível (Exemplo 06) e Solução Ótima')
ax.legend()
plt.show()
