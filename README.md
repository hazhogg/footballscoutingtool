# ⚽ Football Scout

An interactive Football Manager 2024 wonderkid scouting dashboard built with Streamlit. Scrapes live data from FMScout and lets you filter, explore, and export the best young talent by position, age, rating, and club.

---

## Features

- **Live data** scraped directly from [FMScout](https://www.fmscout.com/a-football-manager-2024-wonderkids.html)
- **Tabbed by position** — Goalkeepers, Defenders, Midfielders, and Forwards
- **Top 100 per position** displayed and ranked by rating
- **Interactive bar charts** of ratings, colour-coded by club
- **Sidebar filters:**
  - Age range slider
  - Minimum rating slider
  - Multi-select club filter
  - Player name search
- **Export options** — download your filtered results as CSV or Excel

---

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

---

## Usage

Use the **sidebar** to narrow down players:

| Filter | Description |
|--------|-------------|
| **Age Range** | Slide to set a minimum and maximum age |
| **Minimum Rating** | Only show players at or above this rating |
| **Club** | Filter by one or more clubs |
| **Search by Name** | Type a partial name to find a specific player |

Switch between the **Goalkeepers**, **Defenders**, **Midfielders**, and **Forwards** tabs to browse each position group. Use the **Download CSV** or **Download Excel** buttons to export your filtered shortlist.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web app framework |
| `pandas` | Data manipulation and HTML scraping |
| `plotly` | Interactive charts |
| `lxml` | HTML table parsing |
| `openpyxl` | Excel export |

Install all dependencies:

```bash
pip install streamlit pandas plotly lxml openpyxl
```

Or use the provided requirements file:

```bash
pip install -r requirements.txt
```

### requirements.txt

```
streamlit
pandas
plotly
lxml
openpyxl
```

---

## Project Structure

```
.
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Screenshots

> Add screenshots of the dashboard here once deployed.

---

## Contributing

Pull requests are welcome! Possible additions — FM25 support, additional stat columns, player comparison view, or league/nation filters — feel free to open an issue.

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
