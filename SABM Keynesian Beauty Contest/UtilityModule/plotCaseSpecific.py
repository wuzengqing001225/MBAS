import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Georgia'
default_font_size = 42

def plotVarianceOld(variances, filenameOutput = "./variance.pdf", varEnv=None):
    rounds = ["Round 1", "Round 2", "Round 3", "Round 4"]
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, variances, marker='o')
    plt.xlabel('Round')
    plt.ylabel('Variance')
    plt.xticks(["Round 1", "Round 2", "Round 3", "Round 4"])
    plt.grid(True)
    plt.savefig(filenameOutput, dpi = 300)
    if varEnv != None and varEnv["verbosity"] != 0: plt.show()

def plotVariance(variances, filenameOutput = "./variance.pdf", varEnv=None):
    rounds = ["0", "1", "2", "3"]
    plt.figure(figsize=(12, 8))
    plt.plot(rounds, variances, linewidth=9)
    plt.xlabel('k', fontsize=default_font_size - 4, fontstyle='italic')
    plt.ylabel('Variance of Choices', fontsize=default_font_size - 4)
    plt.xticks(rounds, fontsize=default_font_size - 8)
    plt.yticks(fontsize=default_font_size - 12)
    plt.grid(True)
    plt.subplots_adjust(left=0.15, right=0.98, top=0.95, bottom=0.15)
    plt.savefig(filenameOutput, dpi = 300)
    if varEnv != None and varEnv["verbosity"] != 0: plt.show()

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