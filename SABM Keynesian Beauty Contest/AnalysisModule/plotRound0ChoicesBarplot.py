import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Georgia'
default_font_size = 46

choices_df = pd.read_csv('./AnalysisModule/externalData/Choices.csv')
nyt_df = pd.read_csv('./AnalysisModule/externalData/nyt_data.csv')

def expand_data(df):
    return np.repeat(df['Number'].values, np.ceil(df['Percentage'] * 1000).astype(int))

expanded_choices = expand_data(choices_df)
expanded_nyt = expand_data(nyt_df)

plt.figure(figsize=(12, 6))

sns.kdeplot(expanded_choices, bw_adjust=0.5, color='blue', fill=True, alpha=0.2, lw = 4, label='Simulation Choices')
sns.kdeplot(expanded_nyt, bw_adjust=0.5, color='red', fill=True, alpha=0.2, lw = 4, label='NYT Choices')

# plt.yscale('log')

plt.grid()
plt.subplots_adjust(left=0.18, right=0.98, top=0.95, bottom=0.2)
plt.xticks(np.arange(0, 101, 10), fontsize=default_font_size - 8)
plt.yticks(fontsize=default_font_size - 8)
plt.xlabel('Chosen Numbers', fontsize=default_font_size - 4)
plt.ylabel('Frequency', fontsize=default_font_size - 4)
plt.legend(fontsize=default_font_size - 12, labelspacing=0.2)
plt.savefig("./AnalysisModule/results/KBC_choices_distributions.pdf", dpi = 300)
plt.show()
