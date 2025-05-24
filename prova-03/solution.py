import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Exercício – Fabricação de Refribom e Refrisaúde via Álgebra Linear
# Salvando gráfico em:
# C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-03
# =============================================================================

# 1) Definição das restrições ativas
A = np.array([[7, 9],    # coeficientes na 1ª restrição
              [11, 5]])  # coeficientes na 2ª restrição
b = np.array([63,        # lado direito da 1ª restrição
              55])       # lado direito da 2ª restrição

# resolve A · [x1, x2]ᵀ = b → interseção das duas retas
x_int, y_int = np.linalg.solve(A, b)

# 2) Cálculo de outros vértices factíveis
vertice_origem     = (0.0, 0.0)                   # (0,0)
vertice_r1_eixo_x2 = (0.0, 63/9)                  # x1=0 na 1ª restrição → x2=7
vertice_x1_cap     = (4.0, (55 - 11*4) / 5)       # x1=4 na 2ª restrição → x2=2.2
vertice_duas_restr = (x_int, y_int)               # interseção das duas restrições

# 3) Filtrar vértices que satisfazem todas as restrições
candidatos = [
    vertice_origem,
    vertice_r1_eixo_x2,
    vertice_x1_cap,
    vertice_duas_restr
]
feasible = []
for x, y in candidatos:
    if (0 <= x <= 4 and y >= 0
        and 7*x + 9*y <= 63
        and 11*x + 5*y <= 55):
        feasible.append((x, y))

# 4) Avaliar função-objetivo L = x1 + 2·x2 em cada vértice
melhor = None
L_max = -np.inf
print("Avaliação nos vértices factíveis:")
for x, y in feasible:
    L = x + 2*y
    print(f"  x1 = {x:.3f}, x2 = {y:.3f} → L = {L:.3f}")
    if L > L_max:
        L_max = L
        melhor = (x, y)

# 5) Exibir solução ótima
print("\n=== SOLUÇÃO ÓTIMA ===")
print(f"Refribom (x1)   = {melhor[0]:.3f} milhões")
print(f"Refrisaúde (x2) = {melhor[1]:.3f} milhões")
print(f"Lucro máximo Lₘₐₓ = {L_max:.3f} milhões")

# 6) Plot da região factível e ponto ótimo
x_vals = np.linspace(0, 4, 200)
y_vals = np.linspace(0, 8, 200)
X, Y = np.meshgrid(x_vals, y_vals)
mask = (7*X + 9*Y <= 63) & (11*X + 5*Y <= 55)

plt.figure(figsize=(6, 6))
plt.contourf(X, Y, mask, levels=[-0.5, 0.5, 1.5], alpha=0.3)
plt.contour(X, Y, 7*X + 9*Y, levels=[63], linestyles='--', linewidths=2)
plt.contour(X, Y, 11*X + 5*Y, levels=[55], linestyles='--', linewidths=2)

for vx, vy in feasible:
    plt.scatter(vx, vy, color='black', zorder=5)
plt.scatter(melhor[0], melhor[1], color='red', zorder=6, label=f'Ótimo ({melhor[0]:.0f},{melhor[1]:.0f})')

plt.xlim(0, 4)
plt.ylim(0, 8)
plt.xlabel('x1 (Refribom, milhões)')
plt.ylabel('x2 (Refrisaúde, milhões)')
plt.title('Região Factível e Solução Ótima')
plt.legend()
plt.grid(True)

# 7) Salvar o gráfico na pasta indicada
output_path = r'C:\Users\Vinícius Andrade\Desktop\linear-programming-and-applications-in-python\prova-03\regiao_factivel_modelo_matricial.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Gráfico salvo em: {output_path}")

plt.show()
