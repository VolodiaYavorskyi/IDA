import matplotlib.pyplot as plt

colors = {"new_death": "tab:red", "new_confirm": "tab:orange", "new_susp": "tab:blue", "new_recover": "tab:green"}
colormaps = {"new_death": "Reds", "new_confirm": "Oranges", "new_susp": "Blues", "new_recover": "Greens"}


def plot_area(dynamics, area):
    dyn = dynamics[dynamics["registration_area"] == area]
    dyn.plot(x="zvit_date", kind="area", color=colors)
    plt.title("COVID-19 " + area + " statistics")
    plt.xlabel("Date")
    plt.ylabel("People")
    plt.show()


def plot_compare(dynamics, column, area_list):
    n = len(area_list)
    dyn_list = []
    for i in range(n):
        dyn_list.append(dynamics[dynamics["registration_area"] == area_list[i]])
    ax = dyn_list[0].plot(x="zvit_date", y=column, label=area_list[0])
    for i in range(1, n):
        dyn_list[i].plot(x="zvit_date", y=column, label=area_list[i], ax=ax)
    ar_str = ""
    for i in range(n):
        ar_str += " " + area_list[i] + ","
    ar_str = ar_str[:-1]
    plt.title("COVID-19" + ar_str + " comparison")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("People")
    plt.show()


def plot_map(map_df, col):
    map_df.plot(cmap=colormaps[col], column=col, edgecolor="0.5", figsize=(12.0, 8.0),
                missing_kwds={"color": "lightgrey", "hatch": "//"})
    vmin, vmax = map_df[col].min(), map_df[col].max()
    sm = plt.cm.ScalarMappable(cmap=colormaps[col], norm=plt.Normalize(vmin=vmin, vmax=vmax))
    plt.colorbar(sm)
    plt.title("Ukraine COVID-19 " + col + " (last week)")
    plt.axis("off")
    plt.show()
