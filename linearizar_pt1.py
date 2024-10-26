import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress

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

# Linearizar os dados aplicando o logaritmo natural à voltagem
df['ln_VC'] = np.log(df['Voltagem adequado'])

# Plotar o gráfico linearizado (ln(VC) vs Tempo)
plt.figure(figsize=(10, 6))
plt.scatter(df['Tempo em segundos'], df['ln_VC'], color='black', label='Dados experimentais', marker='o', s=10,alpha=0.4)
plt.title('Gráfico linearizado: ln(VC(t)) vs Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('ln(VC(t))')
plt.grid(True, linestyle='--', alpha=0.7)



# Ajuste linear (regressão) para determinar a inclinação da reta
slope, intercept, r_value, p_value, std_err = linregress(df['Tempo em segundos'], df['ln_VC'])

# Create the regression line
regression_line = slope * df['Tempo em segundos'] + intercept

# Plot the regression line
plt.plot(df['Tempo em segundos'], regression_line, color='blue', label='Fit linear', linewidth=3)
plt.legend()

# Cálculo da incerteza do intercepto
n = len(df)  # número de pontos
erro_intercept = std_err * np.sqrt(1/n)

print(f"Inclinação (coef. angular): {slope:.4f} ± {std_err:.4f}")
print(f"Intercepto (coef. linear): {intercept:.4f} ± {erro_intercept:.4f}")

# Exibir os resultados da regressão
print(f"Coeficiente de determinação (R²): {r_value**2}")

# Determinar RC a partir da inclinação
RC = -1 / slope
erro_RC = std_err / slope**2  # incerteza em RC
print(f"RC (constante de tempo): {RC} segundos")

# Determinar E0 (tensão inicial) a partir do intercepto
E0 = np.exp(intercept)
erro_E0 = E0 * erro_intercept  # incerteza de E0 usando propagação de erros
print(f"Tensão inicial (E0): {E0:.4f} ± {erro_E0:.4f} volts")

plt.show()
