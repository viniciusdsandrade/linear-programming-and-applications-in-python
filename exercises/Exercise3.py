# [RESUMO DO PROBLEMA]
# Temos um sapateiro que pode fabricar sapatos e cintos:
#   - Se fizer SOMENTE sapatos durante 1 hora => produz 6 sapatos.
#   - Se fizer SOMENTE cintos  durante 1 hora => produz 5 cintos.
# Cada sapato consome 2 unidades de couro e cada cinto 1 unidade de couro.
# O total disponível de couro é 6 unidades.
# Lucro unitário: sapato = $5, cinto = $2.
# Queremos Max LUCR0 por hora.

# [MODELO DE PROGRAMAÇÃO LINEAR]
# Definindo as variáveis de decisão:
#   x1 = quantidade de sapatos produzidos por hora
#   x2 = quantidade de cintos produzidos por hora
#
# 1) Restrições de tempo:
#    (x1 / 6) + (x2 / 5) <= 1
#    => pois x1/6 é a fração de hora necessária para produzir x1 sapatos
#       e x2/5 é a fração de hora para x2 cintos.
#
# 2) Restrição de couro:
#    2*x1 + 1*x2 <= 6
#
# 3) Restrição de não negatividade:
#    x1 >= 0, x2 >= 0
#
# [FUNÇÃO OBJETIVO]
#   Max Z = 5*x1 + 2*x2

# [CÓDIGO COMPLETO EM PYTHON COM SOLUÇÃO E GRÁFICO]

import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1) Definir o problema
model = pulp.LpProblem("Exemplo_03", pulp.LpMaximize)

# 2) Criar variáveis
x1 = pulp.LpVariable('Sapatos', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Cintos',  lowBound=0, cat='Continuous')

# 3) Definir a função objetivo (maximizar lucro por hora)
model += 5*x1 + 2*x2, "Lucro_por_hora"

# 4) Adicionar restrições
#    Tempo: x1/6 + x2/5 <= 1
model += (1/6)*x1 + (1/5)*x2 <= 1, "Restricao_de_tempo"

#    Couro: 2*x1 + x2 <= 6
model += 2*x1 + x2 <= 6, "Restricao_de_couro"

# 5) Resolver o modelo
model.solve()

# 6) Mostrar resultados
print("Status da solução:", pulp.LpStatus[model.status])
print("x1 (Sapatos) =", x1.varValue)
print("x2 (Cintos)  =", x2.varValue)
print("Lucro máximo por hora = $", pulp.value(model.objective))

# 7) Plot da região factível e solução ótima em 2D
x1_vals = np.linspace(0, 6, 200)

# Da restrição de tempo: x1/6 + x2/5 <= 1 => x2 <= 5*(1 - x1/6) = 5 - (5/6)*x1
x2_tempo   = 5 - (5/6)*x1_vals

# Da restrição de couro: 2*x1 + x2 <= 6 => x2 <= 6 - 2*x1
x2_couro   = 6 - 2*x1_vals

plt.figure(figsize=(8,6))

# Curva da restrição de tempo
plt.plot(x1_vals, x2_tempo, label='x1/6 + x2/5 = 1', color='blue')
# Curva da restrição de couro
plt.plot(x1_vals, x2_couro, label='2*x1 + x2 = 6', color='red')

# Região factível
# precisamos tomar o mínimo das duas restrições (x2_tempo, x2_couro),
# e garantir que seja >= 0, pois x2 >= 0
x2_feasible = np.minimum(x2_tempo, x2_couro)
x2_feasible = np.maximum(x2_feasible, 0)
plt.fill_between(x1_vals, x2_feasible, color='gray', alpha=0.3)

# Solução ótima (ponto)
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 6)
plt.ylim(0, 6)
plt.xlabel('x1 (Sapatos por hora)')
plt.ylabel('x2 (Cintos por hora)')
plt.title('Região Factível (Exemplo 03) e Solução Ótima')
plt.legend()
plt.grid(True)
plt.show()
