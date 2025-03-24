import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D
from mpl_toolkits.mplot3d import Axes3D  # Necessário para criar gráficos 3D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# A empresa "Afia Bem Ltda." produz três modelos de facas: Padrão (P), Média (M)
# e Grande (G). O processo de fabricação passa por cinco máquinas:
#   1) Corte
#   2) Modelagem
#   3) Afiação
#   4) Cabo
#   5) Montagem
#
# Cada tipo de faca requer um certo tempo de processamento (em segundos) em cada
# máquina, conforme a tabela (valores reais extraídos da imagem):
#            Corte | Modelagem | Afiação | Cabo | Montagem
# Padrão  ->   10  |    10     |   12    |  19  |   19
# Médio   ->   10  |   15.5    |   16    |  21  |   21
# Grande  ->   12  |    17     |   19    |  24  |   22
#
# As disponibilidades diárias (em horas) de cada máquina são:
#   - Corte: 4 h
#   - Modelagem: 6 h
#   - Afiação: 6 h
#   - Cabo: 8 h
#   - Montagem: 8 h
#
# Além disso, há um limite de matéria-prima: 2,5 chapas metálicas,
# cada chapa medindo 2,00 m x 1,00 m => 20.000 cm² por chapa => 50.000 cm² no total.
# O consumo de área (cm²) por faca é:
#   - Padrão: 25 cm²
#   - Média:  32 cm²
#   - Grande: 45 cm²
#
# O lucro unitário (contribuição) de cada modelo é:
#   - Padrão (P): R$3,00
#   - Médio  (M): R$4,00
#   - Grande (G): R$4,70
#
# Objetivo: Determinar quantas facas de cada modelo devem ser produzidas
# para maximizar o lucro total, respeitando as restrições de tempo de máquina
# e disponibilidade de chapas metálicas.
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exemplo_07", pulp.LpMaximize)

# =============================================================================
# 2) Variáveis de decisão
# -----------------------------------------------------------------------------
xP = pulp.LpVariable("Facas_Padrao", lowBound=0, cat='Continuous')
xM = pulp.LpVariable("Facas_Media",  lowBound=0, cat='Continuous')
xG = pulp.LpVariable("Facas_Grande", lowBound=0, cat='Continuous')

# =============================================================================
# 3) Tempos de processamento (em segundos) para cada modelo e máquina
# -----------------------------------------------------------------------------
# Valores reais extraídos da tabela:
#   Padrão (P), Médio (M), Grande (G)
# Corte
cP, cM, cG = 10, 10, 12
# Modelagem
sP, sM, sG = 10, 15.5, 17
# Afiação
aP, aM, aG = 12, 16, 19
# Cabo
hP, hM, hG = 19, 21, 24
# Montagem
tP, tM, tG = 19, 21, 22

# =============================================================================
# 4) Disponibilidade das máquinas (horas convertidas em segundos)
# -----------------------------------------------------------------------------
# Multiplicamos cada disponibilidade (horas/dia) por 3600 para obter em segundos.
CUT_AVAILABLE      = 4 * 3600  # Corte
SHAPE_AVAILABLE    = 6 * 3600  # Modelagem
SHARP_AVAILABLE    = 6 * 3600  # Afiação
HANDLE_AVAILABLE   = 8 * 3600  # Cabo
ASSEMBLY_AVAILABLE = 8 * 3600  # Montagem

# =============================================================================
# 5) Restrição de matéria-prima (chapas metálicas)
# -----------------------------------------------------------------------------
# Cada chapa tem 2,00 m x 1,00 m = 20.000 cm²
# Estão disponíveis 2,5 chapas => 2,5 * 20.000 = 50.000 cm²
# Consumo de cada modelo (em cm²):
#   Padrão: 25, Médio: 32, Grande: 45
area_total = 50_000

# =============================================================================
# 6) Função objetivo (lucro)
# -----------------------------------------------------------------------------
# Lucro unitário:
#   Padrão: R$3,00
#   Médio:  R$4,00
#   Grande: R$4,70
model += 3.0*xP + 4.0*xM + 4.70*xG, "Lucro"

# =============================================================================
# 7) Adicionar restrições de tempo em cada máquina
# -----------------------------------------------------------------------------
model += cP*xP + cM*xM + cG*xG <= CUT_AVAILABLE,      "Limite_Corte"
model += sP*xP + sM*xM + sG*xG <= SHAPE_AVAILABLE,    "Limite_Modelagem"
model += aP*xP + aM*xM + aG*xG <= SHARP_AVAILABLE,    "Limite_Afiacao"
model += hP*xP + hM*xM + hG*xG <= HANDLE_AVAILABLE,   "Limite_Cabo"
model += tP*xP + tM*xM + tG*xG <= ASSEMBLY_AVAILABLE, "Limite_Montagem"

# =============================================================================
# 8) Restrição de área (chapas metálicas)
# -----------------------------------------------------------------------------
model += 25*xP + 32*xM + 45*xG <= area_total, "Limite_Chapas"

# =============================================================================
# 9) Resolver o problema
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 10) Mostrar resultados no console
# -----------------------------------------------------------------------------
print("Status da Solução =", pulp.LpStatus[model.status])
print("xP (Facas Padrão)  =", xP.varValue)
print("xM (Facas Médias)  =", xM.varValue)
print("xG (Facas Grandes) =", xG.varValue)
print("Lucro Máximo = R$ ", pulp.value(model.objective))

# =============================================================================
# 11) Plotagem em 3D da região factível (amostrada)
# -----------------------------------------------------------------------------
# Definimos intervalos (xP_range, xM_range, xG_range) e varremos as restrições.
# Intervalos muito grandes e passos pequenos podem deixar o loop lento.
# Ajuste conforme necessário.

xP_range = np.arange(0, 3001, 100)  # 0..3000, passo de 100
xM_range = np.arange(0, 3001, 100)
xG_range = np.arange(0, 3001, 100)

feasible_points = []

for p in xP_range:
    for m in xM_range:
        for g in xG_range:
            # Verifica primeiro a restrição de área (mais rápida de checar).
            if 25*p + 32*m + 45*g <= area_total:
                # Agora verifica as restrições de cada máquina:
                cond_corte  = (cP*p + cM*m + cG*g) <= CUT_AVAILABLE
                cond_model  = (sP*p + sM*m + sG*g) <= SHAPE_AVAILABLE
                cond_afia   = (aP*p + aM*m + aG*g) <= SHARP_AVAILABLE
                cond_cabo   = (hP*p + hM*m + hG*g) <= HANDLE_AVAILABLE
                cond_mont   = (tP*p + tM*m + tG*g) <= ASSEMBLY_AVAILABLE

                if cond_corte and cond_model and cond_afia and cond_cabo and cond_mont:
                    feasible_points.append((p, m, g))

feasible_points = np.array(feasible_points)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Se houver pontos factíveis, plotá-los em cinza
if len(feasible_points) > 0:
    ax.scatter(
        feasible_points[:, 0],
        feasible_points[:, 1],
        feasible_points[:, 2],
        s=5,
        color='gray',
        alpha=0.3,
        label='Região Factível (amostrada)'
    )

# Destaca a solução ótima em vermelho
ax.scatter(
    [xP.varValue], [xM.varValue], [xG.varValue],
    color='red', s=80, label='Solução Ótima'
)

ax.set_xlabel('xP (Padrão)')
ax.set_ylabel('xM (Média)')
ax.set_zlabel('xG (Grande)')
ax.set_title('Exemplo 07 - Região Factível (3D) e Solução Ótima')
ax.legend()

# Salva o gráfico antes de exibir (ajuste o caminho conforme necessário)
plt.savefig(
    r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\exercises\result\exercise07.png'
)

# Exibe o gráfico
plt.show()
