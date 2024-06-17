import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys

def transformCSV(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            round_data = {"Round": int(row["Round"].split()[1])}
            for key in row:
                if key.startswith("player_"):
                    round_data[key] = int(row[key])
            data.append(round_data)
    return data

def plotSingleRunVariance(filenames, rule):
    fig, axes = plt.subplots(5, 3, figsize=(20, 12))
    axes = axes.flatten()
    
    for i, filename in enumerate(filenames):
        df = pd.DataFrame(transformCSV(filename))
        ax = axes[i]
        
        for round_num in df["Round"]:
            round_data = df[df["Round"] == round_num].drop(columns=["Round"]).values.flatten()
            ax.boxplot(round_data, positions=[round_num], widths=0.6)
        
        ax.set_xlabel('Round')
        ax.set_ylabel('Choices')
        # ax.set_title(f'Dataset {i+1}')
        ax.set_xticks(df["Round"])
        ax.set_ylim((0, 70))
    
    fig.suptitle(f'{rule.capitalize()} rule')
    plt.tight_layout()
    plt.savefig(f"./AnalysisModule/results/240610_{rule}_boxplot.pdf", dpi = 300)
    plt.show()

if __name__ == "__main__":
    rule = "independent"
    mainFolder = f"./output/SimulationSet_240608_1607/{rule}"

    sys.path.append(".")
    from UtilityModule.fileInputOutput import getSubdirectories
    subFolders = getSubdirectories(mainFolder)
    
    filenames = []
    for subFolder in subFolders:
        filenames.append(f"{mainFolder}/{subFolder}/overview.csv")
    
    plotSingleRunVariance(filenames, rule)