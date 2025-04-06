import numpy as np
import matplotlib.pyplot as plt

# Gera um grid de valores para x1 e x2 (ex: de 0 a 5)
x1_vals = np.linspace(0, 5, 200)
x2_vals = np.linspace(0, 5, 200)
X1, X2 = np.meshgrid(x1_vals, x2_vals)

# Restrições no plano x3=x4=x5=0
# R1: 30x1 + 20x2 >= 80
# R2: 60x1 + 20x2 >= 120
# R3:  5x1 + 10x2 >= 30
R1 = (30*X1 + 20*X2 >= 80)
R2 = (60*X1 + 20*X2 >= 120)
R3 = (5*X1 + 10*X2 >= 30)

# Define a região factível
feasible = R1 & R2 & R3

# Configuração do gráfico
plt.figure(figsize=(6,6))
plt.title("Corte do problema no plano (x1, x2)")

# Preenche a área que satisfaz TODAS as restrições
plt.contourf(X1, X2, feasible, levels=[0, 0.5, 1], alpha=0.3)

# Desenha as retas de fronteira (igualdades)
# R1: 30x1 + 20x2 = 80 => x2 = (80 - 30x1)/20
x2_r1 = (80 - 30*x1_vals)/20
# R2: 60x1 + 20x2 = 120 => x2 = (120 - 60x1)/20
x2_r2 = (120 - 60*x1_vals)/20
# R3:  5x1 + 10x2 = 30 => x2 = (30 - 5*x1_vals)/10
x2_r3 = (30 - 5*x1_vals)/10

plt.plot(x1_vals, x2_r1, 'r--', label="30x1 + 20x2 = 80")
plt.plot(x1_vals, x2_r2, 'g--', label="60x1 + 20x2 = 120")
plt.plot(x1_vals, x2_r3, 'b--', label="5x1 + 10x2 = 30")

# Destaca a solução ótima (x1=1.2, x2=2.4) no corte
plt.plot(1.2, 2.4, 'mo', markersize=8, label='Ótimo (1.2, 2.4)')

plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.legend()
plt.grid(True)

# Salva a figura na pasta "result" e depois exibe
plt.savefig("result/dieta_corte.png", dpi=300)
plt.show()
