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

# Remover valores inválidos
df = df.dropna()

# Definir o valor máximo e os valores-alvo (2%, 37%, 63%, 98%)
valor_maximo = 4.1
valores_alvo = {
    "2%": 0.02 * valor_maximo,
    "37%": 0.37 * valor_maximo,
    #"63%": 0.63 * valor_maximo,
    "98%": 0.98 * valor_maximo
}

# Definir uma tolerância menor para considerar os valores próximos
tolerancia = 0.05  # Reduzindo a tolerância para aumentar precisão

# Dicionário para armazenar as primeiras ocorrências de cada porcentagem
ocorrencias = {}

# Encontrar as primeiras ocorrências de cada valor alvo (2%, 37%, 63%, 98%)
for porcentagem, valor in valores_alvo.items():
    indices = np.where(np.abs(df['Voltagem adequado'] - valor) <= tolerancia)[0]  # Encontrar todos os índices
    if len(indices) > 0:
        tempo_correspondente = df['Tempo em segundos'].iloc[indices[0]]  # Pegar o primeiro tempo correspondente
        ocorrencias[porcentagem] = tempo_correspondente

# Exibir as primeiras ocorrências encontradas
for porcentagem, tempo in ocorrencias.items():
    print(f"Primeira ocorrência de {porcentagem} do valor máximo: {tempo:.6f} segundos")

# Plotar o gráfico com as primeiras ocorrências marcadas
plt.figure(figsize=(10, 6))
plt.plot(df['Tempo em segundos'], df['Voltagem adequado'], label='Voltagem (V)', color='blue', linewidth=1.5)

# Destacar as primeiras ocorrências no gráfico
for porcentagem, tempo in ocorrencias.items():
    valor = valores_alvo[porcentagem]
    plt.scatter(tempo, valor, color='red', s=50)  # Marcar o ponto
    plt.text(tempo, valor, f'{porcentagem}', fontsize=10, verticalalignment='bottom')  # Exibir o texto

# Detalhes do gráfico
plt.title('Voltagem vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Voltagem (V)')
plt.ylim(0, 5)  # Limitar o eixo Y
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
