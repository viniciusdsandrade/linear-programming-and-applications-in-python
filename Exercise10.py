# [RESUMO DO PROBLEMA]
# Duas fábricas (F1 e F2) produzem três tipos de papel: fino, médio e grosso.
# O pedido total é:
#   - 16 toneladas de papel fino
#   - 6 toneladas de papel médio
#   - 28 toneladas de papel grosso
#
# Custo de operação (por dia):
#   - Fábrica 1 (F1): R$ 1.000,00/dia
#   - Fábrica 2 (F2): R$ 2.000,00/dia
#
# Produção diária:
#   Fábrica 1:
#       - 8 toneladas de papel fino
#       - 1 tonelada de papel médio
#       - 2 toneladas de papel grosso
#   Fábrica 2:
#       - 2 toneladas de papel fino
#       - 1 tonelada de papel médio
#       - 7 toneladas de papel grosso
#
# OBJETIVO: Atender as demandas, gastando o menor custo possível (Minimizar custo).
#
# [MODELO DE PROGRAMAÇÃO LINEAR]
# Variáveis de decisão (dias de operação):
#   x1 = nº de dias que a Fábrica 1 (F1) vai operar
#   x2 = nº de dias que a Fábrica 2 (F2) vai operar
#
# Função Objetivo:
#   Min Z = 1000 * x1 + 2000 * x2
#
# Restrições (suprir as demandas):
#   - Papel fino >= 16 toneladas:
#        8*x1 + 2*x2 >= 16
#   - Papel médio >= 6 toneladas:
#        1*x1 + 1*x2 >= 6
#   - Papel grosso >= 28 toneladas:
#        2*x1 + 7*x2 >= 28
#   - Não negatividade: x1 >= 0, x2 >= 0
#   (Não há menção se devem ser valores inteiros ou fracionários; assumimos cat='Continuous' por padrão.)
#
# [CÓDIGO COMPLETO EM PYTHON + PLOTAGEM 2D]

# Se precisar instalar:
# !pip install pulp

import pulp
import numpy as np
import matplotlib.pyplot as plt

# 1) Definir o problema (Minimização)
model = pulp.LpProblem("Exemplo_10", pulp.LpMinimize)

# 2) Criar variáveis (dias de operação)
#    Se quiser forçar dias inteiros, usar cat='Integer'.
#    O enunciado não especifica se pode fracionar. Vamos assumir cat='Continuous'.
x1 = pulp.LpVariable('Fabrica1_dias', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Fabrica2_dias', lowBound=0, cat='Continuous')

# 3) Função objetivo: Min Custo
model += 1000 * x1 + 2000 * x2, "Custo"

# 4) Restrições de produção
model += 8 * x1 + 2 * x2 >= 16, "Fino"
model += 1 * x1 + 1 * x2 >= 6, "Medio"
model += 2 * x1 + 7 * x2 >= 28, "Grosso"

# 5) Resolver
model.solve()

# 6) Mostrar resultados
print("Status da Solução:", pulp.LpStatus[model.status])
print("x1 (Dias de Fábrica 1) =", x1.varValue)
print("x2 (Dias de Fábrica 2) =", x2.varValue)
print("Custo Mínimo = R$ ", pulp.value(model.objective))

# 7) Plotar a região factível em 2D
#    Nossas variáveis: x1 (eixo X), x2 (eixo Y).
#    Restrições (>=) vamos isolar x2:
#       (1) 8x1 + 2x2 >= 16  => x2 >= (16 - 8x1)/2  = 8 - 4x1
#       (2) x1 + x2 >= 6     => x2 >= 6 - x1
#       (3) 2x1 + 7x2 >= 28  => x2 >= (28 - 2x1)/7 = 4 - (2/7)*x1
#    E x1 >= 0, x2 >= 0.
#    A região factível é "acima" (ou igual) dessas retas, e dentro do 1º quadrante.

x1_vals = np.linspace(0, 10, 300)  # supondo que a solução não ultrapasse x1=10
# Calculando as fronteiras:
x2_fino = 8 - 4 * x1_vals  # x2 >= 8 - 4x1
x2_medio = 6 - x1_vals  # x2 >= 6 - x1
x2_grosso = 4 - (2 / 7) * x1_vals  # x2 >= 4 - (2/7)*x1

plt.figure(figsize=(8, 6))

# Plot das fronteiras
plt.plot(x1_vals, x2_fino, label='8x1 + 2x2 = 16 (Fino)', color='blue')
plt.plot(x1_vals, x2_medio, label='x1 + x2 = 6 (Médio)', color='red')
plt.plot(x1_vals, x2_grosso, label='2x1 + 7x2 = 28 (Grosso)', color='green')

# Precisamos que x2 >= max( x2_fino, x2_medio, x2_grosso, 0 )
x2_feasible = []
for i, x1v in enumerate(x1_vals):
    val_fino = 8 - 4 * x1v
    val_medio = 6 - x1v
    val_grosso = 4 - (2 / 7) * x1v

    # Para cada x1, a restrição diz que x2 >= max(val_fino, val_medio, val_grosso, 0)
    lower_bound = max(val_fino, val_medio, val_grosso, 0)
    # Não há um upper bound explícito, mas vamos desenhar algo
    if lower_bound < 20:
        # para um limite de plot, digamos 20
        x2_feasible.append((x1v, lower_bound))
    else:
        # se lower_bound > 20, vamos ignorar (sai do gráfico)
        x2_feasible.append((x1v, np.nan))

# Preencher a área "acima" de max(...)?
# De fato, as restrições são >=, a região factível é toda a área ACIMA dessas linhas,
# mas vamos recortar em y até um limite de exibição (digamos y=20).
x1_feas = [p[0] for p in x2_feasible]
low_feas = [p[1] for p in x2_feasible]

plt.fill_between(x1_feas, low_feas, 20, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima
plt.scatter(x1.varValue, x2.varValue, color='black', zorder=5, label='Solução Ótima')

plt.xlim(0, 10)
plt.ylim(0, 20)
plt.xlabel('x1 (Dias de Fábrica 1)')
plt.ylabel('x2 (Dias de Fábrica 2)')
plt.title('Exemplo 10 - Região Factível e Solução Ótima (Min. Custo)')
plt.legend()
plt.grid(True)
plt.show()
