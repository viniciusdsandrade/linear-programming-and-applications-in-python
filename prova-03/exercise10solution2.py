# Lucros por unidade de produto (em R$)
LUCRO_PANELA = 3      # Lucro de R$ 3,00 por panela de pressão
LUCRO_FRIGIDEIRA = 4  # Lucro de R$ 4,00 por frigideira

# Capacidades e limites
HORAS_DISPONIVEIS = 6   # Horas disponíveis de máquina por dia (1 h/un)
DEMANDA_MAX_PANELA = 4  # Demanda máxima de panelas por dia
DEMANDA_MAX_FRIGIDEIRA = 4  # Demanda máxima de frigideiras por dia

# Lista de pontos extremos (vértices) viáveis
pontos_viaveis = []

# Gerar todas as combinações possíveis de produção (x panelas, y frigideiras)
for x in range(DEMANDA_MAX_PANELA + 1):
    for y in range(DEMANDA_MAX_FRIGIDEIRA + 1):
        # Restrição de tempo de máquina: 1 h por unidade
        if x + y <= HORAS_DISPONIVEIS:
            pontos_viaveis.append((x, y))

# Encontrar a solução ótima (máximo lucro)
melhor_plano = None
lucro_maximo = -1

for x, y in pontos_viaveis:
    # Cálculo do lucro total para o vértice (x, y)
    lucro = LUCRO_PANELA * x + LUCRO_FRIGIDEIRA * y
    print(f"Produzir {x} panelas e {y} frigideiras → Lucro = R${lucro}")
    # Atualiza melhor solução caso o lucro seja maior
    if lucro > lucro_maximo:
        lucro_maximo = lucro
        melhor_plano = (x, y)

# Exibe o resultado final
print("\n=== Solução Ótima ===")
print(f"Painelas de pressão: {melhor_plano[0]}")
print(f"Frigideiras:       {melhor_plano[1]}")
print(f"Lucro máximo:      R${lucro_maximo}")
