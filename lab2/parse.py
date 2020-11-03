import pandas as pd
import geopandas as gpd
from lab2 import my_plots

base_commands = ["show area statistics", "compare area dynamics", "show statistics on map", "write statistics to excel"]
areas = ["Івано-Франківська", "Волинська", "Вінницька", "Дніпропетровська",
         "Донецька", "Житомирська", "Закарпатська", "Запорізька", "Київська",
         "Кіровоградська", "Луганська", "Львівська", "Миколаївська", "Одеська",
         "Полтавська", "Рівненська", "Сумська", "Тернопільська", "Харківська",
         "Херсонська", "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська",
         "м. Київ"]
columns = ["new_susp", "new_confirm",
           "new_death", "new_recover"]


def parse_data(loc):
    dyn = pd.read_csv(loc)
    dyn = dyn.drop(columns=["active_confirm"])
    dyn = dyn.groupby(["zvit_date", "registration_area"]).sum().reset_index()
    return dyn


def parse_map_data(zipfile):
    mdf = gpd.read_file(zipfile)
    mdf = mdf.replace({"Chernihiv": "Чернігівська",
                       "Donets'k": "Донецька",
                       "Dnipropetrovs'k": "Дніпропетровська",
                       "Luhans'k": "Луганська",
                       "L'viv": "Львівська",
                       "Ivano-Frankivs'k": "Івано-Франківська",
                       "Odessa": "Одеська",
                       "Poltava": "Полтавська",
                       "Kiev": "Київська",
                       "Chernivtsi": "Чернівецька",
                       "Kharkiv": "Харківська",
                       "Kirovohrad": "Кіровоградська",
                       "Volyn": "Волинська",
                       "Rivne": "Рівненська",
                       "Transcarpathia": "Закарпатська",
                       "Zhytomyr": "Житомирська",
                       "Vinnytsya": "Вінницька",
                       "Mykolayiv": "Миколаївська",
                       "Kiev City": "м. Київ",
                       "Ternopil'": "Тернопільська",
                       "Cherkasy": "Черкаська",
                       "Kherson": "Херсонська",
                       "Khmel'nyts'kyy": "Хмельницька",
                       "Sumy": "Сумська",
                       "Zaporizhzhya": "Запорізька"})
    return mdf


def merge_df(map_df, dynamics):
    left = map_df.rename(columns={"NAME_1": "registration_area"})
    last_week = dynamics["zvit_date"].unique()[-7:]
    dynamics_lw = dynamics[dynamics["zvit_date"].isin(last_week)]
    right = dynamics_lw.groupby("registration_area").sum()
    res = left.merge(right, how="left", on="registration_area")
    return res


def main_menu(dynamics, map_df):
    show_options(base_commands)
    print("0 - exit")
    com = get_command("Command: ", range(len(base_commands) + 1))
    if com == 1:
        show_options(areas)
        area = get_command("Area: ", range(1, len(areas) + 1))
        my_plots.plot_area(dynamics, areas[area - 1])
    elif com == 2:
        show_options(columns)
        col = get_command("Column: ", range(1, len(columns) + 1))
        show_options(areas)
        ars = get_areas("Areas (by space): ", range(1, len(areas) + 1))
        my_plots.plot_compare(dynamics, columns[col - 1], ars)
    elif com == 3:
        show_options(columns)
        col = get_command("Column: ", range(1, len(columns) + 1))
        my_plots.plot_map(map_df, columns[col - 1])
    elif com == 4:
        to_excel(dynamics)
    else:
        return False
    return True


def get_command(text, vals):
    fl = True
    while fl:
        fl = False
        print(text, end='')
        c = int(input())
        if c not in vals:
            fl = True
    return c


def get_areas(text, vals):
    fl = True
    while fl:
        fl = False
        print(text, end='')
        c = [int(i) for i in input().split()]
        c = list(set(c))
        if len(c) < 2:
            fl = True
        for x in c:
            if x not in vals:
                fl = True
    res = [areas[i - 1] for i in c]
    return res


def show_options(options):
    n = len(options)
    for i in range(n):
        print(i + 1, "-", options[i])


def to_excel(dynamics):
    area_stats = dynamics.groupby("registration_area").sum()
    unique = dynamics["registration_area"].unique()
    with pd.ExcelWriter("stats.xlsx") as writer:
        area_stats.to_excel(writer, sheet_name="Area_statistics")
        for area in unique:
            curr = dynamics[dynamics["registration_area"] == area].describe()
            curr.to_excel(writer, sheet_name=area)


def main():
    # dynamics = parse_data("covid19_by_area_type_hosp_dynamics.csv")
    url = "https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_area_type_hosp_dynamics.csv"
    dynamics = parse_data(url)

    map_df = parse_map_data("zip:///Users/1/PycharmProjects/IDA/lab2/UKR_adm.zip!UKR_adm1.shp")
    map_df = merge_df(map_df, dynamics)

    flag = True
    while flag:
        flag = main_menu(dynamics, map_df)


if __name__ == "__main__":
    main()
