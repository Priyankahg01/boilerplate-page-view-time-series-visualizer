import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    index_col="date",
    parse_dates=True
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


# Draw line plot
def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df_line.index, df_line["value"])

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


# Draw bar plot
def draw_bar_plot():
    df_bar = df.copy()

    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    df_bar = df_bar.groupby(
        ["year", "month"]
    )["value"].mean().unstack()

    df_bar = df_bar.rename(
        columns={
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
    )

    fig = df_bar.plot(
        kind="bar",
        figsize=(10, 6)
    ).figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig


# Draw box plot
def draw_box_plot():
    df_box = df.copy()

    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.month

    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    df_box["month_name"] = df_box["month"].map(
        dict(enumerate(month_order, 1))
    )

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        x="month_name",
        y="value",
        data=df_box,
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig