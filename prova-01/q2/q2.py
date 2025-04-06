import pulp                   # Biblioteca para modelagem e resolução de problemas de programação linear
import numpy as np            # Biblioteca para manipulação de arrays e cálculos numéricos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos 2D

# =============================================================================
# DESCRIÇÃO DO PROBLEMA
# -----------------------------------------------------------------------------
# Um jovem atleta deseja maximizar o número total de sessões de treinamento, praticando:
#   - Natação: cada sessão custa R$3,00, dura 2 horas e consome 1.500 calorias.
#   - Ciclismo: cada sessão custa R$2,00, dura 2 horas e consome 1.000 calorias.
#
# Recursos disponíveis:
#   - Orçamento: R$70,00
#   - Tempo: 18 horas mensais (cada sessão dura 2 horas, logo, máximo de 9 sessões)
#   - Calorias: 80.000 calorias
#
# MODELO DE PROGRAMAÇÃO LINEAR:
#
# Variáveis de decisão:
#   x = número de sessões de natação
#   y = número de sessões de ciclismo
#
# Função objetivo:
#   Max Z = x + y
#
# Restrições:
#   a) Custo:    3*x + 2*y <= 70
#   b) Tempo:    2*(x+y) <= 18  ->  x + y <= 9
#   c) Calorias: 1500*x + 1000*y <= 80000  (ou, dividindo por 500: 3*x + 2*y <= 160)
#
# Não negatividade:
#   x >= 0, y >= 0
# =============================================================================

# =============================================================================
# 1) Definir o problema de otimização (Maximização do Número de Sessões)
# -----------------------------------------------------------------------------
model = pulp.LpProblem("Exercicio2_Maximizar_Sessoes", pulp.LpMaximize)

# =============================================================================
# 2) Criar as variáveis de decisão
# -----------------------------------------------------------------------------
x = pulp.LpVariable('Natacao', lowBound=0, cat='Continuous')
y = pulp.LpVariable('Ciclismo', lowBound=0, cat='Continuous')

# =============================================================================
# 3) Definir a função objetivo
# -----------------------------------------------------------------------------
model += x + y, "Numero_Total_Sessoes"

# =============================================================================
# 4) Adicionar as restrições do problema
# -----------------------------------------------------------------------------
# Restrição de custo:
model += 3 * x + 2 * y <= 70, "Restricao_Custo"

# Restrição de tempo (cada sessão tem 2 horas, total máximo 18 horas):
model += x + y <= 9, "Restricao_Tempo"

# Restrição calórica:
model += 1500 * x + 1000 * y <= 80000, "Restricao_Calorias"
# (A forma simplificada 3*x + 2*y <= 160 não é necessária, pois a restrição de custo já é mais
#  limitante)

# =============================================================================
# 5) Resolver o modelo
# -----------------------------------------------------------------------------
model.solve()

# =============================================================================
# 6) Exibir os resultados da otimização
# -----------------------------------------------------------------------------
print("Status da Solução:", pulp.LpStatus[model.status])
print("Número de Sessões de Natação =", x.varValue)
print("Número de Sessões de Ciclismo =", y.varValue)
print("Número Total de Sessões =", pulp.value(model.objective))

# =============================================================================
# 7) Visualizar a região factível e a solução ótima em 2D
# -----------------------------------------------------------------------------
# Para a plotagem, usamos x no eixo X e y no eixo Y.
# As restrições importantes para a visualização:
# (1) Tempo:      x + y <= 9         -> y <= 9 - x
# (2) Custo:      3*x + 2*y <= 70    -> y <= (70 - 3*x) / 2
# (3) Calorias:   1500*x + 1000*y <= 80000  -> y <= (80000 - 1500*x) / 1000

x_vals = np.linspace(0, 10, 300)
y_tempo = 9 - x_vals
y_custo = (70 - 3 * x_vals) / 2
y_calorias = (80000 - 1500 * x_vals) / 1000

# Para cada valor de x, o limite efetivo de y é o menor entre as restrições (garantindo que y >= 0)
y_feasible = np.minimum(np.minimum(y_tempo, y_custo), y_calorias)
y_feasible = np.maximum(y_feasible, 0)

plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_tempo, label='x + y = 9 (Tempo)')
plt.plot(x_vals, y_custo, label='3x + 2y = 70 (Custo)')
plt.plot(x_vals, y_calorias, label='1500x + 1000y = 80000 (Calorias)')
plt.fill_between(x_vals, 0, y_feasible, color='gray', alpha=0.3, label='Região Factível')

# Marcar a solução ótima encontrada (qualquer ponto com x+y = 9 é ótimo)
# Exemplo: escolher x = 4, y = 5
plt.scatter(4, 5, color='black', zorder=5, label='Solução Ótima (exemplo)')

plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('Sessões de Natação (x)')
plt.ylabel('Sessões de Ciclismo (y)')
plt.title('Exercício 2 - Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

plt.savefig(r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-01\q2\exercise2.png')
plt.show()
