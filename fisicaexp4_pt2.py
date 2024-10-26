import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Carregar os dados do arquivo
df = pd.read_csv(r'C:\Users\giova\Downloads\fisicaexp\testes_ceramico.txt', delimiter='\t')

# Substituir ',' por '.' para converter os números corretamente
df['Tempo em segundos'] = df['Tempo em segundos'].astype(str).str.replace(',', '.')
df['Voltagem adequado'] = df['Voltagem adequado'].astype(str).str.replace(',', '.')

# Converter as colunas para numéricas
df['Tempo em segundos'] = pd.to_numeric(df['Tempo em segundos'], errors='coerce')
df['Voltagem adequado'] = pd.to_numeric(df['Voltagem adequado'], errors='coerce')

df['Tempo em segundos'] = df['Tempo em segundos'] - 0.5

# Remover valores inválidos
df = df.dropna()

# Definir o valor máximo e os valores-alvo (2%, 37%)
valor_maximo = 4
valores_alvo = {
    "2%": 0.02 * valor_maximo,
    "37%": 0.37 * valor_maximo
}

# Definir uma tolerância de 5% para considerar os valores próximos
tolerancia = 0.05

# Dicionário para armazenar a primeira ocorrência de cada porcentagem
ocorrencias = {}

# Encontrar a primeira ocorrência de cada valor alvo (2%, 37%)
for porcentagem, valor in valores_alvo.items():
    indices = np.where(np.abs(df['Voltagem adequado'] - valor) <= tolerancia)[0]  # Encontrar todos os índices
    if len(indices) > 0:
        primeiro_tempo = df['Tempo em segundos'].iloc[indices[0]]  # Pegar o tempo da primeira ocorrência
        ocorrencias[porcentagem] = primeiro_tempo  # Armazenar no dicionário de ocorrências

# Exibir a primeira ocorrência de cada porcentagem encontrada
for porcentagem, tempo in ocorrencias.items():
    print(f"Primeira ocorrência correspondente a {porcentagem} do valor máximo: [{tempo:.2f}] segundos")

# Melhorar a estética do gráfico
plt.figure(figsize=(10, 6))

# Desenhar a linha do gráfico
plt.plot(df['Tempo em segundos'], df['Voltagem adequado'], label='Voltagem (V)', color='blue', linestyle='-', linewidth=2)

# Destacar a primeira ocorrência no gráfico, com legendas ajustadas
for porcentagem, tempo in ocorrencias.items():
    valor = valores_alvo[porcentagem]
    # Marcar o ponto acima da linha do gráfico, garantindo visibilidade
    plt.scatter(tempo, valor, color='red', s=80, edgecolor='black', zorder=5)  # O zorder garante que o ponto esteja acima
    # Ajustar a posição da legenda para uma melhor visualização
    if porcentagem == "2%":
        plt.text(tempo, valor + 0.1, f'{porcentagem}', fontsize=9, verticalalignment='bottom', horizontalalignment='right')  # Mover a legenda 2% para cima
    elif porcentagem == "37%":
        plt.text(tempo, valor - 0.15, f'{porcentagem}', fontsize=9, verticalalignment='top', horizontalalignment='left')  # Mover a legenda 37% para baixo

# Definir título e rótulos do gráfico
plt.title('Voltagem vs Tempo com Primeiras Ocorrências Destacadas', fontsize=14)
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Voltagem (V)', fontsize=12)
plt.ylim(0, 5)  # Limitar o eixo Y entre 0 e 5V
plt.xlim(0, df['Tempo em segundos'].max())  # Limitar o eixo X
plt.grid(True, linestyle='--', alpha=0.7)  # Grid com linhas tracejadas e leve transparência

# Mostrar a legenda no gráfico
plt.legend()

# Mostrar o gráfico
plt.show()
