# -----------------------------------------------------------------------------
# Preswald Dashboard: "Magnum, B.I. & The Mystery of the Vanishing Profits
# Side-bar adds branding, table of contents, detective reflections, and images.
# Main area presents 10 narrative-driven visualizations in themed detective style.
# -----------------------------------------------------------------------------

import pandas as pd
import plotly.express as px
from preswald import text, plotly, table, sidebar, get_df, selectbox, slider, connect, separator, chat

# Import tomllib from the standard library (Python 3.11+), fallback to tomli for older versions
try:
    import tomllib
except ImportError:
    import tomli as tomllib

connect()

# Utility: Convert all datetime columns to string for serialization
def stringify_dates(df):
    if df is None:
        return None
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)
    return df

# Utility for categories/regions
df = get_df("merged_data")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.strftime('%Y-%m')
df["Profit Margin %"] = df["Profit"] / df["Sales"] * 100
df["Returned"] = df["Returned"].astype(str)

# --- Sidebar ---
sidebar(text("# 🕵🏾‍♂️ Magnum, B.I. — The Mystery of the Vanishing Profits"))
sidebar(text("---"))

# --- Onboarding Section ---
text("""
Welcome, Detective Partner. I'm Magnum B.I.—a specialist in unsolved business mysteries. 
The CEO of Superstore has called us in: Sales are soaring, numbers look golden on paper, but profits aren't 
showing up where expected. Something's fishy in the books and it's up to us to follow the data trail.
""")

text("""
### How to Navigate the Case (Dashboard)
- 🔍 Use filters to explore different aspects of the data
- 📊 Hover over charts for detailed information
- 💡 Look for insights below each visualization
""")


# --- Main Case File ---
text("## Main Case File")
text("### The Evidence Table")
table(stringify_dates(df), title="Original Data")
separator()

threshold = slider("Threshold", min_val=-10000, max_val=10000, default=0)
table(stringify_dates(df[df["Profit"] > threshold]), title="Dynamic Data View Based on Threshold Value")
separator()

text("""
*The Suspects:*  
- Different Regions lurking with mismatched numbers  
- Product Categories & Sub-Categories, some draining resources  
- Discounts that seduce sales but possibly murder profits  
- A rising tide of Returns, quietly eroding our bottom line

Ready to crack the case? Let's follow the trail!
""")


# --- Chapter 1 ---
text("## Chapter 1: The Big Picture — Sales vs. Profit Overview")
text("""
> **Clue 1:** Are big sales always big profit?  
> Each point represents an order. X shows Sales, Y shows Profit, color is Region.  
> Select a Category to see its pattern—do some attract profit, others danger?
""")
selected_category = selectbox("Category (filter)", ["All"] + sorted([str(x) for x in df["Category"].unique() if pd.notnull(x)]), default="All")
if selected_category != "All":
    df1 = df[df["Category"] == selected_category]
else:
    df1 = df
fig1 = px.scatter(
    df1,
    x="Sales", y="Profit", color="Region",
    hover_data=["Category", "Sub-Category", "Discount", "Returned"],
    title="Sales vs. Profit by Region",
    labels={"Sales": "Order Sales ($)", "Profit": "Order Profit ($)", "Region": "Region"},
    opacity=0.7,
)
fig1.update_traces(marker=dict(size=7, line=dict(width=0.5, color='DarkSlateGrey')))
fig1.update_layout(legend_title_text='Region', height=450)
plotly(fig1)
text("> _Magnum B.I.: Some categories look profitable, others risky. Let's see what the calendar tells us..._")


# --- Chapter 2 ---
text("## Chapter 2: The Flow of Time — Sales & Profit Trends")
text("""
> **Clue 2:** Do profits follow sales, or diverge?  
> This line chart tracks Sales and Profit by time.  
> Set the time scale below.
""")
granularity = selectbox("Time Granularity", ["Month", "Year"], default="Month")
if granularity == "Month":
    grp = df.groupby("Month").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    xaxis = "Month"
else:
    grp = df.groupby("Year").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    xaxis = "Year"
fig2 = px.line(
    grp, x=xaxis, y=["Sales", "Profit"],
    labels={xaxis: f"Order {granularity}", "value": "Amount ($)", "variable": ""},
    markers=True, title="Sales and Profit Trend Over Time"
)
fig2.update_layout(legend_title_text="", height=400)
plotly(fig2)
text("> _Magnum B.I.: Do profits lag behind sales, or split off? Time to go regional..._")


# --- Chapter 3 ---
text("## Chapter 3: Regional Suspicions")
text("""
> **Clue 3:** Do all regions pull their weight?  
> See Sales and Profits for each Region.  
> Filter Category to watch shifts in the evidence.
""")
selected_cat3 = selectbox("Category (filter for region)", ["All"] + sorted([str(x) for x in df["Category"].unique() if pd.notnull(x)]), default="All")
df3 = df[df["Category"] == selected_cat3] if selected_cat3 != "All" else df
grp3 = df3.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
fig3 = px.bar(
    grp3, x="Region", y=["Sales", "Profit"], barmode="group",
    labels={"value": "Total Amount ($)", "variable": "", "Region": "Region"},
    title="Total Sales and Profits by Region"
)
fig3.update_layout(legend_title_text="", height=400)
plotly(fig3)
text("> _Magnum B.I.: Some regions might be innocent, others suspicious. What about the product lineup?_")


# --- Chapter 4 ---
text("## Chapter 4: Category Clues")
text("""
> **Clue 4:** What's hiding in each category?  
> Below, a stacked bar shows Profits by Category and Sub-Category.  
> Focus on a Region to reveal its suspects.
""")
selected_region_4 = selectbox("Region (for Category Clues)", ["All"] + sorted([str(x) for x in df["Region"].unique() if pd.notnull(x)]), default="All")
df4 = df[df["Region"] == selected_region_4] if selected_region_4 != "All" else df
grp4 = df4.groupby(["Category", "Sub-Category"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
fig4 = px.bar(
    grp4, x="Category", y="Profit", color="Sub-Category", text="Sales",
    title=f"Profits by Category and Sub-Category{' in ' + selected_region_4 if selected_region_4 != 'All' else ''}",
    labels={"Profit": "Total Profit ($)", "Category": "Category", "Sub-Category": "Sub-Category"},
)
fig4.update_layout(barmode='stack', height=450, legend_title_text='Sub-Category')
plotly(fig4)
text("> _Magnum B.I.: Do some sub-categories betray our trust? Let's spotlight the star and villain performers..._")


# --- Chapter 5 ---
text("## Chapter 5: Top and Bottom Performers")
text("""
> **Clue 5:** Who's making bank—and who's a drain?  
> Horizontal bar ranks the TOP 8 and BOTTOM 2 sub-categories by profit.  
> The worst offenders are painted red—are surprises lurking among our 'usual suspects'?
""")

# Find sub-categories by total profit
grp5 = df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=False)
top8 = grp5.head(8)
bottom2 = grp5.tail(2)
combined = pd.concat([top8, bottom2]).reset_index()
combined['Highlight'] = ['Top'] * 8 + ['Bottom'] * 2

fig5 = px.bar(
    combined.sort_values("Profit", ascending=True),
    x="Profit",
    y="Sub-Category",
    orientation="h",
    color="Highlight",
    color_discrete_map={"Top": "#2C77CE", "Bottom": "#E74C3C"},
    title="Top 8 and Bottom 2 Sub-Categories by Profit",
    labels={"Profit": "Total Profit ($)", "Sub-Category": "Sub-Category", "Highlight": ""},
    text="Profit"
)
fig5.update_layout(height=450)
plotly(fig5)

text("> _Magnum B.I.: Surprised by any 'villains' at the bottom? The price of a sale is about to get murkier..._")


# --- Chapter 6 ---
text("## Chapter 6: The Discount Trap")
text("""
> **Clue 6:** Are discounts more foe than friend?  
> This scatterplot (Discount vs Profit, color by Category) exposes the cost of those tempting deals.  
> Tighten or loosen the discount range below to check its effect.
""")

min_disc = round(float(df["Discount"].min()), 2)
max_disc = round(float(df["Discount"].max()), 2)
if min_disc == max_disc:
    slider_min_disc, slider_max_disc = 0.0, 1.0
else:
    slider_min_disc, slider_max_disc = min_disc, max_disc
selected_disc_range = slider("Discount Range", min_val=slider_min_disc, max_val=slider_max_disc, default=(slider_min_disc, slider_max_disc), step=0.01)
if isinstance(selected_disc_range, (tuple, list)) and len(selected_disc_range) == 2:
    selected_min_disc, selected_max_disc = selected_disc_range
else:
    selected_min_disc = selected_max_disc = slider_min_disc

df6 = df[(df["Discount"] >= selected_min_disc) & (df["Discount"] <= selected_max_disc)]

fig6 = px.scatter(
    df6,
    x="Discount",
    y="Profit",
    color="Category",
    hover_data=["Sales", "Region", "Sub-Category"],
    title="Discount vs. Profit by Category",
    labels={"Discount": "Discount Rate", "Profit": "Order Profit ($)", "Category": "Category"},
    opacity=0.6
)
fig6.update_traces(marker=dict(size=6, line=dict(width=0.5, color='Gray')))
fig6.update_layout(height=420, legend_title_text='Category')
plotly(fig6)

text("> _Magnum B.I.: Is there a point where too much discount means all profit's lost? Now, what about returns?_")


# --- Chapter 7 ---
text("## Chapter 7: Impact of Returns")
text("""
> **Clue 7:** Returns—the unseen profit thief?  
> Grouped bar splits Sales and Profits by Return status for each Region.  
> Filter by Category and see which regions are plagued by product boomerangs.
""")

selected_category_7 = selectbox("Category (filter for returns)", ["All"] + sorted([str(x) for x in df["Category"].unique() if pd.notnull(x)]), default="All")
df7 = df[df["Category"] == selected_category_7] if selected_category_7 != "All" else df
grp7 = df7.groupby(["Region", "Returned"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()

fig7 = px.bar(
    grp7,
    x="Region",
    y="Profit",
    color="Returned",
    barmode="group",
    title=f"Profits by Region & Returned Status{' — ' + selected_category_7 if selected_category_7 != 'All' else ''}",
    labels={"Profit": "Total Profit ($)", "Region": "Region", "Returned": "Returned?"},
    text="Sales"
)
fig7.update_layout(height=420)
plotly(fig7)

text("> _Magnum B.I.: Who knew returns could bleed a region dry? Let's look at profitability in sharper focus..._")


# --- Chapter 8 ---
text("## Chapter 8: Profit Margin Heatmap")
text("""
> **Clue 8:** Where does profit really melt away?  
> The heatmap's colors show profit margin percent for every Category (rows) and Region (columns).  
> Red is where margin vanishes; green is healthy.
""")

heatmap_df = df.pivot_table(
    values="Profit Margin %",
    index="Category",
    columns="Region",
    aggfunc="mean"
).round(2)

fig8 = px.imshow(
    heatmap_df,
    color_continuous_scale='RdYlGn',
    labels=dict(x="Region", y="Category", color="Profit Margin (%)"),
    title="Profit Margin by Category and Region"
)
fig8.update_xaxes(side="top")
fig8.update_layout(height=370)
plotly(fig8)

text("> _Magnum B.I.: Which combination is our biggest danger zone? Let's trace when trouble built up..._")


# --- Chapter 9 ---
text("## Chapter 9: Timeline of Trouble")
text("""
> **Clue 9:** When did things start sinking?  
> Here's cumulative negative profit (losses) by time—how fast, and when, have things turned sour?
""")

df_loss = df[df["Profit"] < 0].sort_values("Order Date")
if not df_loss.empty:
    cumsum_loss_df = df_loss.groupby("Month")["Profit"].sum().cumsum().reset_index()
    cumsum_loss_df.rename(columns={"Profit": "Cumulative Loss"}, inplace=True)
    fig9 = px.area(
        cumsum_loss_df,
        x="Month",
        y="Cumulative Loss",
        title="Cumulative Losses Over Time (Negative Profits Only)",
        labels={"Month": "Month", "Cumulative Loss": "Cumulative Loss ($)"},
    )
    fig9.update_traces(line_color="#A93226")
    fig9.update_layout(height=380)
    plotly(fig9)
else:
    text("_(No negative profit orders found in data!)_")

text("> _Magnum B.I.: Trouble might come in waves—or as a timeless drip. Who are the real culprits?_")


# --- Chapter 10 ---
text("## Chapter 10: The Final Case File")
text("""
> **Final Clue:** Who—or what—is truly to blame?  
> This pie chart shows how much each prime suspect (Regions, Categories, Heavy Discounts, Returns) contributed to overall losses.  
> Examine the evidence and deliver your verdict!
""")

region_loss = df[df["Profit"] < 0].groupby("Region")["Profit"].sum().abs()
category_loss = df[df["Profit"] < 0].groupby("Category")["Profit"].sum().abs()
returns_loss = df[df["Returned"].str.lower().str.startswith("y")]["Profit"].sum()
heavy_discount_loss = df[(df["Profit"] < 0) & (df["Discount"] > 0.3)]["Profit"].sum()

labels = []
values = []
if not region_loss.empty:
    labels.append("Regions (max loss)")
    values.append(region_loss.max())
if not category_loss.empty:
    labels.append("Categories (max loss)")
    values.append(category_loss.max())
if pd.notnull(returns_loss):
    labels.append("Returns")
    values.append(abs(returns_loss))
if pd.notnull(heavy_discount_loss):
    labels.append("Heavy Discounts")
    values.append(abs(heavy_discount_loss))

fig10 = px.pie(
    names=labels,
    values=values,
    color_discrete_sequence=['#2C77CE', '#A93226', '#F7DC6F', '#979A9A'],
    title="Loss Attribution: Suspects' Shares of Total Losses"
)
fig10.update_traces(textinfo='percent+label', pull=[0.07 if label == 'Returns' else 0.01 for label in labels])
fig10.update_layout(height=400)
plotly(fig10)


text("""
**Case Closed:**  
So detective, who's the true culprit behind Superstore's vanishing profits?  
Was it a regional slump, product appetite gone bad, the sweet poison of discounts, or the slow bleed of returns?  
Whatever you decide, you've followed the data trail with true detective grit!

**Thank you for helping Magnum B.I. close the Mystery of the Vanishing Profits. Case dismissed!**
""")


# Get all data sources
with open("preswald.toml", "rb") as f:
    config = tomllib.load(f)

source_list = []
for source_path in config["data"]:
    source_list.append(source_path)
 
# Create a selectbox for choosing a column to visualize
source_choice = selectbox(
    label="Choose a dataset as chat source",
    options=source_list,
)

# Create an AI chat window using the selected source!
chat(source_choice)
