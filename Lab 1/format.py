import pandas as pd
import lab1_plots

columns = ["Time", "Temperature", "Dew Point", "Humidity", "Wind", "Wind Speed",
           "Wind Gust", "Pressure", "Precip.", "Precip Accum", "Condition"]
plots = ["line", "bar", "scatter", "hist", "pie"]


def parse_data(loc):
    data = pd.read_csv(loc, sep=';')

    ind = "day/month"
    data[ind] = pd.to_datetime(data[ind] + ".2019")
    data = data.rename(columns={"day/month": "Date"})
    data = data.set_index("Date")

    data[columns[0]] = pd.to_datetime(data[columns[0]]).dt.strftime("%H:%M")
    data[columns[3]] = data[columns[3]].str[:-1].astype("float") / 100.0
    data[columns[5]] = data[columns[5]].str[:-4].astype("int64")
    data[columns[6]] = data[columns[6]].str[:-4].astype("int64")
    data[columns[7]] = data[columns[7]].str.replace(',', '.').astype("float")

    return data


def printColumns():
    for i in range(len(columns)):
        print(i + 1, "-", columns[i])


def getCommand(text, vals):
    print(text, end='')
    c = int(input())
    while c not in vals:
        print(text, end='')
        c = int(input())
    return c


df = parse_data("DATABASE.csv")

com1, com2, col1, col2 = -1, -1, -1, -1

while com1 != 0:
    print("1 - line plot")
    print("2 - bar plot")
    print("3 - scatter plot")
    print("4 - histogram")
    print("5 - pie chart")
    print("0 - exit")
    com1 = getCommand("Command: ", [0, 1, 2, 3, 4, 5])

    if com1 in [1, 2, 3]:
        print("1 - one column")
        print("2 - two columns")
        com2 = getCommand("Command: ", [1, 2])

        if com2 == 2:
            printColumns()
            col1 = getCommand("Column 1:", range(1, 12))
            col2 = getCommand("Column 2:", range(1, 12))
            lab1_plots.numericPlot2(df, columns[col1 - 1], columns[col2 - 1], plots[com1 - 1])
        else:
            printColumns()
            col1 = getCommand("Column:", range(1, 12))
            lab1_plots.numericPlot(df, columns[col1 - 1], plots[com1 - 1])
    elif com1 == 4:
        printColumns()
        col1 = getCommand("Column:", range(1, 12))
        lab1_plots.numericPlot(df, columns[col1 - 1], plots[com1 - 1])
    elif com1 != 0:
        printColumns()
        col1 = getCommand("Column: ", range(1, 12))
        lab1_plots.numericPlot(df, columns[col1 - 1], plots[com1 - 1])
