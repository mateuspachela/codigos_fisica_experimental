import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Carregar os dados do arquivo .txt com separação por tabulação
df = pd.read_csv(r'C:\Users\giova\Downloads\fisicaexp\massa_10cm.txt', sep='\t')

# Remover espaços antes ou depois dos nomes das colunas
df.columns = df.columns.str.strip()

# Renomear as colunas para 'Tempo' e 'Posicao'
df.rename(columns={'NomeDaColunaTempo': 'Tempo', 'NomeDaColunaPosicao': 'Posicao'}, inplace=True)

# Substituir vírgulas por pontos nas colunas 'Tempo' e 'Posicao'
df['Tempo'] = df['Tempo'].astype(str).str.replace(',', '.')
df['Posicao'] = df['Posicao'].astype(str).str.replace(',', '.')

# Converter as colunas para tipo numérico
df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
df['Posicao'] = pd.to_numeric(df['Posicao'], errors='coerce')

# Remover linhas com valores inválidos
df = df.dropna()

# Calcular a derivada (velocidade) usando diferenças finitas
df['Velocidade'] = df['Posicao'].diff() / df['Tempo'].diff()

# Encontrar cruzamentos com o zero com base na posição
cruzamentos_posicao = np.where(np.diff(np.sign(df['Posicao'])))[0]

# Encontrar cruzamentos com o zero com base na velocidade
cruzamentos_velocidade = np.where(np.diff(np.sign(df['Velocidade'])))[0]

# Refinar cruzamentos de zero usando interpolação linear
def interpolar_cruzamento(df, cruzamentos):
    tempos_cruzamentos = []
    for i in cruzamentos:
        t1, t2 = df['Tempo'].iloc[i], df['Tempo'].iloc[i + 1]
        x1, x2 = df['Posicao'].iloc[i], df['Posicao'].iloc[i + 1]
        t_cruzamento = t1 - (x1 * (t2 - t1) / (x2 - x1))
        tempos_cruzamentos.append(t_cruzamento)
    return np.array(tempos_cruzamentos)

tempos_cruzamentos_posicao = interpolar_cruzamento(df, cruzamentos_posicao)
tempos_cruzamentos_velocidade = interpolar_cruzamento(df, cruzamentos_velocidade)

print(f"Tempos nos cruzamentos com o zero (posição): {tempos_cruzamentos_posicao}")
print(f"Tempos nos cruzamentos com o zero (velocidade): {tempos_cruzamentos_velocidade}")

# Desconsiderar os últimos 5 períodos
def calcular_periodo_medio_e_incerteza(tempos_cruzamentos):
    if len(tempos_cruzamentos) > 1:
        periodos = np.diff(tempos_cruzamentos) * 2  # Cada diferença é meia onda
        if len(periodos) > 5:
            periodos = periodos[:-5]  # Desconsiderar os últimos 5 períodos
        periodo_medio = np.mean(periodos)
        incerteza = np.std(periodos) / np.sqrt(len(periodos))  # Erro padrão da média
        return periodo_medio, incerteza
    else:
        return None, None

# Calcular período médio e incerteza com base na posição
periodo_medio_posicao, incerteza_posicao = calcular_periodo_medio_e_incerteza(tempos_cruzamentos_posicao)
if periodo_medio_posicao is not None:
    print(f"Período médio (posição): {periodo_medio_posicao:.4f} segundos")
    print(f"Incerteza do período (posição): {incerteza_posicao:.4f} segundos")
else:
    print("Não foram encontrados cruzamentos suficientes para calcular o período (posição).")

# Calcular período médio e incerteza com base na velocidade
periodo_medio_velocidade, incerteza_velocidade = calcular_periodo_medio_e_incerteza(tempos_cruzamentos_velocidade)
if periodo_medio_velocidade is not None:
    print(f"Período médio (velocidade): {periodo_medio_velocidade:.4f} segundos")
    print(f"Incerteza do período (velocidade): {incerteza_velocidade:.4f} segundos")
else:
    print("Não foram encontrados cruzamentos suficientes para calcular o período (velocidade).")

# Plotar os cruzamentos com o zero no gráfico
plt.figure(figsize=(10, 6))
plt.plot(df['Tempo'], df['Posicao'], label='Posição')
plt.plot(df['Tempo'].iloc[cruzamentos_posicao], df['Posicao'].iloc[cruzamentos_posicao], 'ro', label='Cruzamentos com o zero (posição)')
plt.plot(df['Tempo'].iloc[cruzamentos_velocidade], df['Posicao'].iloc[cruzamentos_velocidade], 'go', label='Cruzamentos com o zero (velocidade)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Gráfico de Posição com Cruzamentos com o Zero')
plt.xlim(0, 10)  # Ajuste os limites conforme necessário
plt.grid(True)
plt.legend()
plt.show()
