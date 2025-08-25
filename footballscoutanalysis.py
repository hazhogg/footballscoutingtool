import streamlit as st
import pandas as pd
import plotly.express as px
import re
from io import BytesIO

st.set_page_config(page_title="Football Scout", layout="wide")

# --- Source URL ---
URL = "https://www.fmscout.com/a-football-manager-2024-wonderkids.html"

# --- Helper functions ---

# Check if a scraped table looks like a wonderkids table
def is_wonderkids_table(t: pd.DataFrame) -> bool:
    needed = {"R", "Name", "Age", "Pos", "Club"}
    return needed.issubset(set(t.columns)) and len(t) > 0

# Clean up position strings (remove brackets, slashes, commas, etc.)
def tokenise_pos(s: str):
    s = str(s).upper()
    s = re.sub(r"[()/,]", " ", s)
    toks = set(s.split())
    return toks

# Decide which category (GK, DF, MF, FW) a whole table belongs to
def table_majority_category(df: pd.DataFrame) -> str:
    counts = {"Goalkeeper": 0, "Defender": 0, "Midfielder": 0, "Forward": 0}
    for p in df["Pos"].astype(str):
        toks = tokenise_pos(p)
        if "GK" in toks:
            counts["Goalkeeper"] += 1
        if {"D", "WB", "FB"}.intersection(toks):
            counts["Defender"] += 1
        if {"DM", "M", "AM", "W"}.intersection(toks):
            counts["Midfielder"] += 1
        if {"ST", "CF", "FW"}.intersection(toks):
            counts["Forward"] += 1
    # Pick the category with most hits (site order breaks ties)
    order = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
    return max(order, key=lambda k: (counts[k], -order.index(k)))

# --- Load & combine all relevant tables ---
tables = pd.read_html(URL, flavor="lxml")
dfs = []
for t in tables:
    if not is_wonderkids_table(t):
        continue
    # Keep only the useful columns
    t = t[["R", "Name", "Age", "Pos", "Club"]].dropna(subset=["R"]).copy()
    t.rename(columns={"R": "Rating"}, inplace=True)
    t["Rating"] = pd.to_numeric(t["Rating"], errors="coerce")
    # Label this table as GK/DF/MF/FW
    category = table_majority_category(t)
    t["Category"] = category
    dfs.append(t)

if not dfs:
    st.error("Could not find the wonderkids tables on the page.")
    st.stop()

# Merge all tables into one dataframe
df = pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["Name", "Club", "Pos"])

st.title("⚽ Football Scout")

# --- Sidebar filters ---
st.sidebar.header("Filters")

# Age filter (slider)
min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

# Rating filter (slider)
min_rating = int(df["Rating"].min())
max_rating = int(df["Rating"].max())
rating_filter = st.sidebar.slider("Minimum Rating", min_rating, max_rating, min_rating)

# Club filter (multi-select)
clubs = sorted(df["Club"].unique())
selected_clubs = st.sidebar.multiselect("Club", clubs)

# Search bar for player name
search_name = st.sidebar.text_input("Search Player by Name").strip().lower()

# Apply filters to dataframe
filtered = df.copy()
filtered = filtered[(filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1])]
filtered = filtered[filtered["Rating"] >= rating_filter]
if selected_clubs:
    filtered = filtered[filtered["Club"].isin(selected_clubs)]
if search_name:
    filtered = filtered[filtered["Name"].str.lower().str.contains(search_name)]

# --- Tabs per category ---
tab_gk, tab_df, tab_mf, tab_fw = st.tabs(["Goalkeepers", "Defenders", "Midfielders", "Forwards"])

# Function to render top 100 players for each category
def render_tab(cat_label, tab):
    with tab:
        sub = filtered[filtered["Category"] == cat_label].sort_values("Rating", ascending=False).head(100)
        st.subheader(f"Top {cat_label}s")
        st.dataframe(sub[["Rating", "Name", "Age", "Pos", "Club"]], use_container_width=True)
        if not sub.empty:
            # Plot bar chart of ratings
            fig = px.bar(sub, x="Name", y="Rating", color="Club",
                         title=f"Top {cat_label}s by Rating")
            st.plotly_chart(fig, use_container_width=True)

# Render each tab
render_tab("Goalkeeper", tab_gk)
render_tab("Defender", tab_df)
render_tab("Midfielder", tab_mf)
render_tab("Forward", tab_fw)

# --- Export options ---
st.sidebar.header("Export Data")

# Export filtered table as CSV
csv = filtered.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("Download CSV", csv, "wonderkids.csv", "text/csv")

# Export to Excel (in-memory, no temp file)
output = BytesIO()
filtered.to_excel(output, index=False, engine="openpyxl")
output.seek(0)
st.sidebar.download_button(
    "Download Excel",
    output,
    "wonderkids.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)