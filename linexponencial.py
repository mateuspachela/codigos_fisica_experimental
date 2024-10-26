import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

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

# Definir a função exponencial para o ajuste
def exp_decay(t, E0, RC):
    return E0 * np.exp(-t / RC)

# Ajuste exponencial usando curve_fit
popt, pcov = curve_fit(exp_decay, df['Tempo em segundos'], df['Voltagem adequado'], p0=(4, 1))

# Obter os valores ajustados de E0 e RC e as incertezas
E0_fit, RC_fit = popt
E0_err, RC_err = np.sqrt(np.diag(pcov))  # Incertezas nos parâmetros

# Exibir os parâmetros ajustados e as incertezas
print(f"Tensão inicial (E0): {E0_fit:.4f} ± {E0_err:.4f} volts")
print(f"Constante de tempo (RC): {RC_fit:.4f} ± {RC_err:.4f} segundos")

# Plotar os dados experimentais
plt.figure(figsize=(10, 6))
plt.scatter(df['Tempo em segundos'], df['Voltagem adequado'], color='black', label='Dados experimentais', marker='o', s=5, alpha=1)

# Criar a linha de ajuste exponencial
tempo_fit = np.linspace(df['Tempo em segundos'].min(), df['Tempo em segundos'].max(), 500)
ajuste_exponencial = exp_decay(tempo_fit, E0_fit, RC_fit)

# Plotar a linha de ajuste exponencial
plt.plot(tempo_fit, ajuste_exponencial, color='blue', label='Ajuste exponencial', linewidth=3)
plt.title('Ajuste Exponencial: VC(t) = E0 * exp(-t / RC)')
plt.xlabel('Tempo (s)')
plt.ylabel('Voltagem (V)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
