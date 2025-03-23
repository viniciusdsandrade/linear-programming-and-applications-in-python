import pulp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------
# EXEMPLO 07 COM PLOTAGEM 3D
# -----------------------------
# SUPONDO valores de tempo FICTÍCIOS (em segundos) para cada modelo em cada máquina.
# Se você tiver os valores reais, substitua diretamente.

# 1) Definir o problema
model = pulp.LpProblem("Exemplo_07", pulp.LpMaximize)

# 2) Variáveis de decisão
xP = pulp.LpVariable("Facas_Padrao", lowBound=0, cat='Continuous')
xM = pulp.LpVariable("Facas_Media",  lowBound=0, cat='Continuous')
xG = pulp.LpVariable("Facas_Grande", lowBound=0, cat='Continuous')

# 3) Parâmetros fictícios de tempo (seg/faca) - Troque pelos valores reais
#    Corte (cP, cM, cG)
cP, cM, cG = 20, 26, 35
#    Modelagem (sP, sM, sG)
sP, sM, sG = 30, 40, 50
#    Afiação (aP, aM, aG)
aP, aM, aG = 10, 12, 16
#    Cabo (hP, hM, hG)
hP, hM, hG = 15, 18, 25
#    Montagem (tP, tM, tG)
tP, tM, tG = 15, 20, 28

# 4) Disponibilidade das máquinas (horas -> segundos)
CUT_AVAILABLE      = 4 * 3600   # 14.400
SHAPE_AVAILABLE    = 6 * 3600   # 21.600
SHARP_AVAILABLE    = 6 * 3600   # 21.600
HANDLE_AVAILABLE   = 8 * 3600   # 28.800
ASSEMBLY_AVAILABLE = 8 * 3600   # 28.800

# 5) Restrição de matéria-prima (chapas metálicas)
#    Cada chapa tem 2,00m x 1,00m = 20.000 cm²
#    Disponíveis 2,5 chapas => 50.000 cm²
area_total = 50000

# 6) Função objetivo (lucro)
#    R$ 3,00 (P), 4,00 (M), 4,70 (G)
model += 3.0*xP + 4.0*xM + 4.70*xG, "Lucro"

# 7) Restrições de tempo nas máquinas
model += cP*xP + cM*xM + cG*xG <= CUT_AVAILABLE,      "Limite_Corte"
model += sP*xP + sM*xM + sG*xG <= SHAPE_AVAILABLE,    "Limite_Modelagem"
model += aP*xP + aM*xM + aG*xG <= SHARP_AVAILABLE,    "Limite_Afiacao"
model += hP*xP + hM*xM + hG*xG <= HANDLE_AVAILABLE,   "Limite_Cabo"
model += tP*xP + tM*xM + tG*xG <= ASSEMBLY_AVAILABLE, "Limite_Montagem"

# 8) Restrição de área (chapas metálicas)
model += 25*xP + 32*xM + 45*xG <= area_total, "Limite_Chapas"

# 9) Resolver
model.solve()

# 10) Mostrar resultados no console
print("Status da Solução =", pulp.LpStatus[model.status])
print("xP (Facas Padrão)  =", xP.varValue)
print("xM (Facas Médias)  =", xM.varValue)
print("xG (Facas Grandes) =", xG.varValue)
print("Lucro Máximo = R$ ", pulp.value(model.objective))

# 11) Plotagem em 3D da região factível (amostrada)
#     Ajuste os intervalos e passos conforme sua necessidade.
#     Intervalos muito grandes e passo pequeno => loop pesado.

xP_range = np.arange(0, 3001, 100)  # 0..3000, passo de 100
xM_range = np.arange(0, 3001, 100)
xG_range = np.arange(0, 3001, 100)

feasible_points = []

for p in xP_range:
    for m in xM_range:
        for g in xG_range:
            # Primeiro, checar se passa na restrição de área, evitando checar
            # todas as máquinas desnecessariamente caso já reprove por área:
            if 25*p + 32*m + 45*g <= area_total:
                # Restrições de corte, modelagem, afiação, cabo e montagem
                cond_corte  = (cP*p + cM*m + cG*g) <= CUT_AVAILABLE
                cond_model  = (sP*p + sM*m + sG*g) <= SHAPE_AVAILABLE
                cond_afia   = (aP*p + aM*m + aG*g) <= SHARP_AVAILABLE
                cond_cabo   = (hP*p + hM*m + hG*g) <= HANDLE_AVAILABLE
                cond_mont   = (tP*p + tM*m + tG*g) <= ASSEMBLY_AVAILABLE
                if cond_corte and cond_model and cond_afia and cond_cabo and cond_mont:
                    feasible_points.append((p, m, g))

feasible_points = np.array(feasible_points)

# Criar a figura 3D
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

# Plot dos pontos factíveis (em cinza)
if len(feasible_points) > 0:
    ax.scatter(
        feasible_points[:,0],
        feasible_points[:,1],
        feasible_points[:,2],
        s=5, color='gray', alpha=0.3,
        label='Região Factível (amostrada)'
    )

# Plot da solução ótima em vermelho
ax.scatter(
    [xP.varValue], [xM.varValue], [xG.varValue],
    color='red', s=80, label='Solução Ótima'
)

ax.set_xlabel('xP (Padrão)')
ax.set_ylabel('xM (Média)')
ax.set_zlabel('xG (Grande)')
ax.set_title('Exemplo 07 - Região Factível (3D) e Solução Ótima')
ax.legend()
plt.show()
