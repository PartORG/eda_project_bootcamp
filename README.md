
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

## Analysis Steps

The analysis follows a structured 9-step approach documented in [EDA_Project.ipynb](EDA_Project.ipynb):

1. **Load Data** - Import dataset from CSV
2. **Understanding Data** - Initial exploration and summary statistics
3. **Hypotheses** - Formulate 7 testable hypotheses
4. **Correlation Matrix** - Identify feature relationships
5. **Working with Missing Data** - Validate imputation strategies
6. **Data Cleaning** - Apply transformations and handle missing values
7. **Hypotheses Investigation** - Test and visualize each hypothesis
8. **Client Insights** - Filter properties and generate recommendations
9. **Final Results** - Summarize findings and delivery

## Requirements

- pyenv
- python==3.11.3

## Dependencies

Key libraries used in this project:
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` & `seaborn` - Data visualization
- `folium` - Interactive maps
- Custom utility: `cartesian_interpolation` - Geographic imputation

## Setup Instructions

This repo contains a [requirements.txt](requirements.txt) file with all the packages and dependencies needed.

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

## Usage

1. **Start with the main analysis notebook**: Open [EDA_Project.ipynb](EDA_Project.ipynb) in Jupyter Lab/Notebook
2. **Run all cells** to reproduce the analysis
3. **View generated outputs**:
   - Statistical summaries and insights in the notebook
   - Visualizations saved to the `images/` folder
   - Interactive map: [map_jennifer_targets.html](map_jennifer_targets.html)

## Hypotheses Tested

1. **H1 - Missing Waterfront Data**: Missing waterfront values represent non-waterfront properties (✅ VALIDATED)
2. **H2 - Missing Year Renovated**: Missing renovation data means "never renovated" (✅ VALIDATED)
3. **H3 - Waterfront Price Premium**: Waterfront properties have significantly higher prices (✅ VALIDATED)
4. **H4 - Living Area & Price**: Non-linear relationship between size and price (✅ VALIDATED)
5. **H5 - Renovation Effect**: Renovated properties sell for more (✅ VALIDATED)
6. **H6 - Luxury Price Seasonality**: Luxury segment shows seasonal pricing patterns (✅ VALIDATED)
7. **H7 - Sales Volume & Price**: Inverse relationship between volume and prices (✅ VALIDATED)

## Key Visualizations

The project generates several executive dashboards:
- **Waterfront Price Dependence** - Shows waterfront premium and grade distribution
- **Renovation Price Impact** - Compares renovated vs non-renovated properties
- **Price per Square Foot Analysis** - Identifies value opportunities in luxury segment
- **Best Day to Buy** - Optimal timing for luxury purchases
- **Best Month to Sell** - Seasonal pricing patterns for resale strategy

## Dataset

**Source**: King County Housing Data (2014-2015)
**Size**: 21,597 property records
**Features**: 22 columns including price, location, size, condition, grade, waterfront status, etc.

### Key Features:
- `price` - Sale price (target variable)
- `grade` - Overall grade based on King County grading system (1-13)
- `waterfront` - Property has waterfront view
- `sqft_living` - Interior living space square footage
- `year_renovated` - Year of renovation (0 if never renovated)
- `view` - Quality of view (0-4)
- `condition` - Overall condition (1-5)

## Results & Insights

### Investment Strategy for Jennifer Montgomery:
1. **Timing**: Buy on the 10th day of July or August, sell in September
2. **Expected Return**: September sales command ~40% premium over August prices
3. **Property Focus**: Zipcodes 98040 and 98008 dominate luxury waterfront market
4. **Value Opportunity**: Larger luxury homes often have better price per square foot

Only 5 properties (0.02% of dataset) match ALL strict criteria, highlighting the exclusivity of the luxury waterfront market.

## License

This project is part of MIT Licence.
 
