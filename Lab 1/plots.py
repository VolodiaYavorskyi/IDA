import matplotlib.pyplot as plt


def numericPlot(dataframe, column, pl_type):
    fig, ax = plt.subplots()

    if pl_type == "bar":
        dataframe = dataframe.groupby(dataframe.index).max()
        ax.bar(dataframe.index, dataframe[column], label=column)
        ax.set_title("Bar plot")
    elif pl_type == "scatter":
        dataframe = dataframe.groupby(dataframe.index).max()
        ax.scatter(dataframe.index, dataframe[column], label=column)
        ax.set_title("Scatter plot")
    elif pl_type == "hist":
        ax.hist(dataframe[column], bins=10, label=column)
        ax.set_title("Histogram")
        ax.set_xlabel(column)
        plt.show()
        return
    elif pl_type == "pie":
        stats = dataframe.value_counts(column)
        ax.pie(stats, autopct='%1.1f%%')
        ax.legend(stats.index, fontsize="x-small", loc='best', bbox_to_anchor=(0.8, 0.65, 0.5, 0.5))
        ax.set_title("Pie chart")
        plt.show()
        return
    else:
        dataframe = dataframe.groupby(dataframe.index).max()
        ax.plot(dataframe.index, dataframe[column], label=column)
        ax.set_title("Line plot")
    ax.legend()
    ax.set_xlabel("Date")
    plt.xticks(dataframe.index, rotation='vertical')
    plt.subplots_adjust(bottom=0.3)
    plt.show()


def numericPlot2(dataframe, column1, column2, pl_type):
    dataframe = dataframe.groupby(dataframe.index).max()
    fig, ax = plt.subplots()

    if pl_type == "bar":
        ax.bar(dataframe.index, dataframe[column1], label=column1)
        ax.bar(dataframe.index, dataframe[column2], label=column2)
        ax.set_title("Bar plot")
    elif pl_type == "scatter":
        ax.scatter(dataframe.index, dataframe[column1], label=column1)
        ax.scatter(dataframe.index, dataframe[column2], label=column2)
        ax.set_title("Scatter plot")
    else:
        ax.plot(dataframe.index, dataframe[column1], label=column1)
        ax.plot(dataframe.index, dataframe[column2], label=column2)
        ax.set_title("Line plot")
    ax.legend()
    ax.set_xlabel("Date")
    plt.xticks(dataframe.index, rotation='vertical')
    plt.subplots_adjust(bottom=0.3)
    plt.show()
