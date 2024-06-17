import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set font properties
plt.rcParams['font.family'] = 'Georgia'
default_font_size = 46

def caluVariance(filename):
    data = pd.read_csv(filename)
    variance_cols = data['variance'].str.split(' ', expand=True)
    variance_cols.columns = ['variance1', 'variance2', 'variance3', 'variance4']
    variance_cols = variance_cols.apply(pd.to_numeric)
    data = pd.concat([data, variance_cols], axis=1)
    data = data.drop(columns=['variance'])
    grouped_mean = data.groupby('rule')[['variance1', 'variance2', 'variance3', 'variance4']].mean()
    grouped_std = data.groupby('rule')[['variance1', 'variance2', 'variance3', 'variance4']].std()
    return grouped_mean, grouped_std

def plotVarianceAll(title, variances, std_devs, filenameOutput = "./variance.pdf", fill_between=False, ylabel=True):
    rounds = ["0", "1", "2", "3"]
    if title == "Different Instructions":
        plt.figure(figsize=(12, 8))
    else:
        plt.figure(figsize=(11, 8))
    
    max_ylim = 0
    for label, variance in variances.items():
        std_dev = std_devs[label]
        if label in ["Baseline", "Temp=0.7", "GPT-4-0314"]:
            plt.plot(rounds, variance, label=label, linewidth=9, zorder = 3)
        else:
            plt.plot(rounds, variance, label=label, linewidth=9)
        if fill_between:
            plt.fill_between(rounds, [v - s for v, s in zip(variance, std_dev)], 
                         [v + s for v, s in zip(variance, std_dev)], alpha=0.15)
        max_ylim = max(max_ylim, max(v + s for v, s in zip(variance, std_dev)))
    
    plt.xlabel('k', fontsize=default_font_size - 4, fontstyle='italic')
    if ylabel: plt.ylabel('Variance of Choices', fontsize=default_font_size - 4)
    plt.xticks(rounds, fontsize=default_font_size - 8)
    plt.yticks(fontsize=default_font_size - 8)
    plt.ylim([0, max_ylim])
    # plt.title(title, fontsize=default_font_size)
    legend = plt.legend(fontsize=default_font_size - 10, labelspacing=0.2)
    legend.get_texts()[0].set_fontweight('bold')
    plt.grid(True)
    if title == "Different Instructions":
        plt.subplots_adjust(left=0.15, right=0.98, top=0.95, bottom=0.15)
    else:
        plt.subplots_adjust(left=0.10, right=0.98, top=0.95, bottom=0.15)
    plt.savefig(filenameOutput, dpi=300)
    plt.show()

if __name__ == "__main__":
    grouped_mean, grouped_std = caluVariance("D:\\程序与工具集\\SABM Keynesian Beauty Contest\\SABM KBC ver EMNLP 2024-06\\output\\keyResults\\full_results.csv")

    # Default (GPT-4, temp 0.7, no explicit instruction, no persona)
    varianceAll = {
        # "Baseline": list(grouped_mean.loc["independent (temp 0.7)"].fillna(0).replace([np.inf, -np.inf], 0)),
        # "Explicit instruction": list(grouped_mean.loc["independent (Explicit instruction)"].fillna(0).replace([np.inf, -np.inf], 0)),
        # "Uncooperative": list(grouped_mean.loc["independent (Uncooperative persona)"].fillna(0).replace([np.inf, -np.inf], 0)),

        "Temp=0.7": list(grouped_mean.loc["independent (temp 0.7)"].fillna(0).replace([np.inf, -np.inf], 0)),
        "Temp=0.0": list(grouped_mean.loc["independent (temp 0.0)"].fillna(0).replace([np.inf, -np.inf], 0)),
        "Temp=1.2": list(grouped_mean.loc["independent (temp 1.2)"].fillna(0).replace([np.inf, -np.inf], 0)),

        # "GPT-4-0314": list(grouped_mean.loc["independent (temp 0.7)"].fillna(0).replace([np.inf, -np.inf], 0)),
        # "Claude-3-Sonnet": list(grouped_mean.loc["independent (Claude 3 sonnet)"].fillna(0).replace([np.inf, -np.inf], 0)),
    }
    stdDevAll = {
        # "Baseline": list(grouped_std.loc["independent (temp 0.7)"].fillna(0).replace([np.inf, -np.inf], 0)),
        # "Explicit instruction": list(grouped_std.loc["independent (Explicit instruction)"].fillna(0).replace([np.inf, -np.inf], 0)),
        # "Uncooperative": list(grouped_std.loc["independent (Uncooperative persona)"].fillna(0).replace([np.inf, -np.inf], 0)),

        "Temp=0.7": list(grouped_std.loc["independent (temp 0.7)"].fillna(0).replace([np.inf, -np.inf], 0)),
        "Temp=0.0": list(grouped_std.loc["independent (temp 0.0)"].fillna(0).replace([np.inf, -np.inf], 0)),
        "Temp=1.2": list(grouped_std.loc["independent (temp 1.2)"].fillna(0).replace([np.inf, -np.inf], 0)),

        # "GPT-4-0314": list(grouped_std.loc["independent (temp 0.7)"].fillna(0).replace([np.inf, -np.inf], 0)),
        # "Claude-3-Sonnet": list(grouped_std.loc["independent (Claude 3 sonnet)"].fillna(0).replace([np.inf, -np.inf], 0)),
    }
    
    # plotVarianceAll("Different Instructions", varianceAll, stdDevAll, "./AnalysisModule/results/KBC_variance_instruction.pdf", fill_between=True, ylabel=True)
    plotVarianceAll("Different Temperatures", varianceAll, stdDevAll, "./AnalysisModule/results/KBC_variance_temperatures.pdf", fill_between=True, ylabel=False)
    # plotVarianceAll("Different Models", varianceAll, stdDevAll, "./AnalysisModule/results/KBC_variance_model.pdf", fill_between=True, ylabel=False)
