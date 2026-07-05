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

### Exploratory Data Analysis (EDA)
- **Data Cleaning & Imputation**: Handles missing values in critical features.
- **Hypothesis Testing**: Validates 7 hypotheses about price drivers and market timing.
- **Market Insights**: Identifies optimal buying/selling strategies.
- **Property Recommendations**: Finds properties matching specific luxury criteria.

### Visualization
- **Interactive Maps**: Uses Folium to create interactive maps of recommended properties.
- **Correlation Matrix**: Visualizes relationships between features using Seaborn.

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
9. **Final Results** - Summarize findings and delivery.

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Jupyter Notebook | Primary development environment for data analysis and visualization. |
| Python | Programming language used for data manipulation, analysis, and visualization. |
| Pandas | Data manipulation and analysis library. |
| NumPy | Numerical computing library. |
| Matplotlib & Seaborn | Data visualization libraries. |
| Folium | Interactive maps library. |
| Altair | Declarative statistical visualization library. |
| SQLAlchemy | SQL toolkit and Object-Relational Mapping (ORM) library. |
| psycopg2-binary | PostgreSQL database adapter for Python. |
| ipywidgets | Interactive widgets for Jupyter Notebook. |
| jupyterlab-dash | Integration of Dash with JupyterLab. |
| python-dotenv | Loads environment variables from a `.env` file. |

## Requirements

- pyenv
- python==3.11.3

## Installation

### macOS Setup

1. Set Python version and create virtual environment:
   ```bash
   pyenv local 3.11.3
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Windows Setup

For **PowerShell**:
```powershell
pyenv local 3.11.3
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For **Git-Bash**:
```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

No specific configuration files or environment variables are required.

## Quick Start

To run the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/PartORG/eda_project_bootcamp.git
   cd eda_project_bootcamp
   ```

2. Set up the virtual environment and install dependencies:
   ```bash
   pyenv local 3.11.3
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Run the Jupyter Notebook:
   ```bash
   jupyter lab EDA_Project.ipynb
   ```

## Usage

To use this project, open the `EDA_Project.ipynb` notebook in JupyterLab and follow the steps outlined in the analysis.

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

## Development

The project is primarily developed using Jupyter Notebook. Dependencies are managed via `requirements.txt`.

## Testing

No tests exist for this project.

## Limitations

- The analysis assumes the dataset is complete and accurate.
- The project does not include real-time data updates.

## License

MIT License

Copyright (c) 2021 neuefische GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.