import pandas as pd
import matplotlib.pyplot as plt
import sys

def caluVariance(filename):
    data = pd.read_csv(filename)

    variance_cols = data['variance'].str.split(' ', expand=True)
    variance_cols.columns = ['variance1', 'variance2', 'variance3', 'variance4']
    variance_cols = variance_cols.apply(pd.to_numeric)

    data = pd.concat([data, variance_cols], axis=1)
    data = data.drop(columns=['variance'])

    grouped = data.groupby('rule')[['variance1', 'variance2', 'variance3', 'variance4']].mean()
    # grouped = data.groupby('rule')[['variance1', 'variance2', 'variance3', 'variance4']].median()

    return grouped

def plotVarianceAll(variances, filenameOutput = "./variance.pdf", varEnv=None):
    plt.rcParams.update({'font.size': 28})
    rounds = ["Round 1", "Round 2", "Round 3", "Round 4"]
    plt.figure(figsize=(12, 8))
    for label, variances in variances.items():
        plt.plot(rounds, variances, marker='o', label = label)
    plt.xlabel('Round')
    plt.ylabel('Variance')
    plt.xticks(["Round 1", "Round 2", "Round 3", "Round 4"])
    plt.legend()
    plt.grid(True)
    plt.savefig(filenameOutput, dpi = 300)
    if varEnv != None and varEnv["verbosity"] != 0: plt.show()

if __name__ == "__main__":
    grouped = caluVariance("D:\\程序与工具集\\SABM Keynesian Beauty Contest\\SABM KBC ver EMNLP 2024-06\\output\\keyResults\\full_results.csv")
    sys.path.append(".")

    varianceAll = {
        "Independent (temp 0.0)": list(grouped.loc["independent (temp 0.0)"]),
        "Independent (temp 0.7)": list(grouped.loc["independent (temp 0.7)"]),
        "Independent (temp 1.2)": list(grouped.loc["independent (temp 1.2)"]),
        "Default": list(grouped.loc["independent (temp 0.7)"]),
        "Independent (Claude-3)": list(grouped.loc["independent (Claude 3 sonnet)"]),
        "Explicit": list(grouped.loc["independent (Explicit instruction)"]),
        "Uncooperative": list(grouped.loc["independent (Uncooperative persona)"]),
        "Independent reward": list(grouped.loc["independent"]),
        "Exclusive reward": list(grouped.loc["exclusive"])
    }
    plotVarianceAll(varianceAll, "./AnalysisModule/results/240612_uncooperative_GPT_variance.pdf")
