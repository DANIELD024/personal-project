# Railway Analysis Project

This project performs a comprehensive data analysis on railway operations using the `Railway_info.csv` dataset. The analysis is automated using a Python script (`railway_analysis.py`) which generates a detailed report and visualizations.

## Overview

The analysis covers the following key areas:

1.  **Data Exploration**: Loading data, checking structure, basic statistics, and handling missing values.
2.  **Data Transformation**: Filtering, grouping, and enriching data (e.g., adding weekday/weekend categories).
3.  **Advanced Analysis**: Analyzing weekly distribution patterns of trains.
4.  **Visualization**: Generating charts for:
    - Trains operating by day of the week (`trains_per_day.png`)
    - Top 10 source stations (`top_source_stations.png`)
    - Weekday vs. Weekend operations (`weekday_vs_weekend.png`)

## Output

Running the analysis generates:
-   **Report**: `Railway_Analysis_Report.md` (Markdown report)
-   **Visualizations**: PNG images of the charts.
-   **Data Exports**: CSV files for further analysis (e.g., `top_source_stations.csv`, `railway_info_enriched.csv`).

## Usage

Run the main script to execute the analysis:

```bash
python railway_analysis.py
```

## Dependencies

-   pandas
-   matplotlib
-   seaborn
