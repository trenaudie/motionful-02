#%% Comprehensive Plotly Analysis of Obesity Data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np

# Set default template for better-looking plots
pio.templates.default = "plotly_white"

#%% Load and prepare data
df = pd.read_csv('NCD_RisC_Lancet_2024_BMI_age_standardised_country.csv')
obesity_column = 'Prevalence of BMI>=30 kg/m² (obesity)'
index_columns = ['Year','Country/Region/World', 'Sex']

# Clean the data
df_clean = df[index_columns + [obesity_column]].dropna()
df_clean = df_clean.rename(columns={'Country/Region/World': 'Country'})

print(f"Dataset shape: {df_clean.shape}")
print(f"Year range: {df_clean['Year'].min()} - {df_clean['Year'].max()}")
print(f"Number of countries: {df_clean['Country'].nunique()}")
print(f"Sex categories: {df_clean['Sex'].unique()}")

#%% 1. Global Obesity Trends Over Time
def plot_global_trends():
    """Plot global obesity trends by sex over time"""
    global_data = df_clean[df_clean['Country'] == 'World']
    
    fig = px.line(global_data, 
                  x='Year', 
                  y=obesity_column,
                  color='Sex',
                  title='Global Obesity Prevalence Trends (1990-2022)',
                  labels={obesity_column: 'Obesity Prevalence (%)'})
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig

global_fig = plot_global_trends()
global_fig.show()

#%% 2. Top 20 Countries with Highest Obesity Rates (Latest Year)
def plot_top_countries():
    """Plot top 20 countries with highest obesity rates"""
    latest_year = df_clean['Year'].max()
    latest_data = df_clean[df_clean['Year'] == latest_year]
    
    # Get top 20 countries by average obesity rate across sexes
    country_avg = latest_data.groupby('Country')[obesity_column].mean().sort_values(ascending=False).head(20)
    top_countries = country_avg.index.tolist()
    
    # Filter data for top countries
    top_data = latest_data[latest_data['Country'].isin(top_countries)]
    
    fig = px.bar(top_data, 
                 x='Country', 
                 y=obesity_column,
                 color='Sex',
                 title=f'Top 20 Countries by Obesity Prevalence ({latest_year})',
                 labels={obesity_column: 'Obesity Prevalence (%)'},
                 barmode='group')
    
    fig.update_layout(
        height=600,
        xaxis_tickangle=-45,
        showlegend=True
    )
    
    return fig, top_countries

top_fig, top_countries = plot_top_countries()
top_fig.show()

#%% 3. Heatmap of Obesity Trends by Region/Country
def plot_heatmap():
    """Create heatmap showing obesity trends across countries"""
    # Select a subset of countries for readability
    selected_countries = df_clean['Country'].value_counts().head(30).index.tolist()
    if 'World' in selected_countries:
        selected_countries.remove('World')
    
    heatmap_data = df_clean[df_clean['Country'].isin(selected_countries)]
    
    # Create pivot table for heatmap
    pivot_data = heatmap_data.pivot_table(
        values=obesity_column, 
        index='Country', 
        columns='Year', 
        aggfunc='mean'
    )
    
    fig = px.imshow(pivot_data, 
                    aspect='auto',
                    title='Obesity Prevalence Heatmap Across Countries and Years',
                    labels=dict(x="Year", y="Country", color="Obesity Prevalence (%)"))
    
    fig.update_layout(height=800)
    
    return fig

heatmap_fig = plot_heatmap()
heatmap_fig.show()

#%% 4. Gender Gap Analysis
def plot_gender_gap():
    """Analyze and visualize gender gaps in obesity"""
    # Calculate gender gap (Female - Male obesity rates)
    pivot_gender = df_clean.pivot_table(
        values=obesity_column,
        index=['Country', 'Year'],
        columns='Sex',
        aggfunc='first'
    ).reset_index()
    
    # Calculate gender gap
    pivot_gender['Gender_Gap'] = pivot_gender['Women'] - pivot_gender['Men']
    
    # Global gender gap over time
    global_gap = pivot_gender[pivot_gender['Country'] == 'World']
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Global Gender Gap in Obesity Over Time', 
                       'Gender Gap Distribution by Country (Latest Year)'],
        vertical_spacing=0.1
    )
    
    # Global trend
    fig.add_trace(
        go.Scatter(x=global_gap['Year'], 
                  y=global_gap['Gender_Gap'],
                  mode='lines+markers',
                  name='Global Gender Gap',
                  line=dict(color='purple', width=3)),
        row=1, col=1
    )
    
    # Distribution by country (latest year)
    latest_year = df_clean['Year'].max()
    latest_gap = pivot_gender[pivot_gender['Year'] == latest_year]
    
    fig.add_trace(
        go.Histogram(x=latest_gap['Gender_Gap'],
                    nbinsx=30,
                    name=f'Countries ({latest_year})',
                    marker_color='lightblue'),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_yaxes(title_text="Gender Gap (% points)", row=1, col=1)
    fig.update_xaxes(title_text="Gender Gap (% points)", row=2, col=1)
    fig.update_yaxes(title_text="Number of Countries", row=2, col=1)
    
    fig.update_layout(height=800, title_text="Gender Gap Analysis in Obesity")
    
    return fig, pivot_gender

gender_fig, gender_data = plot_gender_gap()
gender_fig.show()

#%% 5. Time Series Analysis for Selected Countries
def plot_country_comparison():
    """Compare obesity trends for selected high-impact countries"""
    # Select diverse countries for comparison
    comparison_countries = ['United States of America', 'China', 'India', 'Brazil', 
                          'United Kingdom', 'Germany', 'Japan', 'Mexico']
    
    # Filter available countries
    available_countries = [c for c in comparison_countries if c in df_clean['Country'].values]
    
    comparison_data = df_clean[df_clean['Country'].isin(available_countries)]
    
    fig = px.line(comparison_data,
                  x='Year',
                  y=obesity_column,
                  color='Country',
                  facet_col='Sex',
                  title='Obesity Trends Comparison: Selected Countries',
                  labels={obesity_column: 'Obesity Prevalence (%)'})
    
    fig.update_layout(height=500)
    
    return fig

comparison_fig = plot_country_comparison()
comparison_fig.show()

#%% 6. Statistical Summary and Insights
def generate_insights():
    """Generate key insights from the data"""
    latest_year = df_clean['Year'].max()
    earliest_year = df_clean['Year'].min()
    
    # Global statistics
    global_latest = df_clean[(df_clean['Country'] == 'World') & (df_clean['Year'] == latest_year)]
    global_earliest = df_clean[(df_clean['Country'] == 'World') & (df_clean['Year'] == earliest_year)]
    
    insights = {
        'time_span': f"{earliest_year} - {latest_year}",
        'total_countries': df_clean['Country'].nunique(),
        'global_obesity_latest': global_latest[obesity_column].mean(),
        'global_obesity_earliest': global_earliest[obesity_column].mean(),
        'global_change': global_latest[obesity_column].mean() - global_earliest[obesity_column].mean()
    }
    
    # Top 5 countries with highest rates
    latest_data = df_clean[df_clean['Year'] == latest_year]
    top_5 = latest_data.groupby('Country')[obesity_column].mean().sort_values(ascending=False).head(5)
    
    # Countries with fastest growth
    country_growth = []
    for country in df_clean['Country'].unique():
        if country != 'World':
            country_data = df_clean[df_clean['Country'] == country]
            if len(country_data) > 1:
                earliest = country_data[country_data['Year'] == country_data['Year'].min()][obesity_column].mean()
                latest = country_data[country_data['Year'] == country_data['Year'].max()][obesity_column].mean()
                growth = latest - earliest
                country_growth.append((country, growth))
    
    fastest_growth = sorted(country_growth, key=lambda x: x[1], reverse=True)[:5]
    
    print("=== OBESITY DATA INSIGHTS ===")
    print(f"Data spans: {insights['time_span']}")
    print(f"Countries analyzed: {insights['total_countries']}")
    print(f"Global obesity rate ({latest_year}): {insights['global_obesity_latest']:.1f}%")
    print(f"Global obesity rate ({earliest_year}): {insights['global_obesity_earliest']:.1f}%")
    print(f"Global change: +{insights['global_change']:.1f} percentage points")
    print()
    print("Top 5 countries with highest obesity rates:")
    for i, (country, rate) in enumerate(top_5.items(), 1):
        print(f"{i}. {country}: {rate:.1f}%")
    print()
    print("Top 5 countries with fastest obesity growth:")
    for i, (country, growth) in enumerate(fastest_growth, 1):
        print(f"{i}. {country}: +{growth:.1f} percentage points")
    
    return insights

insights = generate_insights()

#%% 7. Interactive Dashboard Summary
def create_summary_dashboard():
    """Create a comprehensive summary dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Global Trends by Sex', 'Top 10 Countries (Latest Year)',
                       'Obesity Growth Rate by Country', 'Gender Gap Over Time'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Global trends
    global_data = df_clean[df_clean['Country'] == 'World']
    for sex in global_data['Sex'].unique():
        sex_data = global_data[global_data['Sex'] == sex]
        fig.add_trace(
            go.Scatter(x=sex_data['Year'], y=sex_data[obesity_column],
                      mode='lines+markers', name=f'Global {sex}'),
            row=1, col=1
        )
    
    # Top countries
    latest_year = df_clean['Year'].max()
    latest_data = df_clean[df_clean['Year'] == latest_year]
    top_10 = latest_data.groupby('Country')[obesity_column].mean().sort_values(ascending=False).head(10)
    
    fig.add_trace(
        go.Bar(x=list(range(len(top_10))), y=top_10.values,
               text=top_10.index, textposition='outside',
               name='Top 10 Countries'),
        row=1, col=2
    )
    
    # Growth rates
    country_growth = {}
    for country in df_clean['Country'].unique()[:20]:  # Limit for readability
        if country != 'World':
            country_data = df_clean[df_clean['Country'] == country]
            if len(country_data) > 1:
                earliest = country_data[country_data['Year'] == country_data['Year'].min()][obesity_column].mean()
                latest = country_data[country_data['Year'] == country_data['Year'].max()][obesity_column].mean()
                country_growth[country] = latest - earliest
    
    growth_sorted = dict(sorted(country_growth.items(), key=lambda x: x[1], reverse=True)[:10])
    fig.add_trace(
        go.Bar(x=list(range(len(growth_sorted))), y=list(growth_sorted.values()),
               text=list(growth_sorted.keys()), textposition='outside',
               name='Growth Rate'),
        row=2, col=1
    )
    
    # Gender gap
    pivot_gender = df_clean.pivot_table(
        values=obesity_column,
        index=['Country', 'Year'],
        columns='Sex',
        aggfunc='first'
    ).reset_index()
    pivot_gender['Gender_Gap'] = pivot_gender['Women'] - pivot_gender['Men']
    global_gap = pivot_gender[pivot_gender['Country'] == 'World']
    
    fig.add_trace(
        go.Scatter(x=global_gap['Year'], y=global_gap['Gender_Gap'],
                  mode='lines+markers', name='Gender Gap'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, title_text="Comprehensive Obesity Analysis Dashboard")
    
    return fig

dashboard_fig = create_summary_dashboard()
dashboard_fig.show()

#%% 8. USA vs France vs Italy vs Japan Comparison
def plot_country_specific_comparison():
    """Compare obesity trends for USA, France, Italy, and Japan (Men only)"""
    target_countries = ['United States of America', 'France', 'Italy', 'Japan']
    
    # Filter data for these countries and men only
    comparison_data = df_clean[
        (df_clean['Country'].isin(target_countries)) & 
        (df_clean['Sex'] == 'Men')
    ]
    
    fig = px.line(comparison_data,
                  x='Year',
                  y=obesity_column,
                  color='Country',
                  title='Obesity Trends: USA vs France vs Italy vs Japan (Men)',
                  labels={obesity_column: 'Obesity Prevalence (%)'},
                  markers=True)
    
    fig.update_layout(
        height=500,
        hovermode='x unified'
    )
    
    # Update line styles for better distinction
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    for i, trace in enumerate(fig.data):
        trace.line.width = 3
    
    return fig, comparison_data

country_comparison_fig, comparison_data = plot_country_specific_comparison()
country_comparison_fig.show()

#%% 9. Canvas-adapted comparison data table
def create_canvas_table():
    """Create a canvas-adapted table with Year and country columns"""
    target_countries = ['United States of America', 'France', 'Italy', 'Japan']
    
    # Filter data for these countries and men only
    filtered_data = df_clean[
        (df_clean['Country'].isin(target_countries)) & 
        (df_clean['Sex'] == 'Men')
    ]
    
    # Pivot the data to have countries as columns
    canvas_table = filtered_data.pivot_table(
        values=obesity_column,
        index='Year',
        columns='Country',
        aggfunc='first'
    ).reset_index()
    
    # Round values to 2 decimal places for cleaner display
    for col in canvas_table.columns:
        if col != 'Year':
            canvas_table[col] = canvas_table[col].round(2)
    
    return canvas_table

canvas_data = create_canvas_table()
print("\n=== CANVAS-ADAPTED DATA TABLE ===")
print(canvas_data.to_string(index=False))

# Optional: Save to CSV for easy import into Canvas
canvas_data.to_csv('obesity_comparison_canvas.csv', index=False)
print("\nData saved to 'obesity_comparison_canvas.csv'")

print("\n=== ANALYSIS COMPLETE ===")
print("All visualizations have been generated successfully!")
print("The analysis includes:")
print("1. Global obesity trends over time")
print("2. Top countries with highest obesity rates")
print("3. Heatmap visualization across countries and years")
print("4. Gender gap analysis")
print("5. Country comparison time series")
print("6. Statistical insights and summary")
print("7. Interactive comprehensive dashboard")
print("8. USA vs France vs Italy vs Japan comparison (Men)")
print("9. Canvas-adapted data table")
# %%
