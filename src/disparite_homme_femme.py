# %%
import pandas as pd


# %% [markdown]
# # Load dataset

# %%
people = pd.read_csv("dataset/taxonomies/personnality.csv")
people = people[people["gender"] != "none"]
def explode_by_people(df):
    df.drop_duplicates()
    df["personality_ids"] = df["personality_ids"].str.split(pat="|")
    df = df.explode("personality_ids")
    df = df.merge(people, left_on="personality_ids", right_on="uuid")
    df = df[df["gender"] != "none"]
    return df


france_culture = explode_by_people(pd.read_csv("dataset/grid/franceculture.csv"))

france_info = explode_by_people(pd.read_csv("dataset/grid/franceinfo.csv"))
france_inter = explode_by_people(pd.read_csv("dataset/grid/franceinter.csv"))
all_grids = pd.concat([france_culture, france_info, france_inter], ignore_index=True)
all_grids.head()

def filter_by_hour(df, hour):
    return df[df.diffusion_start_date.str.contains(f"^.{{11}}{hour:02}.{{6}}$", regex=True)]

def filter_by_month(df, month):
    return df[df.diffusion_start_date.str.contains(f"^{month}", regex=True)]


def get_hours_breakdown(df):
    return [filter_by_hour(df, hour) for hour in range(24)]

month_list = [f"2022-{x:02}" for x in range(1, 13)] + [f"2023-{x:02}" for x in range(1, 10)]
def get_by_months(df):
    return [filter_by_month(df, month) for month in month_list]

all_hours = get_hours_breakdown(all_grids)
culture_hours = get_hours_breakdown(france_culture)
info_hours = get_hours_breakdown(france_info)
inter_hours = get_hours_breakdown(france_inter)

all_months = get_by_months(all_grids)
culture_months = get_by_months(france_culture)
info_months = get_by_months(france_info)
inter_months = get_by_months(france_inter)


# %%
all_grids.gender.value_counts()


# %% [markdown]
# Let's plot this data in a horizontal bar chart.

# %%
import matplotlib.pyplot as plt

def color_map(name) -> str:
    if name == "man":
        return "mediumvioletred"
    if name == "woman":
        return "mediumaquamarine"
    return "crimson"

def get_ratio(data):
    other_number = 0 if "other" not in data else data.other
    return data.man / (data.man + data.woman + other_number)
 

def get_safe(df, value):
    return 0 if value not in df else df[value]

def plot_hours(name, df):
    fig, ax = plt.subplots()

    datas = [hour.gender.value_counts() for hour in df]

    man_data = [get_safe(data, "man") for data in datas]
    woman_data = [get_safe(data, "woman") for data in datas]
    other_data = [get_safe(data, "other") for data in datas]

    ax.set_title(name)
    ax.set_xlabel("Hour of the day")
    ax.set_ylabel("Number of participants")
    ax.plot(man_data, label = "man", color=color_map("man"))
    ax.plot(woman_data, label = "woman", color=color_map("woman"))
    ax.plot(other_data, label = "other", color=color_map("other"))
    ax.set_xticks([x for x in range(24)])
    ax.legend()

def plot_months(name, df):

    fig, ax = plt.subplots()
    datas = [hour.gender.value_counts() for hour in df]

    man_data = [get_safe(data, "man") for data in datas]
    woman_data = [get_safe(data, "woman") for data in datas]
    other_data = [get_safe(data, "other") for data in datas]

    ax.set_title(name)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of participants")
    ax.plot(man_data, label = "man", color=color_map("man"))
    ax.plot(woman_data, label = "woman", color=color_map("woman"))
    ax.plot(other_data, label = "other", color=color_map("other"))
    ax.set_xticks([x for x in range(21) if x % 5 == 0], labels=[x for index, x in enumerate(month_list) if index % 5 == 0])
    ax.legend()

def do_plot(name, df):
    fig, ax = plt.subplots()

    data = df.gender.value_counts()
    labels = data.index
    colors = [color_map(x) for x in labels]

    ax.barh(labels, data, color=colors)

    ratio = get_ratio(data)
    ax.set_ylabel(f"Gender")
    ax.set_xlabel('Number of appearances')
    ax.set_title(f"{name}: {ratio * 100:.2f}%")
    ax.invert_yaxis()

do_plot("Overall", all_grids)
plt.savefig("assets_build/Overall.png")
do_plot("France culture", france_culture)
plt.savefig("assets_build/France culture.png")
do_plot("France info", france_info)
plt.savefig("assets_build/France info.png")
do_plot("France inter", france_inter)
plt.savefig("assets_build/France inter.png")

plot_hours("Overall", all_hours)
plt.savefig("assets_build/Overall_hours.png")
plot_hours("France culture", culture_hours)
plt.savefig("assets_build/France culture_hours.png")
plot_hours("France info", info_hours)
plt.savefig("assets_build/France info_hours.png")
plot_hours("France inter", inter_hours)
plt.savefig("assets_build/France inter_hours.png")

plot_months("Overall", all_months)
plt.savefig("assets_build/Overall_months.png")
plot_months("France culture", culture_months)
plt.savefig("assets_build/France culture_months.png")
plot_months("France info", info_months)
plt.savefig("assets_build/France info_months.png")
plot_months("France inter", inter_months)
plt.savefig("assets_build/France inter_months.png")

plt.show()
