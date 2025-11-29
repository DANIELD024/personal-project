import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set plot style
sns.set_theme(style="whitegrid")

def main():
    print("Starting Railway Data Analysis...")
    report_content = "# Railway Analysis Report\n\n"

    # --- Level 1: Data Exploration and Basic Operations ---
    print("\n--- Level 1: Data Exploration ---")
    
    # Task 1.1: Load and Inspect Data
    try:
        df = pd.read_csv('Railway_info.csv')
        print("Dataset loaded successfully.")
    except FileNotFoundError:
        print("Error: Railway_info.csv not found.")
        return

    report_content += "## Level 1: Data Exploration\n\n"
    report_content += "### Task 1.1: Data Structure\n"
    report_content += f"- **Shape**: {df.shape}\n"
    report_content += f"- **Columns**: {', '.join(df.columns)}\n"
    report_content += "#### First 5 Rows\n"
    report_content += df.head().to_markdown(index=False) + "\n\n"

    # Task 1.2: Basic Statistics
    num_trains = df['Train_No'].nunique()
    unique_source = df['Source_Station_Name'].nunique()
    unique_dest = df['Destination_Station_Name'].nunique()
    
    most_common_source = df['Source_Station_Name'].mode()[0]
    most_common_dest = df['Destination_Station_Name'].mode()[0]

    report_content += "### Task 1.2: Basic Statistics\n"
    report_content += f"- **Total Trains**: {num_trains}\n"
    report_content += f"- **Unique Source Stations**: {unique_source}\n"
    report_content += f"- **Unique Destination Stations**: {unique_dest}\n"
    report_content += f"- **Most Common Source**: {most_common_source}\n"
    report_content += f"- **Most Common Destination**: {most_common_dest}\n\n"

    # Task 1.3: Data Cleaning
    # Check for missing values
    missing_values = df.isnull().sum()
    report_content += "### Task 1.3: Data Cleaning\n"
    report_content += "#### Missing Values:\n"
    report_content += missing_values.to_markdown() + "\n\n"
    
    # Standardize station names (uppercase)
    df['Source_Station_Name'] = df['Source_Station_Name'].str.upper()
    df['Destination_Station_Name'] = df['Destination_Station_Name'].str.upper()
    report_content += "- Station names have been standardized to uppercase.\n\n"

    # --- Level 2: Data Transformation and Aggregation ---
    print("\n--- Level 2: Data Transformation ---")
    report_content += "## Level 2: Data Transformation\n\n"

    # Task 2.1: Data Filtering
    # Filter for trains on Saturdays
    saturday_trains = df[df['days'] == 'Saturday']
    report_content += "### Task 2.1: Filtering\n"
    report_content += f"- **Trains operating on Saturday**: {len(saturday_trains)}\n"

    # Task 2.2: Grouping and Aggregation
    source_counts = df.groupby('Source_Station_Name')['Train_No'].count().reset_index()
    source_counts.columns = ['Source_Station_Name', 'Train_Count']
    top_sources = source_counts.sort_values(by='Train_Count', ascending=False).head(10)
    
    report_content += "### Task 2.2: Top 10 Source Stations by Train Count\n"
    report_content += top_sources.to_markdown(index=False) + "\n\n"

    # Average number of trains per day for each source station
    # First, count trains per source and day
    source_day_counts = df.groupby(['Source_Station_Name', 'days'])['Train_No'].count().reset_index()
    # Then average these counts per source
    avg_trains_per_source = source_day_counts.groupby('Source_Station_Name')['Train_No'].mean().reset_index()
    avg_trains_per_source.columns = ['Source_Station_Name', 'Avg_Trains_Per_Day']
    
    report_content += "#### Average Trains per Day (Top 5 Sources)\n"
    report_content += avg_trains_per_source.sort_values(by='Avg_Trains_Per_Day', ascending=False).head(5).to_markdown(index=False) + "\n\n"

    # Task 2.3: Data Enrichment
    weekend_days = ['Saturday', 'Sunday']
    df['Day_Category'] = df['days'].apply(lambda x: 'Weekend' if x in weekend_days else 'Weekday')
    
    report_content += "### Task 2.3: Data Enrichment\n"
    report_content += "- Added `Day_Category` column (Weekday/Weekend).\n"
    report_content += df['Day_Category'].value_counts().to_markdown() + "\n\n"

    # --- Level 3: Advanced Data Analysis ---
    print("\n--- Level 3: Advanced Analysis ---")
    report_content += "## Level 3: Advanced Analysis\n\n"

    # Task 3.1: Pattern Analysis (Weekly Distribution)
    day_counts = df['days'].value_counts()
    # Order days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = day_counts.reindex(days_order)
    
    report_content += "### Task 3.1: Weekly Distribution\n"
    report_content += day_counts.to_markdown() + "\n\n"

    # --- Level 4: Visualization and Reporting ---
    print("\n--- Level 4: Visualization ---")
    report_content += "## Level 4: Visualizations\n\n"

    # Task 4.1: Visualization
    # 1. Bar chart of trains per day
    plt.figure(figsize=(10, 6))
    sns.barplot(x=day_counts.index, y=day_counts.values, palette="viridis")
    plt.title('Number of Trains Operating by Day of Week')
    plt.xlabel('Day')
    plt.ylabel('Number of Trains')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('trains_per_day.png')
    plt.close()
    report_content += "![Trains per Day](trains_per_day.png)\n\n"

    # 2. Top 10 Source Stations
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_sources, x='Train_Count', y='Source_Station_Name', palette="magma")
    plt.title('Top 10 Source Stations')
    plt.xlabel('Number of Trains')
    plt.ylabel('Station Name')
    plt.tight_layout()
    plt.savefig('top_source_stations.png')
    plt.close()
    report_content += "![Top Source Stations](top_source_stations.png)\n\n"
    
    # 3. Weekday vs Weekend
    plt.figure(figsize=(6, 6))
    df['Day_Category'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
    plt.title('Weekday vs Weekend Train Operations')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('weekday_vs_weekend.png')
    plt.close()
    report_content += "![Weekday vs Weekend](weekday_vs_weekend.png)\n\n"

    # Save Report
    with open('Railway_Analysis_Report.md', 'w') as f:
        f.write(report_content)
    
    # --- Export to CSV ---
    print("\n--- Exporting Results to CSV ---")
    
    # 1. Top 10 Source Stations
    top_sources.to_csv('top_source_stations.csv', index=False)
    print("Saved top_source_stations.csv")
    
    # 2. Average Trains per Day
    avg_trains_per_source.to_csv('avg_trains_per_source.csv', index=False)
    print("Saved avg_trains_per_source.csv")
    
    # 3. Weekly Distribution
    day_counts.to_csv('weekly_train_counts.csv', header=['Train_Count'])
    print("Saved weekly_train_counts.csv")
    
    # 4. Weekday vs Weekend Counts
    df['Day_Category'].value_counts().to_csv('day_category_counts.csv', header=['Count'])
    print("Saved day_category_counts.csv")

    # 5. Enriched Full Dataset
    df.to_csv('railway_info_enriched.csv', index=False)
    print("Saved railway_info_enriched.csv")

    print("Analysis complete. Report saved to Railway_Analysis_Report.md and CSVs generated.")

if __name__ == "__main__":
    main()
