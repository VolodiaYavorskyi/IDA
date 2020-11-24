import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
from lab3 import my_plots

base_commands = ["show raw correlation", "show lag correlation",
                 "predict cases for area by leader", "predict cases for area by 3 leaders"]
areas = ["Івано-Франківська", "Волинська", "Вінницька", "Дніпропетровська",
         "Донецька", "Житомирська", "Закарпатська", "Запорізька", "Київська",
         "Кіровоградська", "Луганська", "Львівська", "Миколаївська", "Одеська",
         "Полтавська", "Рівненська", "Сумська", "Тернопільська", "Харківська",
         "Херсонська", "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська",
         "м. Київ"]


def main_menu():
    print()
    show_options(base_commands)
    print("0 - exit")
    com = get_command("Command: ", range(len(base_commands) + 1))
    if com == 1:
        my_plots.plot_raw_correlation(dynamics)
    elif com == 2:
        lag_max = get_command("Max lag (1-50): ", range(1, 51))
        ldf, cdf = lag_df(lag_max)
        my_plots.plot_lag_correlation(ldf, cdf, lag_max)
    elif com == 3:
        show_options(areas)
        area = get_command("Area for prediciton: ", range(1, len(areas) + 1))
        leaders = get_leaders(areas[area - 1], 1)
        print("Leader: ", list(leaders))
        pr = predict_cases(areas[area - 1], leaders)
        my_plots.plot_prediction(pr, areas[area - 1])
    elif com == 4:
        show_options(areas)
        area = get_command("Area for prediciton: ", range(1, len(areas) + 1))
        leaders = get_leaders(areas[area - 1], 3)
        print("Leaders: ", list(leaders))
        pr = predict_cases(areas[area - 1], leaders)
        my_plots.plot_prediction(pr, areas[area - 1])
    else:
        return False
    return True


def get_command(text, vals):
    print(text, end='')
    c = int(input())
    while c not in vals:
        print(text, end='')
        c = int(input())
    return c


def show_options(options):
    n = len(options)
    for i in range(n):
        print(i + 1, "-", options[i])


def parse_data(loc):
    dyn = pd.read_csv(loc)
    dyn = dyn[["zvit_date", "registration_area", "active_confirm"]]
    dyn = dyn.groupby(["zvit_date", "registration_area"]).sum().reset_index()
    return dyn


def format_data(dyn):
    unique_area = dyn["registration_area"].unique()
    unique_date = dyn["zvit_date"].unique()
    res = pd.DataFrame({"zvit_date": unique_date})
    for area in unique_area:
        right = dyn[dyn["registration_area"] == area]
        right = right.drop(columns=["registration_area"])
        right = right.rename(columns={"active_confirm": area})
        res = res.merge(right, how="left", on="zvit_date")
    return res


def lag_corr(area1, area2, lag):
    lag_max, corr_max = 0.0, 0.0
    df_shifted = dynamics[[area1, area2]].copy()
    df_shifted[area2] = df_shifted[area2].shift(-lag - 1)
    for lag_curr in range(-lag, lag + 1):
        df_shifted[area2] = df_shifted[area2].shift(1)
        curr_corr = df_shifted[area1].corr(df_shifted[area2])
        if curr_corr > corr_max:
            lag_max, corr_max = lag_curr, curr_corr
    return lag_max, corr_max


def lag_df(lag):
    a_u = dynamics.columns[1:]
    df_lag = pd.DataFrame(columns=a_u, index=a_u, dtype="float64")
    df_corr = pd.DataFrame(columns=a_u, index=a_u, dtype="float64")
    n = len(a_u)
    for i in range(n):
        a1 = a_u[i]
        for j in range(n):
            a2 = a_u[j]
            if i == j:
                df_lag.at[a1, a2] = 0
                df_corr.at[a1, a2] = 1.0
            else:
                lag_a1_a2, corr_a1_a1 = lag_corr(a1, a2, lag)
                df_lag.at[a1, a2] = lag_a1_a2
                df_corr.at[a1, a2] = corr_a1_a1
    return df_lag, df_corr


def get_leaders(area, num):
    lag_max = 100
    a_u = dynamics.columns[1:]
    n = len(a_u)
    corrs = pd.Series(index=a_u, dtype="int64")
    for i in range(n):
        ar = a_u[i]
        if ar == area:
            corrs.loc[ar] = 0
        else:
            lag_curr, corr_curr = lag_corr(area, ar, lag_max)
            if lag_curr >= 7:
                corrs.loc[ar] = corr_curr
            else:
                corrs.loc[ar] = -1.0
    res = corrs.nlargest(num).index
    return res


def predict_cases(pr_area, tr_areas):
    # max lag allowed
    lag_max = 100
    # empty data frames
    tdf = pd.DataFrame()
    pdf = pd.DataFrame()
    pred = pd.DataFrame()
    # fill train and prediction data frames
    tdf[pr_area] = dynamics[pr_area].copy()
    for tr_area in tr_areas:
        lag_curr = lag_corr(pr_area, tr_area, lag_max)[0]
        tdf[tr_area] = dynamics[tr_area].copy()
        tdf[tr_area] = tdf[tr_area].shift(lag_curr)
        temp = dynamics[tr_area].iloc[-lag_curr:-lag_curr + 7].reset_index()
        pdf[tr_area] = temp[tr_area]
    # group data on train and test
    tdf = tdf.dropna()
    x_train = tdf[tr_areas].head(-7)
    y_train = tdf[pr_area].head(-7)
    x_test = tdf[tr_areas].tail(7)
    y_test = tdf[pr_area].tail(7)
    # train and test regression model
    reg = LinearRegression(normalize=True).fit(x_train, y_train)
    print("Train score:", reg.score(x_train, y_train))
    print("Test score:", reg.score(x_test, y_test))
    # predict cases for area
    x = tdf[tr_areas].append(pdf[tr_areas])
    pred["prediction"] = reg.predict(x)
    y = y_train.append(y_test).reset_index()[pr_area]
    pred[pr_area] = y
    # add dates
    right = dynamics[["zvit_date", pr_area]].dropna()
    pred = pred.merge(right, how="left", on=pr_area)
    # replace None dates
    first_na = pred[pr_area].isna().idxmax()
    for i in range(first_na, first_na + 7):
        date_prev = str(pred.iloc[i - 1]["zvit_date"])
        last_day = datetime.date.fromisoformat(date_prev)
        pred.loc[i, "zvit_date"] = last_day + datetime.timedelta(days=1)
    pred = pred.set_index("zvit_date")
    return pred


if __name__ == "__main__":
    dynamics = parse_data("covid19_by_area_type_hosp_dynamics.csv")
    # url = "https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_area_type_hosp_dynamics.csv"
    # dynamics = parse_data(url)

    dynamics = format_data(dynamics)

    flag = True
    while flag:
        flag = main_menu()
