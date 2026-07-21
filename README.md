<div align="center">

# 🏝️ Pads, Palaces & Premiums

### Exploratory Data Analysis of the King County Housing Market

**The King County data that justifies your expensive taste — seriously, waterfront is worth it.**

<br>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![pandas](https://img.shields.io/badge/pandas-Data%20Wrangling-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Viz-4C72B0?style=for-the-badge)](https://seaborn.pydata.org/)
[![Folium](https://img.shields.io/badge/Folium-Geo%20Maps-77B829?style=for-the-badge)](https://python-visualization.github.io/folium/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Source-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![uv](https://img.shields.io/badge/uv-managed-DE5FE9?style=for-the-badge)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/License-MIT-1ABC9C?style=for-the-badge)](LICENSE)

<br>

<samp>21,597 sales · 22 features · 7 hypotheses · <b>2 rejected</b> · 1 very demanding client</samp>

<br>

[**Analysis Notebook**](EDA_Project.ipynb) · [**Slide Deck (PDF)**](EDA_Project_Presentation.pdf) · [**Interactive Map**](interactive_map/map_jennifer_targets.html) · [**Findings**](#-key-findings)

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [The Client Brief](#-the-client-brief)
- [Key Findings](#-key-findings)
- [Visual Highlights](#-visual-highlights)
- [Analytical Workflow](#-analytical-workflow)
- [Methodology Notes](#-methodology-notes)
- [Limitations & Honest Caveats](#-limitations--honest-caveats)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [Tech Stack](#-tech-stack)
- [Reproducing This Analysis](#-reproducing-this-analysis)
- [License](#-license)

---

## 🎯 About the Project

An end-to-end **exploratory data analysis** of 21,597 residential property sales in King County, Washington (May 2014 – May 2015), carried out as the capstone data-analysis project of a data science bootcamp.

The exercise is deliberately framed as **consulting work**, not a Kaggle leaderboard chase: a fictional client with concrete, partly conflicting requirements walks in, and the analysis has to turn a raw PostgreSQL table into a defensible shortlist of properties and a timing strategy — then present it to a non-technical audience.

**What this project demonstrates:**

| Skill | Where to see it |
|:--|:--|
| 🗄️ **SQL → DataFrame extraction** | [`Fetch_Data_to_CSV.ipynb`](Fetch_Data_to_CSV.ipynb) — `psycopg2` and `SQLAlchemy` joins across two tables |
| 🧹 **Missing-data reasoning** | Step 5–6 — hypotheses about *why* data is missing, tested before imputing |
| 📐 **Custom imputation** | [`utils/cartesian_interpolation.py`](utils/cartesian_interpolation.py) — geographic nearest-neighbour vote for `waterfront` |
| 📊 **Hypothesis-driven EDA** | Step 3 & 7 — 7 stated hypotheses, each visualised and accepted or rejected |
| 🎲 **Significance testing** | Step 8 — a NumPy permutation test that corrects for cherry-picking the most extreme of 31 buckets, used to **reject** two of my own hypotheses |
| 🔁 **Repeat-sale analysis** | Step 8 — the 176 houses that sold twice, used to test the client's resale thesis directly |
| 🗺️ **Geospatial visualisation** | Step 8–9 — zipcode aggregation, a price-by-location scatter, and a Folium map of the shortlist |
| 🎤 **Stakeholder communication** | [`EDA_Project_Presentation.pdf`](EDA_Project_Presentation.pdf) — the client-facing story |

---

## 👤 The Client Brief

> **Jennifer Montgomery** — Buyer

| Requirement | Translated into a filter |
|:--|:--|
| 💰 High budget | `price ≥ 90th percentile` ($887,000) |
| ✨ Wants to show off | `grade ≥ 10` **and** `view ≥ 3` |
| 🌊 Waterfront | `waterfront == 1` |
| 🔨 Renovated | `year_renovated > 0` |
| 🏠 Good condition | `condition ≥ 3` |
| ⏱️ Buy within a month | Day-of-month price analysis |
| 📈 Resell within a year | Month-of-year price analysis |

Applying every filter simultaneously narrows 21,597 sales down to a handful of properties — which is itself a finding worth reporting to the client: the strict brief is close to unsatisfiable in this market.

> ⚠️ **5 confirmed candidates, plus 10 more whose renovation status is unknown.** Filling
> a missing `year_renovated` with `0` asserts "never renovated" and silently disqualifies
> properties that merely lack the record. Checked against un-imputed source data, **3 of
> those 10 are genuinely renovated** — so the true count of qualifying properties is **8,
> not 5**. The notebook reports both pools. See [Limitations](#-limitations--honest-caveats).

---

## 🔍 Key Findings

<table>
<tr><th align="left">Finding</th><th align="left">Evidence</th><th align="left">Confidence</th></tr>
<tr>
<td><b>🌊 Waterfront is a separate asset class</b></td>
<td>Median <b>$1.51M</b> vs <b>$450K</b> for non-waterfront — a <b>3.4×</b> premium (<b>3.1×</b>, $1.40M, on the un-imputed source data)</td>
<td>🟢 Strong</td>
</tr>
<tr>
<td><b>🔨 Renovated homes trade at a premium</b></td>
<td><b>+35%</b> market-wide ($607K vs $449K); <b>+64%</b> inside the luxury segment ($1.66M vs $1.01M). Survives a size control: holds at <b>+23% to +34%</b> in every living-area band above 1,500 sqft</td>
<td>🟢 Strong — the only price finding that survives a confounder check</td>
</tr>
<tr>
<td><b>📏 Size and grade dominate price</b></td>
<td>Correlation with price: <code>sqft_living</code> <b>0.70</b>, <code>grade</code> <b>0.67</b>, <code>sqft_above</code> <b>0.61</b>, <code>sqft_living15</code> <b>0.59</b>, <code>bathrooms</code> <b>0.53</b></td>
<td>🟢 Strong</td>
</tr>
<tr>
<td><b>💎 Big luxury homes are cheaper per sqft</b></td>
<td>Median $/sqft: <b>$245</b> overall vs <b>$304</b> in the luxury segment, but the largest homes fall back to $107–150/sqft</td>
<td>🟢 Strong</td>
</tr>
<tr>
<td><b>📅 September shows the highest luxury prices</b></td>
<td>Median $2.13M in September (n=18) vs $1.49M in August (n=28), +43% — but the same two months differ by only <b>+1.8%</b> market-wide</td>
<td>🔴 <b>Rejected</b> — permutation p=0.44. Seasonality is real but ~2%, not 43%</td>
</tr>
<tr>
<td><b>🗓️ Day 10 shows the lowest luxury prices</b></td>
<td>Median $1.26M on the 10th — from <b>7 sales</b>. Across the whole market day 10 is the <b>28th cheapest of 31</b></td>
<td>🔴 <b>Rejected</b> — permutation p=0.74, the pattern reverses at scale</td>
</tr>
<tr>
<td><b>🔁 The one-year resale plan does not pay</b></td>
<td>Repeat sales inside the client's own segment (n=5) returned <b>+1.9% median over 176 days</b> (range −0.8% to +7.1%) — below the 6–10% round-trip transaction cost</td>
<td>🟡 Directionally clear, tiny sample</td>
</tr>
<tr>
<td><b>📍 Value follows the Lake Washington corridor</b></td>
<td>Priciest zipcodes: <b>98039 Medina</b> ($1.90M), <b>98004 Bellevue</b> ($1.15M), <b>98040 Mercer Island</b> ($0.99M). Luxury <i>volume</i> concentrates in <b>98006</b> (40 sales) and <b>98040</b> (24)</td>
<td>🟢 Strong</td>
</tr>
</table>

### 🏆 Shortlist delivered to the client

| # | House ID | Zipcode | Price | Grade | View | Renovated | Premium Score |
|:-:|:--|:--|--:|:-:|:-:|:-:|--:|
| 🥇 | `1924059029` | 98040 (Mercer Island) | $4,670,000 | 12 | 4 | 2009 | 20.65 |
| 🥈 | `3625059152` | 98008 (Bellevue) | $3,300,000 | 11 | 4 | 1987 | 5.46 |
| 🥉 | `4114601570` | 98144 (Seattle) | $3,600,000 | 10 | 4 | 2002 | 4.84 |

> ℹ️ Earlier drafts labelled these `8085`, `18185` and `2862` — those were **pandas row
> positions**, not property identifiers, and a client could not have located the houses
> from them. Scores come from the [corrected Premium Score](#the-premium-score); the
> ranking is unchanged by the fix.

*Premium Score is a custom composite ranking metric — see [Methodology Notes](#-methodology-notes) for its definition and its known weakness.*

---

## 📊 Visual Highlights

<table>
<tr>
<td width="50%"><img src="images/waterfront_price_dependence.png" alt="Waterfront price dependence"><br><sub><b>Waterfront premium</b> — median price and grade distribution</sub></td>
<td width="50%"><img src="images/renovation_price_dependence.png" alt="Renovation price dependence"><br><sub><b>Renovation uplift</b> — all properties vs luxury segment</sub></td>
</tr>
<tr>
<td width="50%"><img src="images/price_per_sqft_analysis.png" alt="Price per square foot analysis"><br><sub><b>Price vs living area</b>, coloured by construction grade</sub></td>
<td width="50%"><img src="images/best_month_to_sell_luxury_properties.png" alt="Best month to sell"><br><sub><b>Seasonality</b> — median price and volume by month, with the sample size behind each point</sub></td>
</tr>
<tr>
<td colspan="2"><img src="images/geographic_price_distribution.png" alt="Geographic price distribution"><br><sub><b>Where the value is</b> — the 15 most expensive zipcodes, and every sale placed by latitude/longitude with the shortlist starred</sub></td>
</tr>
</table>

> 🎤 **The 15-slide deck is generated, not hand-drawn** — [`build_presentation.py`](build_presentation.py)
> recomputes every figure on every slide from `data/eda.csv`, so the presentation cannot drift
> out of sync with the analysis. Rebuild it with `uv run python build_presentation.py`.

> 🗺️ **[Open the interactive Folium map](interactive_map/map_jennifer_targets.html)** — waterfront high-grade properties in blue, the top 3 recommendations in red. *(Download and open locally; GitHub does not render HTML in-browser.)*

---

## 🔄 Analytical Workflow

```mermaid
flowchart TB
    A[("🗄️ PostgreSQL · 2 tables")] -->|SQL JOIN| B["📥 Load and profile · 21,597 × 22"]
    B --> C["💡 State 7 hypotheses up front"]
    C --> D["❓ Explain every gap before filling it"]
    D --> E["🧹 Clean and impute"]
    E --> F["📈 Test each hypothesis"]
    F --> G{"🎲 Survives a<br/>permutation test?"}
    G -->|"yes · H1–H5"| H["✅ Keep as a finding"]
    G -->|"no · H6, H7"| I["❌ Report as rejected"]
    H --> J["🎯 Filter to the client's brief"]
    I --> J
    J --> K["🔁 Repeat-sale and 🗺️ geographic analysis"]
    K --> L["🏆 Shortlist · map · 15-slide deck"]

    style A fill:#4169E1,color:#fff
    style C fill:#F39C12,color:#fff
    style G fill:#8E44AD,color:#fff
    style I fill:#E74C3C,color:#fff
    style H fill:#27AE60,color:#fff
    style L fill:#1ABC9C,color:#fff
```

The gate in the middle is the part worth looking at. Two of the seven hypotheses went in as
findings and came out as rejections — see [Limitations](#-limitations--honest-caveats).

<details>
<summary><b>The 7 hypotheses tested (click to expand)</b></summary>

<br>

| # | Hypothesis | Verdict |
|:-:|:--|:--|
| **H1** | Missing `waterfront` values are concentrated among non-waterfront properties | ✅ Supported — NaN-group median price ($445K) sits within 1% of the non-waterfront median ($450K), and far from the waterfront median ($1.51M) |
| **H2** | Missing `year_renovated` values mean "never renovated" | ✅ Supported — NaN-group median price is 0.4% from the never-renovated group |
| **H3** | Waterfront access commands a large price premium | ✅ Confirmed — 3.4× |
| **H4** | Living area is the strongest single price driver | ✅ Confirmed — r = 0.70, the highest of any feature |
| **H5** | Renovated properties sell for more | ✅ Confirmed — +35% overall, +64% in luxury. The **only** hypothesis that survives a confounder check: stratified by living area the premium holds at +23% to +34% for every band above 1,500 sqft |
| **H6** | Luxury prices vary systematically with the month of sale | ❌ **Rejected.** H6 predicted a January peak; the observed peak is September, and the difference is not distinguishable from noise |
| **H7** | Higher sales volume goes with lower median prices | ❌ **Not established.** Spearman ρ = −0.49 across just 12 monthly points (p = 0.095) — too few to conclude anything either way |
| **H7b** | The day of the month predicts price | ❌ **Rejected.** The "cheapest" day rests on 7 sales; permutation p = 0.74, and market-wide that day ranks 28th of 31 |

</details>

---

## 🧪 Methodology Notes

### Missing data strategy

The dataset arrived with three columns holding gaps: `year_renovated` (3,848 / 17.8%), `waterfront` (2,391 / 11.1%) and `sqft_basement` (452 / 2.1%), plus 63 missing `view` values.

Rather than dropping or blanket-filling, each gap was **first explained, then filled**:

- **`year_renovated`** → imputed as `0` ("never renovated"). The missing group's price distribution is statistically indistinguishable from the known-zero group (0.4% median difference).
- **`waterfront`** → imputed by a custom **geographic nearest-neighbour majority vote** ([`utils/cartesian_interpolation.py`](utils/cartesian_interpolation.py)): for each property with an unknown value, all known properties within ~0.0015° (≈165 m) are collected and the majority label wins, falling back to the global mode where no neighbour exists. Result: 3 imputed as waterfront, 2,388 as non-waterfront.
- **`sqft_basement`, `view`** → left as-is; neither feeds the client filters in a way that a gap would bias.

### The Premium Score

Candidates are ranked by a custom composite — four dimensionless factors, each roughly `1.0`
for a typical property:

```python
premium_score = (sqft_living / sqft_living15)   # bigger house than its 15 neighbours
              * (sqft_lot    / sqft_lot15)      # more land than its 15 neighbours
              * (price / 1_000_000)             # independently expensive
              * (grade / 10)                    # build quality
```

The intent is "stands out from its neighbourhood **and** is independently expensive and well
built" — exclusivity, which is what the client actually asked for.

<details>
<summary><b>⚠️ The bug this replaced (click to expand — it is the most instructive thing in the repo)</b></summary>

<br>

The original third factor was `price / sqft_living / 1000`. That looks reasonable, and it is
wrong, because `sqft_living` cancels algebraically against the first factor:

```
(sqft_living / sqft_living15) × (price / sqft_living)  =  price / sqft_living15
```

The whole score therefore collapsed to
`price × sqft_lot × grade / (sqft_living15 × sqft_lot15 × 1000)` — **completely independent
of the property's own living area**, which was the entire point of factor 1. Verified by
tripling `sqft_living` on a candidate: every score came back identical.

Using absolute price instead of price-per-sqft removes the cancellation. The notebook now
carries an `assert` that fails if the bug ever returns:

```python
_probe = df_jennifer.head(1).copy()
_before = premium_score(_probe).iloc[0]
_probe['sqft_living'] *= 2
assert premium_score(_probe).iloc[0] != _before
```

The top-3 ranking is unchanged by the fix. The score remains unnormalised, so its units are
arbitrary and only the ordering carries meaning.

</details>

---

## ⚠️ Limitations & Honest Caveats

A portfolio project is more useful when it states what it does *not* prove. In order of severity:

1. **The timing findings are noise, and the whole-market data says so.** The "luxury market" pool (`price ≥ $887K & grade ≥ 10 & view ≥ 3`) is **240 sales — 1.1% of the market** — spread across 31 day-of-month buckets (n=4–14, median 8) and 12 month buckets (n=12–32). Permutation tests correcting for having picked the most extreme of 31 days / 12 months give **p=0.74** and **p=0.44**: both null. The decisive check is the whole market, where each bucket holds hundreds of sales. Day 10 — supposedly the cheapest, on **7 sales** — turns out to be the **28th cheapest of 31 days**, i.e. one of the most expensive; the pattern *reverses sign* once there is real data behind it. September's advantage shrinks from +43% to **+1.8%**. Note the nuance worth keeping: at full market size a month effect *is* statistically detectable (p<0.001) — it is simply **~2%, not 43%**, and far too small to time a purchase around. Statistical significance is not the same as a decision-relevant effect. **H6 and H7 are rejected.**
2. **The Premium Score had to be rebuilt.** In the original formulation the `sqft_living` terms cancelled algebraically, leaving the score independent of the property's own living area — the opposite of its stated intent. Verified: tripling `sqft_living` left every score identical. It is now four dimensionless factors that cannot cancel, and an `assert` in the notebook fails if the bug ever returns. The top 3 ranking is unchanged by the fix.
3. **The imputation loses three real candidates.** All five shortlisted properties do have a genuine `waterfront == 1`, so the recommendation is not built on a guess. But the `year_renovated` NaN → 0 fill disqualifies three properties whose true renovation years are known — house IDs `3343301920` (renovated 1991, $1.65M), `3761700053` (2000, $2.15M) and `3024059014` (1988, $1.9M). The correct candidate count is **8, not 5**. The top 3 are unaffected (the lost properties rank 5th, 7th and 8th), but the "only 5 properties match" headline is wrong.
4. **The waterfront imputation has 12% recall.** Its 99.3% accuracy is an artifact of a 0.7% base rate. Of 17 genuinely-waterfront properties with unknown status it recovers **2**, and one of its 3 positive calls is a false positive. It also measures distance as Euclidean on raw degrees, so at latitude 47.5° the "165 m radius" is an ellipse roughly 1.5× wider in latitude than longitude.
5. **Premium ≠ causation.** "Renovation adds 35% value" compares two groups that also differ in age, size, grade and location. The correct reading is *renovated homes sell for 35% more*. This one does partly survive scrutiny — stratified by living area the premium holds above 1,500 sqft — but it collapses to **+1.5%** for homes under 1,500 sqft.
6. **The missingness tests are weak by construction.** Comparing the NaN group's median to the `waterfront = 0` median cannot distinguish "missing among non-waterfront" from "missing completely at random", because 88% of all records are `waterfront = 0` either way. The conclusion is probably right; the test does not establish it. A χ² test on the missingness indicator against location or price decile would.
7. **Repeat sales are analysed but never deduplicated.** **176 houses sold twice** (one sold three times) inside the window — 353 rows that remain double-counted in every market-wide median and correlation. The effect is under 1%, but it is an unstated assumption in a notebook whose client thesis is about resale. Those sales are also the single most relevant signal for a client who wants to *resell within one year*, and the answer is discouraging: within Jennifer's own segment (≥$887K, grade ≥10) there are exactly 5 repeat sales, returning **+7.1%, +6.5%, +1.9%, +1.4%, −0.8%** — a median of **+1.9% over 176 days**, a loss net of 6–10% transaction costs. The tempting market-wide figure of +54% is an artifact of low-end flips (median first-sale price $261,500) where the dataset records post-renovation attributes against a distressed purchase price.
8. **"All properties resold within a year" is a truncation artifact.** The observation window is only 13 months (2014-05-02 to 2015-05-27), so the maximum observable holding period is mechanically capped at 390 days.
9. **Selection on the dependent variable.** Defining "luxury" partly by `price ≥ 90th percentile` and then analysing prices within that group truncates the distribution and biases every subsequent price statistic.
10. **Single market, single year.** King County only, one 13-month window. Nothing here generalises to another region or to a different point in the cycle.

---

## 📁 Repository Structure

```
eda_project_bootcamp/
│
├── 📓 EDA_Project.ipynb                 # ⭐ Main analysis — 9 steps, start here
│                                        #   runs clean top-to-bottom, 29 cells
├── 📓 Fetch_Data_to_CSV.ipynb           # PostgreSQL extraction → data/eda.csv
├── 📕 EDA_Project_Presentation.pdf      # Client-facing slide deck
│
├── 📂 data/                             # Dataset (git-ignored, see Getting Started)
├── 📂 images/                           # Exported figures used in the deck & README
├── 📂 interactive_map/
│   └── map_jennifer_targets.html        # Folium map of the shortlist
├── 📂 utils/
│   └── cartesian_interpolation.py       # Geographic waterfront imputation
├── 📂 useful_documentation/             # Assignment brief & EDA how-to notes
│
├── 🎨 build_presentation.py             # Regenerates the slide deck from the data
├── 💼 LINKEDIN_POST.md                  # Write-up of the findings for sharing
├── 📄 pyproject.toml                    # Dependencies (uv)
├── 📄 uv.lock                           # Pinned, reproducible resolution
└── 📄 LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

- [**uv**](https://docs.astral.sh/uv/) — handles Python itself, the virtualenv and the dependencies
- Access to the source PostgreSQL database, **or** a local copy of the King County dataset saved as `data/eda.csv`

<details>
<summary>Installing uv (click to expand)</summary>

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>

### Installation

The same three commands work identically on Linux, macOS and Windows:

```bash
git clone https://github.com/PartORG/eda_project_bootcamp.git
cd eda_project_bootcamp
uv sync
```

`uv sync` reads [`pyproject.toml`](pyproject.toml), downloads Python 3.11 if it is not already
present, creates `.venv/`, and installs the exact versions pinned in
[`uv.lock`](uv.lock) — no `pyenv`, no manual `venv`, no `pip install`, and a
reproducible resolution rather than "whatever PyPI serves today".

### Supplying the data

`data/eda.csv` is git-ignored and not distributed with this repository.

**Option A — regenerate from PostgreSQL.** Create a `.env` file in the project root and run [`Fetch_Data_to_CSV.ipynb`](Fetch_Data_to_CSV.ipynb):

```dotenv
HOST=your-db-host
PORT=5432
DATABASE=your-database
USER_DB=your-user
PASSWORD=your-password
DB_STRING=postgresql://user:password@host:5432/database
```

> 🔐 `.env` is git-ignored. Never commit credentials, and clear notebook outputs before committing — an executed cell can capture secrets in the `.ipynb` JSON.

**Option B — use a public copy.** The underlying data is the public *King County House Sales* dataset. Save it to `data/eda.csv` and rename columns to `latitude`, `longitude`, `year_built`, `year_renovated`, `house_id`.

### Run

```bash
uv run jupyter lab EDA_Project.ipynb
```

Then **Kernel → Restart & Run All** to reproduce the analysis top to bottom. The
notebook is verified to run cleanly start-to-finish on a fresh kernel.

To rebuild the slide deck from the same data:

```bash
uv run python build_presentation.py
```

> Adding a dependency later is `uv add <package>` — it updates `pyproject.toml` and
> `uv.lock` together, so the lockfile never drifts from the manifest.

---

## 🛠️ Tech Stack

<div align="center">

| | Tool | Role in this project |
|:-:|:--|:--|
| 🐍 | **Python 3.11** | Analysis language |
| 🐼 | **pandas / NumPy** | Data wrangling, aggregation, filtering |
| 📊 | **Matplotlib / Seaborn** | Correlation heatmap, box plots, bar charts, scatter plots |
| 🗺️ | **Folium** | Interactive Leaflet map of the shortlist |
| 🐘 | **PostgreSQL** | Source system (two joined tables) |
| 🔌 | **psycopg2 / SQLAlchemy** | Two demonstrated extraction paths |
| 🔑 | **python-dotenv** | Credential handling |
| 📓 | **JupyterLab** | Development environment |
| ⚡ | **uv** | Python, virtualenv and locked dependency management |

</div>

---

## 🔁 Reproducing This Analysis

Three properties this repository tries to hold, because an analysis nobody can re-run is an
assertion rather than a result:

**1 · The notebook runs clean top-to-bottom.** Execution counts are sequential `1 → 29` with
no errors. An earlier version had counts running `69, 56, 7, 57, 9, …, 100, 44` — the saved
outputs came from an out-of-order kernel and no longer matched the code that produced them.
That class of bug is invisible until someone hits *Restart & Run All*, so it is now part of
what gets checked before committing.

**2 · The deck is generated, not drawn.** [`build_presentation.py`](build_presentation.py)
recomputes every figure on all 15 slides from `data/eda.csv` at build time. A hand-edited
presentation drifts from its analysis the moment a number changes; this one cannot.

**3 · Dependencies are locked.** [`uv.lock`](uv.lock) pins the full resolution, so
`uv sync` reproduces the same environment rather than whatever PyPI happens to serve today.

```bash
uv sync                                                              # environment
uv run python -m nbconvert --to notebook --execute --inplace EDA_Project.ipynb
uv run python build_presentation.py                                  # deck
```

> ⚠️ The committed figures were generated from a faithful reconstruction of the source CSV,
> not the original bootcamp export — the two differ by roughly 15 cells in 475,000, which
> moves no conclusion but does shift a handful of counts (luxury pool 240 vs 243). If you
> have the original `data/eda.csv`, drop it in and re-run the two commands above.

---

## 📄 License

Released under the **MIT License** — see [`LICENSE`](LICENSE) for the full text.
Original template © 2021 neuefische GmbH. Analysis and code © Ievgen Perederieiev.

<div align="center">
<br>

**Built as the capstone EDA project of a data science bootcamp.**

⭐ *If you found this useful, consider starring the repository.*

</div>
