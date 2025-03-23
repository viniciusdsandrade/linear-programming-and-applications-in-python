import matplotlib.pyplot as plt
import numpy as np

# /**
#  * Problema: Maximização da função objetivo L = 3x1 + 5x2 sujeito às restrições:
#  *          x1 <= 4,
#  x2 <= 6,
#  3x1 + 2x2 <= 18, e
#  x1, x2 >= 0.
#  * O código plota a região viável definida pelas restrições e destaca o ponto ótimo (2,6),
#  * onde a função objetivo L atinge o valor máximo de 36.
#  */

# Definindo os vértices da região viável
vertices = np.array([
    [0, 0],
    [4, 0],
    [4, 3],
    [2, 6],
    [0, 6]
])

# Configuração do gráfico
plt.figure(figsize=(6, 6))

# Plotando as restrições
# Reta: 3x1 + 2x2 = 18
x_line = np.linspace(0, 6, 100)
y_line = (18 - 3 * x_line) / 2
plt.plot(x_line, y_line, 'r--', label='$3x_1+2x_2=18$')

# Reta vertical: x1 = 4
plt.axvline(x=4, color='g', linestyle='--', label='$x_1=4$')

# Reta horizontal: x2 = 6
plt.axhline(y=6, color='b', linestyle='--', label='$x_2=6$')

# Preenchendo a região viável
plt.fill(vertices[:, 0], vertices[:, 1], color='lightgrey', alpha=0.5)

# Marcando os vértices e adicionando rótulos
for v in vertices:
    plt.plot(v[0], v[1], 'ko')
    plt.text(v[0] + 0.1, v[1] + 0.1, f'({v[0]},{v[1]})', fontsize=9)

# Destaque para o ponto ótimo
plt.plot(2, 6, 'mo', markersize=8, label='Ótimo (2,6)')

plt.xlim(-1, 7)
plt.ylim(-1, 10)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('Gráfico no Geogebra: Região Viável e Restrições')
plt.legend()
plt.grid(True)
plt.show()
