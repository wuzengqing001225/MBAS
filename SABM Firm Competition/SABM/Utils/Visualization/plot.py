import matplotlib.pyplot as plt

firm_color = {
    1: "#FF6103", #"#EE1289", "#FF6103"
    2: "#1C86EE",
    3: "#355E3B",
}

plt.rcParams['font.family'] = 'Georgia'
plt.rcParams.update({'font.size': 16})

WIDTH = 11
HEIGHT = 9

def fig_output(fig_filepath:str, db):
    filename_format = "{fig_filepath}_{type}.pdf"

    db.firms = sorted(db.firms, key = lambda x: x.id)
    round_length = len(db.firms[0].history['price_history'])
    round_range = list(range(1, round_length + 1))
    
    # Price
    plt.figure(figsize=(WIDTH + 3, HEIGHT))
    for fm in db.firms:
        plt.plot(round_range, fm.history['price_history'], label=f"Firm {fm.id}", color=firm_color[fm.id], linewidth = 2.5)
        
        if db.firms[0].ideal_max_lprice != db.firms[1].ideal_max_lprice:
            plt.hlines(fm.ideal_max_lprice, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dotted', label=f"Bertrand Price (Firm {fm.id})")
        if db.firms[0].ideal_max_uprice != db.firms[1].ideal_max_uprice:
            plt.hlines(fm.ideal_max_uprice, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dashed', label=f"Cartel Price (Firm {fm.id})")
    
    if db.firms[0].ideal_max_lprice == db.firms[1].ideal_max_lprice:
        plt.hlines(db.firms[0].ideal_max_lprice, xmin=1, xmax=round_length, color='black', linestyles='dotted', label=f"Bertrand Price")
    if db.firms[0].ideal_max_uprice == db.firms[1].ideal_max_uprice:
        plt.hlines(db.firms[0].ideal_max_uprice, xmin=1, xmax=round_length, color='black', linestyles='dashed', label=f"Cartel Price")
    
    plt.xlabel("Round", fontsize = 40)
    plt.ylabel("Price", fontsize = 40)
    plt.legend(loc='best', fontsize = 26)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(filename_format.format(fig_filepath = fig_filepath, type = 'price'), dpi = 600)
    plt.close()

    # Demand
    plt.figure(figsize=(WIDTH + 3, HEIGHT))
    for fm in db.firms:
        plt.plot(round_range, fm.history['demand_history'], label=f"Firm {fm.id}", color=firm_color[fm.id], linewidth = 2.5)    
    plt.xlabel("Round", fontsize = 40)
    plt.ylabel("Demand", fontsize = 40)
    plt.legend(loc='best', fontsize = 34)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(filename_format.format(fig_filepath = fig_filepath, type = 'demand'), dpi = 600)
    plt.close()

    # Profit
    plt.figure(figsize=(WIDTH + 3, HEIGHT))
    for fm in db.firms:
        plt.plot(round_range, fm.history['profit_history'], label=f"Firm {fm.id}", color=firm_color[fm.id], linewidth = 2.5)

        if db.firms[0].ideal_max_lprofit != db.firms[1].ideal_max_lprofit:
            plt.hlines(fm.ideal_max_lprofit, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dotted', label=f"Bertrand Profit (Firm {fm.id})")
        if db.firms[0].ideal_max_uprofit != db.firms[1].ideal_max_uprofit:
            plt.hlines(fm.ideal_max_uprofit, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dashed', label=f"Cartel Profit (Firm {fm.id})")
    
    if db.firms[0].ideal_max_lprofit == db.firms[1].ideal_max_lprofit:
        plt.hlines(db.firms[0].ideal_max_lprofit, xmin=1, xmax=round_length, color='black', linestyles='dotted', label=f"Bertrand Profit")
    if db.firms[0].ideal_max_uprofit == db.firms[1].ideal_max_uprofit:
        plt.hlines(db.firms[0].ideal_max_uprofit, xmin=1, xmax=round_length, color='black', linestyles='dashed', label=f"Cartel Profit")

    plt.xlabel("Round", fontsize = 40)
    plt.ylabel("Profit", fontsize = 40)
    plt.legend(loc='best', fontsize = 26)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(filename_format.format(fig_filepath = fig_filepath, type = 'profit'), dpi = 600)
    plt.close()

    # Asset
    plt.figure(figsize=(WIDTH + 3, HEIGHT))
    for fm in db.firms:
        plt.plot(round_range, fm.history['asset_history'], label=f"Firm {fm.id}", color=firm_color[fm.id], linewidth = 2.5)    
    plt.xlabel("Round", fontsize = 40)
    plt.ylabel("Asset", fontsize = 40)
    plt.legend(loc='best', fontsize = 34)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.savefig(filename_format.format(fig_filepath = fig_filepath, type = 'asset'), dpi = 600)
    plt.close()

def visulization(fig_filepath:str, db):
    filename_format = "{fig_filepath}_{type}.pdf"

    round_length = len(db.firms[0].history['price_history'])
    round_range = list(range(1, round_length + 1))

    plt.clf()
    plt.subplot(2, 1, 1)
    for fm in db.firms:
        plt.plot(round_range, fm.history['price_history'], label=f"Firm {fm.id}", color=firm_color[fm.id], linewidth = 2.5)
        
        if db.firms[0].ideal_max_lprice != db.firms[1].ideal_max_lprice:
            plt.hlines(fm.ideal_max_lprice, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dotted', label=f"Bertrand Price (Firm {fm.id})")
        if db.firms[0].ideal_max_uprice != db.firms[1].ideal_max_uprice:
            plt.hlines(fm.ideal_max_uprice, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dashed', label=f"Cartel Price (Firm {fm.id})")
    
    if db.firms[0].ideal_max_lprice == db.firms[1].ideal_max_lprice:
        plt.hlines(db.firms[0].ideal_max_lprice, xmin=1, xmax=round_length, color='black', linestyles='dotted', label=f"Bertrand Price")
    if db.firms[0].ideal_max_uprice == db.firms[1].ideal_max_uprice:
        plt.hlines(db.firms[0].ideal_max_uprice, xmin=1, xmax=round_length, color='black', linestyles='dashed', label=f"Cartel Price")
    
    plt.xlabel("Round", fontsize = 20)
    plt.ylabel("Price", fontsize = 20)
    plt.legend(loc='best', fontsize = 15)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    plt.subplot(2, 1, 2)
    for fm in db.firms:
        plt.plot(round_range, fm.history['profit_history'], label=f"Firm {fm.id}", color=firm_color[fm.id], linewidth = 2.5)

        if db.firms[0].ideal_max_lprofit != db.firms[1].ideal_max_lprofit:
            plt.hlines(fm.ideal_max_lprofit, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dotted', label=f"Bertrand Profit (Firm {fm.id})")
        if db.firms[0].ideal_max_uprofit != db.firms[1].ideal_max_uprofit:
            plt.hlines(fm.ideal_max_uprofit, xmin=1, xmax=round_length, color=firm_color[fm.id], linestyles='dashed', label=f"Cartel Profit (Firm {fm.id})")
    
    if db.firms[0].ideal_max_lprofit == db.firms[1].ideal_max_lprofit:
        plt.hlines(db.firms[0].ideal_max_lprofit, xmin=1, xmax=round_length, color='black', linestyles='dotted', label=f"Bertrand Profit")
    if db.firms[0].ideal_max_uprofit == db.firms[1].ideal_max_uprofit:
        plt.hlines(db.firms[0].ideal_max_uprofit, xmin=1, xmax=round_length, color='black', linestyles='dashed', label=f"Cartel Profit")

    plt.xlabel("Round", fontsize = 20)
    plt.ylabel("Profit", fontsize = 20)
    plt.legend(loc='best', fontsize = 15)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    plt.suptitle("Firms' Decisions During the Simulation")
    #plt.savefig(filename_format.format(fig_filepath = fig_filepath, type = 'overview'), dpi = 600)
    plt.pause(0.1)
    plt.show(block=False)
