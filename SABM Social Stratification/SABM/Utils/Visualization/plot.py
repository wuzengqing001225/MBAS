import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Georgia'
plt.rcParams.update({'font.size': 16})

WIDTH = 11
HEIGHT = 9

def fig_output(fig_filepath:str, db):
    filename_format = "{fig_filepath}_{type}.pdf"


def visulization(fig_filepath:str, db):
    plt.clf()

    plt.pause(0.1)
    plt.show(block=False)
