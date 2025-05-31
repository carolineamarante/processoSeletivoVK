import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dados extraídos da imagem
dados = {
    'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
    'Visitas no site': [12500, 9500, 14000, 13500, 11200],
    'Leads': [620, 480, 750, 705, 580],
    'Vendas': [58, 43, 70, 60, 45],
    'Faturamento': [29000, 21500, 35000, 30000, 22500],
    'Investimento': [8000, 6500, 9000, 9000, 8000]
}

# Criar DataFrame
df = pd.DataFrame(dados)

# Cálculo de indicadores
df['Taxa Conversão Visitas→Leads (%)'] = (df['Leads'] / df['Visitas no site']) * 100
df['Taxa Conversão Leads→Vendas (%)'] = (df['Vendas'] / df['Leads']) * 100
df['Custo por Lead (R$)'] = df['Investimento'] / df['Leads']
df['Custo por Venda (R$)'] = df['Investimento'] / df['Vendas']
df['Lucro'] = df['Faturamento'] - df['Investimento']

# Proporção de Investimento e Lucro em percentual sobre Faturamento
df['Investimento (%)'] = (df['Investimento'] / df['Faturamento']) * 100
df['Lucro (%)'] = (df['Lucro'] / df['Faturamento']) * 100

# Gráfico de Investimento vs Lucro com porcentagens
plt.figure(figsize=(10,6))

bar_width = 0.4
x = range(len(df))

bars1 = plt.bar(x, df['Lucro'], width=bar_width, label='Lucro', color='green')
bars2 = plt.bar([i + bar_width for i in x], df['Investimento'], width=bar_width, label='Investimento', color='red')

# Adicionando porcentagens
for i, bar in enumerate(bars1):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f"{df['Lucro (%)'][i]:.1f}%", ha='center', va='bottom', fontsize=10, color='black')

for i, bar in enumerate(bars2):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f"{df['Investimento (%)'][i]:.1f}%", ha='center', va='bottom', fontsize=10, color='black')

plt.xticks([i + bar_width / 2 for i in x], df['Mês'])
plt.ylabel('Valor (R$)')
plt.title('Proporção de Investimento e Lucro sobre Faturamento')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Plot das taxas
sns.lineplot(data=df, x='Mês', y='Taxa Conversão Visitas→Leads (%)', marker='o', label='Visitas → Leads')
sns.lineplot(data=df, x='Mês', y='Taxa Conversão Leads→Vendas (%)', marker='s', label='Leads → Vendas')

# Adicionando valores nas taxas
for i, row in df.iterrows():
    plt.text(i, row['Taxa Conversão Visitas→Leads (%)'] + 0.5,
             f"{row['Taxa Conversão Visitas→Leads (%)']:.1f}%",
             ha='center', va='bottom', fontsize=9, color='blue')

    plt.text(i, row['Taxa Conversão Leads→Vendas (%)'] + 0.5,
             f"{row['Taxa Conversão Leads→Vendas (%)']:.1f}%",
             ha='center', va='bottom', fontsize=9, color='orange')

plt.title('Taxas de Conversão por Mês')
plt.ylabel('Taxa (%)')
plt.legend()
plt.tight_layout()
plt.show()



# Seleção das colunas para a tabela de indicadores
tabela_indicadores = df[['Mês',
                         'Taxa Conversão Visitas→Leads (%)',
                         'Taxa Conversão Leads→Vendas (%)',
                         'Custo por Lead (R$)',
                         'Custo por Venda (R$)']].copy()

# Removendo o símbolo de porcentagem (mostrando como decimal)
tabela_indicadores['Taxa Conversão Visitas→Leads'] = df['Leads'] / df['Visitas no site']
tabela_indicadores['Taxa Conversão Leads→Vendas'] = df['Vendas'] / df['Leads']

# Mantendo os custos
tabela_indicadores['Custo por Lead'] = df['Custo por Lead (R$)']
tabela_indicadores['Custo por Venda'] = df['Custo por Venda (R$)']

# Mantendo apenas as colunas desejadas
tabela_indicadores = tabela_indicadores[['Mês',
                                         'Taxa Conversão Visitas→Leads',
                                         'Taxa Conversão Leads→Vendas',
                                         'Custo por Lead',
                                         'Custo por Venda']]

# Exibir tabela formatada
print("\n====================")
print("TABELA DE INDICADORES")
print("====================\n")
print(tabela_indicadores.to_string(index=False,
                                   float_format='{:,.4f}'.format))


# ---------------------
# ANÁLISE AUTOMÁTICA
# ---------------------

# Melhor e pior mês em lucro
melhor_lucro = df.loc[df['Lucro'].idxmax()]
pior_lucro = df.loc[df['Lucro'].idxmin()]

# Eficiência: Lucro por real investido
df['Lucro por Real Investido'] = df['Lucro'] / df['Investimento']
melhor_eficiencia = df.loc[df['Lucro por Real Investido'].idxmax()]
pior_eficiencia = df.loc[df['Lucro por Real Investido'].idxmin()]

print("\n---------------------")
print("ANÁLISE INTERPRETATIVA DOS DADOS")
print("---------------------")

print(f"\n O mês com maior lucro foi **{melhor_lucro['Mês']}**, com um lucro de R$ {melhor_lucro['Lucro']:.2f},")
print(f"correspondendo a {melhor_lucro['Lucro (%)']:.1f}% do faturamento.")

print(f"\n O mês com menor lucro foi **{pior_lucro['Mês']}**, com um lucro de R$ {pior_lucro['Lucro']:.2f},")
print(f"correspondendo a {pior_lucro['Lucro (%)']:.1f}% do faturamento.")

print(f"\n A maior eficiência no investimento ocorreu em **{melhor_eficiencia['Mês']}**,")
print(f"gerando R$ {melhor_eficiencia['Lucro por Real Investido']:.2f} de lucro por cada real investido.")

print(f"\n A menor eficiência foi em **{pior_eficiencia['Mês']}**, com apenas R$ {pior_eficiencia['Lucro por Real Investido']:.2f} de retorno por real investido.")

print("\n Observações gerais:")

if df['Taxa Conversão Visitas→Leads (%)'].max() - df['Taxa Conversão Visitas→Leads (%)'].min() > 2:
    print(" - A taxa de conversão de visitas para leads variou significativamente entre os meses.")
else:
    print(" - A taxa de conversão de visitas para leads manteve-se relativamente estável.")

if df['Custo por Venda (R$)'].max() - df['Custo por Venda (R$)'].min() > 50:
    print(" - O custo por venda apresentou uma variação expressiva, impactando a eficiência.")
else:
    print(" - O custo por venda foi relativamente constante.")

if melhor_lucro['Mês'] != melhor_eficiencia['Mês']:
    print(" - Nem sempre o maior lucro correspondeu à melhor eficiência do investimento.")
