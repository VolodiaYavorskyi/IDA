import pandas as pd
import lab1_plots


def parse_data(loc):
    data = pd.read_csv(loc, sep=';')

    data["day/month"] = pd.to_datetime(data["day/month"] + ".2019")
    data = data.rename(columns={"day/month": "Date"})
    data = data.set_index("Date")

    data["Time"] = pd.to_datetime(data["Time"]).dt.strftime("%H:%M")
    data["Humidity"] = data["Humidity"].str[:-1].astype("float") / 100.0
    data["Wind Speed"] = data["Wind Speed"].str[:-4].astype("int64")
    data["Wind Gust"] = data["Wind Gust"].str[:-4].astype("int64")
    data["Pressure"] = data["Pressure"].str.replace(',', '.').astype("float")

    return data


df = parse_data("DATABASE.csv")

columns = ["Time", "Temperature", "Dew Point", "Humidity", "Wind", "Wind Speed",
           "Wind Gust", "Pressure", "Precip.", "Precip Accum", "Condition"]
plots = ["line", "bar", "scatter"]
gdf = df.groupby(df.index)

lab1_plots.numericPlot(gdf.mean(), columns[1], plots[1])
lab1_plots.numericPlot2(gdf.mean(), columns[1], columns[2], plots[2])
lab1_plots.pieChart(df, columns[-1])
