# King County Housing Market - Exploratory Data Analysis Project

An in-depth exploratory data analysis of the King County housing dataset, focused on luxury real estate investment strategies and market insights for high-end property buyers.

## Project Overview

This project analyzes the King County housing market dataset (21,597 properties) to provide data-driven insights for a luxury property buyer. The analysis includes:

- **Data Cleaning & Imputation**: Handling missing values in critical features (waterfront, year_renovated)
- **Hypothesis Testing**: Validating 7 hypotheses about price drivers and market timing
- **Market Insights**: Identifying optimal buying/selling strategies
- **Property Recommendations**: Finding properties matching specific luxury criteria

### Key Findings

- **Waterfront Premium**: Waterfront properties command a median price of $1.51M vs $450K for non-waterfront (3.4x premium)
- **Renovation Impact**: Renovated properties sell for 35% more than non-renovated homes
- **Optimal Timing**: Best day to buy luxury properties is the 10th of the month; best month to sell is September
- **Top Price Drivers**: Living area (0.70 correlation), grade (0.67), and sqft_above (0.61) show strongest price correlations

### Client Profile: Jennifer Montgomery

**Requirements:**
- High budget luxury buyer
- Waterfront property required
- Recently renovated
- High grade (≥10)
- Excellent view (≥3)
- Plans to resell within 1 year

**Top 3 Recommendations:**
1. **ID 8085** - Zipcode 98040, $4.67M, Grade 12, Premium Score: 21.42
2. **ID 18185** - Zipcode 98008, $3.30M, Grade 11, Premium Score: 12.94
3. **ID 2862** - Zipcode 98144, $3.60M, Grade 10, Premium Score: 9.64

## Project Structure

```
eda_project_bootcamp/
├── EDA_Project.ipynb           # Main analysis notebook with all steps
├── Fetch_Data_to_CSV.ipynb     # Data extraction from PostgreSQL
├── data/
│   └── eda.csv                 # King County housing dataset
├── images/                     # Generated visualizations
├── utils/
│   └── cartesian_interpolation.py  # Custom imputation function
├── useful_documentation/       # Project requirements and guides
├── map_jennifer_targets.html   # Interactive map of recommended properties
└── requirements.txt            # Python dependencies
```

## Features

### Data Cleaning & Imputation
- **Handling Missing Values**: The project includes a custom utility `cartesian_interpolation.py` to handle missing values in critical features like waterfront and year_renovated.

### Hypothesis Testing
- **7 Testable Hypotheses**: The analysis validates 7 hypotheses about price drivers and market timing, providing actionable insights for luxury property buyers.

### Market Insights
- **Optimal Timing**: Identifies the best day to buy and sell luxury properties based on historical data.
- **Top Price Drivers**: Highlights features that have the strongest correlation with property prices, such as living area, grade, and sqft_above.

### Property Recommendations
- **Custom Recommendations**: Generates tailored property recommendations for high-end buyers based on specific criteria like waterfront, renovation status, grade, and view quality.

## How It Works

The project follows a structured 9-step approach:

1. **Load Data** - Import dataset from CSV.
2. **Understanding Data** - Initial exploration and summary statistics.
3. **Hypotheses** - Formulate 7 testable hypotheses.
4. **Correlation Matrix** - Identify feature relationships.
5. **Working with Missing Data** - Validate imputation strategies.
6. **Data Cleaning** - Apply transformations and handle missing values.
7. **Hypotheses Investigation** - Test and visualize each hypothesis.
8. **Client Insights** - Filter properties and generate recommendations.
9. **Final Results** - Summarize findings and deliver insights.

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Jupyter Notebook | Main analysis environment |
| Python 3.11.3 | Programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| Matplotlib & Seaborn | Data visualization |
| Folium | Interactive maps |
| Altair | Statistical visualizations |
| SQLAlchemy | Database interaction |
| psycopg2-binary | PostgreSQL database adapter |
| ipywidgets | Interactive widgets for Jupyter notebooks |
| jupyterlab-dash | Integration of Dash apps in JupyterLab |
| python-dotenv | Loading environment variables |

## Requirements

- **Python 3.11.3**: Ensure you have the correct Python version installed.
- **pyenv**: For managing multiple Python versions.

## Installation

### macOS Setup

```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows Setup (PowerShell)

```powershell
pyenv local 3.11.3
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows Setup (Git-Bash)

```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

No specific configuration files are required for this project.

## Quick Start

To get started, clone the repository and run the main analysis notebook:

```bash
git clone https://github.com/PartORG/eda_project_bootcamp.git
cd eda_project_bootcamp
jupyter lab EDA_Project.ipynb
```

## Usage

Run the Jupyter Notebook `EDA_Project.ipynb` to execute the analysis. The notebook includes detailed steps and visualizations.

## Project Structure

- **EDA_Project.ipynb**: Main analysis notebook.
- **Fetch_Data_to_CSV.ipynb**: Script for fetching data from PostgreSQL.
- **data/eda.csv**: King County housing dataset.
- **images/**: Directory containing generated visualizations.
- **utils/cartesian_interpolation.py**: Custom utility for handling missing values.
- **useful_documentation/**: Project requirements and guides.
- **map_jennifer_targets.html**: Interactive map of recommended properties.

## Development

The project is open-source, and contributions are welcome. Follow the guidelines in [CONTRIBUTING.md](https://github.com/PartORG/eda_project_bootcamp/blob/main/CONTRIBUTING.md).

## Testing

No tests are included in this project.

## Limitations

- **Data Source**: The analysis relies on a single dataset, which may not be representative of the entire housing market.
- **Hypothesis Validation**: Hypotheses are based on historical data and may not hold true for future trends.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.