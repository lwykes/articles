# Process data and create charts

# First load the data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the SPSS file
df = pd.read_spss('exported_file.sav')

# Filter for specific countries and create visualization
selected_countries = ['United Kingdom', 'United States', 'Australia', 'India', 'Japan', 'South Korea']
df_filtered = df[df['new_label'].isin(selected_countries)].copy()

# Create panel chart
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

# Plot each market
for idx, market in enumerate(selected_countries):
    market_data = df_filtered[df_filtered['new_label'] == market]
    
    # Calculate weighted net favorable for each year
    yearly_data = []
    for year in sorted(market_data['year'].unique()):
        year_data = market_data[market_data['year'] == year]
        
        total_weight = year_data['weight'].sum()
        favorable = ((year_data['fav_china'].isin([1, 2])) * year_data['weight']).sum() / total_weight * 100
        unfavorable = ((year_data['fav_china'].isin([3, 4])) * year_data['weight']).sum() / total_weight * 100
        
        yearly_data.append({
            'year': year,
            'net_favorable': favorable - unfavorable
        })
    
    plot_data = pd.DataFrame(yearly_data)
    
    # Plot with enhanced styling
    axes[idx].plot(plot_data['year'], plot_data['net_favorable'], 
                  marker='o', linestyle='-', color='steelblue', linewidth=2)
    axes[idx].axhline(y=0, color='black', linestyle='--', alpha=0.3)
    axes[idx].grid(True, alpha=0.3)
    axes[idx].set_title(market, fontsize=12, pad=10)
    axes[idx].set_ylim(-100, 100)
    
    # Format axes
    axes[idx].set_xlabel('Year', fontsize=10)
    axes[idx].set_ylabel('Net Favorable %', fontsize=10)
    
    # Add data labels
    for x, y in zip(plot_data['year'], plot_data['net_favorable']):
        axes[idx].annotate(f'{y:.0f}%', 
                          (x, y), 
                          textcoords="offset points", 
                          xytext=(0,10), 
                          ha='center',
                          fontsize=8)

plt.suptitle('Net Favorable Trends Towards China: Key Markets', y=1.02, fontsize=14)
plt.tight_layout()
plt.show()

# Print numerical data
print("\
Net Favorable Scores Over Time (%):")
for country in selected_countries:
    print(f"\
{country}:")
    country_data = df_filtered[df_filtered['new_label'] == country]
    yearly_net = []
    for year in sorted(country_data['year'].unique()):
        year_data = country_data[country_data['year'] == year]
        total_weight = year_data['weight'].sum()
        favorable = ((year_data['fav_china'].isin([1, 2])) * year_data['weight']).sum() / total_weight * 100
        unfavorable = ((year_data['fav_china'].isin([3, 4])) * year_data['weight']).sum() / total_weight * 100
        net = favorable - unfavorable
        print(f"Year: {year:.0f}, Net Favorable: {net:.1f}%")


        # Final adjustment to improve footnote placement and spacing
plt.figure(figsize=(15, 12))

fig, axes = plt.subplots(2, 3, figsize=(15, 12))
axes = axes.flatten()

for idx, market in enumerate(selected_countries):
    market_data = df_filtered[df_filtered['new_label'] == market]
    
    yearly_data = []
    for year in sorted(market_data['year'].unique()):
        year_data = market_data[market_data['year'] == year]
        total_weight = year_data['weight'].sum()
        favorable = ((year_data['fav_china'].isin([1, 2])) * year_data['weight']).sum() / total_weight * 100
        unfavorable = ((year_data['fav_china'].isin([3, 4])) * year_data['weight']).sum() / total_weight * 100
        yearly_data.append({
            'year': int(year),
            'net_favorable': favorable - unfavorable
        })
    
    plot_data = pd.DataFrame(yearly_data)
    
    axes[idx].plot(plot_data['year'], plot_data['net_favorable'], 
                  marker='o', linestyle='-', color='steelblue', linewidth=2)
    axes[idx].axhline(y=0, color='black', linestyle='--', alpha=0.3)
    axes[idx].grid(True, alpha=0.3)
    axes[idx].set_title(market, fontsize=12, pad=10)
    axes[idx].set_ylim(-100, 100)
    axes[idx].xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    axes[idx].set_xlabel('Year', fontsize=10)
    axes[idx].set_ylabel('Net Favorable %', fontsize=10)
    
    for x, y in zip(plot_data['year'], plot_data['net_favorable']):
        axes[idx].annotate(f'{y:.0f}%', 
                          (x, y), 
                          textcoords="offset points", 
                          xytext=(0,10), 
                          ha='center',
                          fontsize=8)

# Add main title
plt.suptitle('Attitudes towards China 2006-2023\
(Net favorable - unfavorable)', y=0.95, fontsize=16)

# Add footnotes with better spacing
plt.figtext(0.1, 0.01, '1. Source: Pew Research Global Attitudes Project Spring 2006-2023 \
    2. Question: Please tell me if you have a very favorable, somewhat favorable, somewhat unfavorable, or very unfavorable opinion of China', fontsize=9, ha='left')
    
# Adjust layout
plt.tight_layout(rect=[0, 0.05, 1, 0.93])
plt.show()
