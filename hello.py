#!/usr/bin/env python3


# Preswald "Mystery of the Vanishing Profits" – Superstore Detective Dashboard

# Data source: merged_data.csv

# All code uses PRESWALD SDK components only, with full, immersive story and 10 detailed visualizations.

# All sections are introduced narratively, with clear, user-facing instructions, controls, and transitions.



import pandas as pd

import plotly.express as px

from preswald import get_df, text, plotly, selectbox, slider



# ========================================

# 0. NARRATIVE HOOK – THE CASE BEGINS

# ========================================



text("# 🕵️ Mystery of the Vanishing Profits")



text("""

**Case File: Superstore – The Vanishing Profits**



Welcome, Detective Partner. I'm Magnum B.I.—a specialist in unsolved business mysteries. The CEO of Superstore has called us in: Sales are soaring, numbers look golden on paper, but profits aren't showing up where expected. Something's fishy in the books and it's up to us to follow the data trail.



**The Suspects:**  

- Different Regions lurking with mismatched numbers  

- Product Categories & Sub-Categories, some draining resources  

- Discounts that seduce sales but possibly murder profits  

- A rising tide of Returns, quietly eroding our bottom line



Together, we'll comb through the evidence in 10 steps—chapter by chapter, clue by clue—until the true culprit is revealed.



Ready to crack the case? Let's follow the trail!

""")



# ========================================

# Load Data

# ========================================



df = get_df("merged_data")  # Preswald-imported; expect 'merged_data.csv'
if df is None:
    raise RuntimeError("Could not load DataFrame for 'merged_data'. Check your preswald.toml and data file.")



# Ensure types are correct for filtering/plotting

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
df["Year"] = df["Order Date"].dt.year

df["Month"] = df["Order Date"].dt.strftime('%Y-%m')



# Derived columns for transforms

df["Profit Margin %"] = df["Profit"] / df["Sales"] * 100

df["Returned"] = df["Returned"].astype(str)  # May be Y/N or True/False as string



# ========================================

# 1. CHAPTER 1: The Big Picture — Sales vs. Profit Overview

# ========================================



text("## Chapter 1: The Big Picture — Sales vs. Profit Overview")



text("""

**Clue 1:** Do great sales really add up to big profits?  

Here, each point is one order in the data. The x-axis shows Sales, y-axis shows Profits. Points are colored by Region.  

**Try selecting a Category:** Are some categories always profitable, or do some bring high sales but little (or negative) profit?

""")

# Preswald dropdown for Category filtering (default: All)

categories = ["All"] + sorted([str(x) for x in df["Category"].unique() if pd.notnull(x)])

selected_category = selectbox("Category (filter)", categories, default="All")



if selected_category != "All":
	
	df_ch1 = df[df["Category"] == selected_category]
	
else:
	
	df_ch1 = df
	
	
	
fig1 = px.scatter(
	
	df_ch1,
	
	x="Sales",
	
	y="Profit",
	
	color="Region",
	
	hover_data=["Category", "Sub-Category", "Discount", "Returned"],
		
	title="Sales vs. Profit by Region",
		
	labels={"Sales": "Order Sales ($)", "Profit": "Order Profit ($)", "Region": "Region"},
		
	opacity=0.7,
		
)
		
fig1.update_traces(marker=dict(size=7, line=dict(width=0.5, color='DarkSlateGrey')))
		
fig1.update_layout(legend_title_text='Region', height=450)
		
		
		
plotly(fig1)
		
		
		
text("""

_Next clue:_ Do these scatter patterns look different for each Category? Are some clusters consistently in profit, or in the red? Let's put time under the microscope..._

""")
		
		
		
# ========================================
		
# 2. CHAPTER 2: The Flow of Time — Sales and Profit Trends
		
# ========================================
		
		
		
text("## Chapter 2: The Flow of Time — Sales and Profit Trends")
		
		
		
text("""

**Clue 2:** Do profits follow sales over time, or do they tell a different tale?  

Below, see total Sales and Profit by month or year. Change the **Time Granularity** to switch between monthly or yearly view.

""")
		
		
		
granularity_options = ["Month", "Year"]
		
selected_granularity = selectbox("Time Granularity", granularity_options, default="Month")
		
		
		
df_ch2 = df.copy()
		
if selected_granularity == "Month":
		
	grp = df_ch2.groupby("Month").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
		
	x_col = "Month"
		
else:
		
	grp = df_ch2.groupby("Year").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
		
	x_col = "Year"
		
		
		
fig2 = px.line(
	
	grp,
	
	x=x_col,
	
	y=["Sales", "Profit"],
	
	labels={x_col: f"Order {selected_granularity}", "value": "Amount ($)", "variable": ""},
	
	markers=True,
	
	title="Sales and Profit Trend Over Time"
	
)
		
fig2.update_layout(legend_title_text="", height=400)
		
plotly(fig2)
		
		
		
text("""

_Do Sales spikes always mean Profits spikes? Are there periods when the lines diverge?_

Let's dig into where in the world these numbers come from...

""")
		
		
		
# ========================================
		
# 3. CHAPTER 3: Regional Suspicions
		
# ========================================
		
		
		
text("## Chapter 3: Regional Suspicions")
		
		
		
text("""

**Clue 3:** Do all regions deliver profit equally? This grouped bar chart shows total Sales and Profits per Region.

Use the **Category** filter below to see how a product category impacts a region's performance.

""")
		
		
		
selected_category_3 = selectbox("Category (filter for region)", categories, default="All")
		
		
		
if selected_category_3 != "All":
		
	df_ch3 = df[df["Category"] == selected_category_3]
		
else:
		
	df_ch3 = df
		
		
		
grp3 = df_ch3.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
		
		
		
fig3 = px.bar(
	
	grp3,
	
	x="Region",
	
	y=["Sales", "Profit"],
	
	barmode="group",
	
	labels={"value": "Total Amount ($)", "variable": "", "Region": "Region"},
	
	title="Total Sales and Profits by Region"
	
)
		
fig3.update_layout(legend_title_text="", height=400)
		
		
		
plotly(fig3)
		
		
		
text("""

_Are there regions where Sales are high but Profits low? Does filtering by Category change the suspect list?_

Now, let's break down the performance by category and sub-category...

""")
		
		
		
# ========================================
		
# 4. CHAPTER 4: Category Clues
		
# ========================================
		
		
		
text("## Chapter 4: Category Clues")
		
		
		
text("""

**Clue 4:** This stacked bar chart shows total Sales and Profits per Category, broken down by Sub-Category.

Pick a Region to see how its product makeup affects the big picture.

""")
		
		
		
regions = ["All"] + sorted([str(x) for x in df["Region"].unique() if pd.notnull(x)])
		
selected_region_4 = selectbox("Region (filter for category clues)", regions, default="All")
		
		
		
if selected_region_4 != "All":
		
	df_ch4 = df[df["Region"] == selected_region_4]
		
else:
		
	df_ch4 = df
		
		
		
grp4 = df_ch4.groupby(["Category", "Sub-Category"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
		
		
		
fig4 = px.bar(
	
	grp4,
	
	x="Category",
	
	y="Profit",
	
	color="Sub-Category",
	
	text="Sales",
	
	title=f"Profits by Category and Sub-Category{' in ' + selected_region_4 if selected_region_4 != 'All' else ''}",
	
	labels={"Profit": "Total Profit ($)", "Category": "Category", "Sub-Category": "Sub-Category"},
	
)
		
fig4.update_layout(barmode='stack', height=450, legend_title_text='Sub-Category')
		
plotly(fig4)
		
		
		
text("""

_Which Categories and Sub-Categories are dragging down profits? Examine, filter, and spot discrepancies._

That brings us to our biggest hits—and our greatest misses...

""")
		
		
		
# ========================================
		
# 5. CHAPTER 5: Top and Bottom Performers
		
# ========================================
		
		
		
text("## Chapter 5: Top and Bottom Performers")
		
		
		
text("""

**Clue 5:** Here's a horizontal bar chart of the top 8 and bottom 2 Sub-Categories by profit.

Our chart intentionally color-highlights those worst offenders (in red): are these bleeding us dry?

""")
		
		
		
# Get top 8 and bottom 2 subcategories by total profit (ensure at least 10 exist)
		
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
		
		
		
text("""

_Does your intuition match reality here? Is that high-volume sub-category actually profitable, or dragging us down?_

Next, let's check: is it the discounts killing profits?

""")
		
		
		
# ========================================
		
# 6. CHAPTER 6: The Discount Trap
		
# ========================================
		
		
		
text("## Chapter 6: The Discount Trap")
		
		
		
text("""

**Clue 6:** Are discounts a blessing or a curse?  

Here's a scatterplot: X-axis is Discount offered, Y-axis is Profit, and color denotes Category.  

**Use the slider** to adjust Discount range and see its effect.

""")
		
		
		
min_disc, max_disc = float(df["Discount"].min()), float(df["Discount"].max())
		
selected_disc_range = slider("Discount Range (%)", min_disc, max_disc, (min_disc, max_disc))
print('slider return:', selected_disc_range, type(selected_disc_range))
if isinstance(selected_disc_range, (tuple, list)) and len(selected_disc_range) == 2:
    selected_min_disc, selected_max_disc = selected_disc_range
elif isinstance(selected_disc_range, (int, float)):
    selected_min_disc = selected_max_disc = selected_disc_range
else:
    raise RuntimeError(f"Unexpected slider return value: {selected_disc_range} ({type(selected_disc_range)})")

df_ch6 = df[(df["Discount"] >= selected_min_disc) & (df["Discount"] <= selected_max_disc)]

fig6 = px.scatter(
    df_ch6,
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
		
		
		
text("""

_Are profits falling as discounts climb? Is there a point where profit vanishes?_

But maybe returns are where our profits really go to die...

""")
		
		
		
# ========================================
		
# 7. CHAPTER 7: Impact of Returns
		
# ========================================
		
		
		
text("## Chapter 7: Impact of Returns")
		
		
		
text("""

**Clue 7:** How do product returns affect profit?

This grouped bar chart splits Sales and Profits by Returned (Yes/No) per Region.

Filter by Category to see where returns hit hardest.

""")
		
		
		
selected_category_7 = selectbox("Category (filter for returns)", categories, default="All")
		
		
		
if selected_category_7 != "All":
		
	df_ch7 = df[df["Category"] == selected_category_7]
		
else:
		
	df_ch7 = df
		
		
		
grp7 = df_ch7.groupby(["Region", "Returned"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
		
		
		
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
		
		
		
text("""

_Are some regions suffering silent profit leaks from high returns? Filter and investigate!_

Let's zoom in on profit margins by region and category...

""")
		
		
		
# ========================================
		
# 8. CHAPTER 8: Profit Margin Heatmap
		
# ========================================


text("## Chapter 8: Profit Margin Heatmap")

text("""
**Clue 8:** Where is profitability melting away?  
This heatmap shows **profit margin percentage** (profit as a percentage of sales) for every Category (rows) and Region (columns).  
Darker reds indicate negative margins; greens mean good margins.
""")

# Build a pivot of Category (rows) x Region (columns) with mean Profit Margin %
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

text("""
_Where do you see a hot spot of negative margin? Any categories or regions need immediate attention?_
But are our issues recent—or a long-term trend?
""")

# ========================================
# 9. CHAPTER 9: Timeline of Trouble
# ========================================

text("## Chapter 9: Timeline of Trouble")

text("""
**Clue 9:** When did the trouble start?  
Below is an area chart of **cumulative negative profits** (i.e., losses) over time.  
This tracks how quickly and when losses have piled up.
""")

# Filter only orders with negative profit
df_loss = df[df["Profit"] < 0].sort_values("Order Date")
if not df_loss.empty:
    df_loss["Cumulative Loss"] = df_loss["Profit"].cumsum()
    # Use month granularity for x-axis
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

text("""
_Do losses cluster in a certain period, or are they a steady drip? Our final report reveals how all the evidence fits together..._
""")

# ========================================
# 10. CHAPTER 10: The Final Case File
# ========================================

text("## Chapter 10: The Final Case File")

text("""
**Final Clue:** Time for the big reveal!  
This pie chart shows how much each prime suspect—Regions, Categories, Heavy Discounts, and Returns—contributes to overall losses.  
Explore the evidence and let's close the case!
""")

# Build share of loss by each suspect:
# a) By Region (Losses only)
region_loss = df[df["Profit"] < 0].groupby("Region")["Profit"].sum().abs()
region_loss_share = region_loss / region_loss.sum() if not region_loss.empty else pd.Series()
# b) By Category
category_loss = df[df["Profit"] < 0].groupby("Category")["Profit"].sum().abs()
category_loss_share = category_loss / category_loss.sum() if not category_loss.empty else pd.Series()
# c) By Returns (lost profit among returned items)
returns_loss = df[df["Returned"].str.lower().str.startswith("y")]["Profit"].sum()
# d) By Heavy Discount (> 0.3), share among losses
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
So detective, who's the real culprit behind Superstore's vanishing profits?  
Was it a regional slump, product appetite gone bad, the sweet poison of discounts, or the slow bleed of returns?  
Whatever you decide, you've followed the data trail with true detective grit!

**Thank you for helping Magnum B.I. close the Mystery of the Vanishing Profits. Case dismissed!**
""")
