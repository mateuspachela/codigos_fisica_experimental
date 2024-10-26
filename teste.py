import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Carregar os dados do arquivo .txt
df = pd.read_csv(r'C:\Users\giova\Downloads\fisicaexp\massa_10cm.txt', sep='\t')

# Substituir vírgulas por pontos nas colunas 'Tempo' e 'Posicao'
df['Tempo'] = df['Tempo'].astype(str).str.replace(',', '.')
df['Posicao'] = df['Posicao'].astype(str).str.replace(',', '.')

# Converter as colunas para tipo numérico
df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df['Posicao'] = pd.to_numeric(df['Posicao'], errors='coerce')

# Remover linhas com valores inválidos
df = df.dropna()

# Plotar o gráfico de posição por tempo
plt.figure(figsize=(10, 6))
plt.plot(df['Tempo'], df['Posicao'], label='Posição')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Gráfico de Posição por Tempo')
plt.grid(True)
plt.legend()
plt.show()

# Encontrar cruzamentos com o zero com interpolação linear
cruzamentos = np.where(np.diff(np.sign(df['Posicao'])))[0]

# Interpolar os cruzamentos com o zero para maior precisão
def interpolar_cruzamento(df, cruzamentos):
    tempos_cruzamentos = []
    for i in cruzamentos:
        t1, t2 = df['Tempo'].iloc[i], df['Tempo'].iloc[i + 1]
        x1, x2 = df['Posicao'].iloc[i], df['Posicao'].iloc[i + 1]
        t_cruzamento = t1 - (x1 * (t2 - t1) / (x2 - x1))
        tempos_cruzamentos.append(t_cruzamento)
    return np.array(tempos_cruzamentos)

tempos_cruzamentos = interpolar_cruzamento(df, cruzamentos)

# Calcular os períodos (tempo entre cruzamentos consecutivos)
if len(tempos_cruzamentos) > 1:
    periodos = np.diff(tempos_cruzamentos) * 2  # Cada diferença é meia onda, multiplicamos por 2
    
    # Desconsiderar os últimos 5 períodos
    if len(periodos) > 5:
        periodos_filtrados = periodos[:-5]
    else:
        periodos_filtrados = periodos
    
    periodo_medio = np.mean(periodos_filtrados)
    incerteza = np.std(periodos_filtrados) / np.sqrt(len(periodos_filtrados))  # Erro padrão da média

    print(f"Períodos filtrados (s): {periodos_filtrados}")
    print(f"Período médio: {periodo_medio:.4f} segundos")
    print(f"Incerteza do período: {incerteza:.4f} segundos")
else:
    print("Não foram encontrados cruzamentos suficientes para calcular o período.")

# Plotar os cruzamentos com o zero no gráfico
plt.figure(figsize=(10, 6))
plt.plot(df['Tempo'], df['Posicao'], label='Posição')
plt.plot(tempos_cruzamentos, [0] * len(tempos_cruzamentos), 'ro', label='Cruzamentos com o zero')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Gráfico de Posição com Cruzamentos com o Zero')
plt.grid(True)
plt.legend()
plt.show()
