from utils import load_pkl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_automation_chart():

    automation_stats_path = "evaluations/stats/automations_stats.pkl"
    automation_df = load_pkl(automation_stats_path)

    #Change the order
    custom_order = ['WikidataTables2024R1', 'HardTablesR1', 'BiodivTab_DBP_2022', 'Kaggle_Diverse_CSV_DS', 'GTFS-Madrid']
    automation_df = automation_df.reindex(custom_order)
    print(automation_df)

    columns = automation_df.columns

    # Normalize mtab values to 100%
    mtab_columns = automation_df[[columns[i] for i in range(3)]]
    mtab_row_sums = mtab_columns.sum(axis=1)
    automation_df[[columns[i] for i in range(3)]] = mtab_columns.div(mtab_row_sums, axis=0)*100

    # Normalize torchictab values to 100%
    torchictab_columns = automation_df[[columns[i] for i in range(3,6)]]
    torchictab_row_sums = torchictab_columns.sum(axis=1)
    automation_df[[columns[i] for i in range(3,6)]] = torchictab_columns.div(torchictab_row_sums, axis=0)*100
    # print(automation_df)

    # Bar chart data
    mtab_fully = automation_df['Number of Automated Constructed KGs w/ mtab']
    mtab_semi = automation_df['Number of Semi-Automated Constructed KGs w/ mtab']
    mtab_failed = automation_df['Number of Failed Constructions w/ mtab']

    torchictab_fully = automation_df['Number of Automated Constructed KGs w/ torchictab']
    torchictab_semi = automation_df['Number of Semi-Automated Constructed KGs w/ torchictab']
    torchictab_failed = automation_df['Number of Failed Constructions w/ torchictab']

    # Combine mtab and torchictab into one dataset for plotting
    collections = automation_df.index
    x = np.arange(len(collections))  # X-axis positions

    # Plotting
    bar_width = 0.25  # Width of each bar group

    fig, ax = plt.subplots(figsize=(10, 6))

    # Stacked bars for mtab
    ax.bar(x - bar_width / 2, mtab_fully, width=bar_width, label='Fully Automated\n(w/ mtab)', color='#FF7F0E')
    ax.bar(x - bar_width / 2, mtab_semi, width=bar_width, bottom=mtab_fully, label='Semi-Automated\n(w/ mtab)', color='#FFBB78')
    ax.bar(x - bar_width / 2, mtab_failed, width=bar_width, bottom=mtab_fully + mtab_semi, label='Failed\n(w/ mtab)', color='#F5F5F5')

    # Stacked bars for torchictab
    ax.bar(x + bar_width / 2, torchictab_fully, width=bar_width, label='Fully Automated\n(w/ torchictab)', color='#1F77B4')
    ax.bar(x + bar_width / 2, torchictab_semi, width=bar_width, bottom=torchictab_fully, label='Semi-Automated\n(w/ torchictab)', color='#AEC7E8')
    ax.bar(x + bar_width / 2, torchictab_failed, width=bar_width, bottom=torchictab_fully + torchictab_semi, label='Failed\n(w/ torchictab)', color='#D3D3D3')

    # Formatting the chart
    ax.set_ylabel('Percentage (%)')
    #ax.set_title('KG Construction Automation Assessment (Percentage)')
    ax.set_xticks(x)
    ax.set_xticklabels(collections, rotation=0)
    ax.legend(loc='upper left', ncols=3) 
    ax.set_ylim(0, 150,)  # Extend the y-axis limit to 110% to add whitespace
    ax.set_yticks(range(0, 101, 20))

    # Add labels under bars for 'mtab' and 'torchictab'
    # for i, dataset in enumerate(collections):
    #     ax.text(x[i] - bar_width / 2, -7, 'mtab', ha='center', va='center', fontsize=10)
    #     ax.text(x[i] + bar_width / 2, -7, 'torchictab', ha='center', va='center', fontsize=10)

    # Display the chart
    plt.tight_layout()
    plt.show()
    return


def generate_accuracy_chart():

    accuracy_stats_path = "evaluations/stats/accuracy_stats_path.pkl"
    accuracy_df = load_pkl(accuracy_stats_path)

    indices = ['WikidataTables2024R1', 'HardTablesR1']
    correctly_annotatated = accuracy_df["Number of Correctly Annotated Tables w/ mtab"].tolist() + (
                            accuracy_df["Number of Correctly Annotated Tables w/ torchictab"].tolist()
    )
    accurate_graphs = accuracy_df["Number of Accurate Graphs w/ mtab"].tolist() + (
                            accuracy_df["Number of Accurate Graphs w/ torchictab"].tolist()
    )

    pairs = ('WikidataTables2024R1 w/ Mtab', 'WikidataTables2024R1 w/ TorchicTab', 'HardTablesR1 w/ Mtab', 'HardTablesR1 w/ TorchicTab')
    accuracy_dict = {
        "Correctly annotated tables": tuple(correctly_annotatated),
        "Accurate graphs constructed": tuple(accurate_graphs)
    }
    
    x = np.arange(len(pairs))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in accuracy_dict.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Number of correctly annot')
    #ax.set_title('Penguin attributes by species')
    ax.set_xticks(x + width/2, pairs)
    ax.legend(loc='upper left', ncols=2)
    ax.set_ylim(0, 280)

    plt.show()


    return

if __name__ == "__main__":

    pd.set_option('display.max_columns', None)
    generate_automation_chart()
    # generate_accuracy_chart()