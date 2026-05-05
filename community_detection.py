import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data
df = pd.read_csv('filtered_data.csv')
df['QuadClass'] = df['QuadClass'].astype(str).str.strip()
print(f"📊 Analyzing {len(df)} US conflict events from 2026\n")

# Define global regions by country codes
regions = {
    'Middle East': ['IRN','IRQ','ISR','SAU','YEM','SYR','LBN','JOR','ARE','QAT','KWT','BHR','OMN','PSE','TUR'],
    'Africa': ['NGA','ZAF','EGY','ETH','KEN','SOM','SDN','DZA','MAR','LBY','GHA','CAF','COD','COG','TZA'],
    'Asia-Pacific': ['CHN','RUS','IND','PAK','KOR','JPN','AUS','NZL','THA','VNM','IDN','MYS','SGP','PHL','TWN'],
    'Europe': ['GBR','FRA','DEU','DNK','IRL','ESP','ITA','NLD','BEL','SWE','NOR','CHE','AUT','POL','UKR'],
    'Latin America': ['VEN','CUB','NIC','MEX','COL','BRA','ARG','CHL','PER','BOL','ECU','GTM','HND','SLV','DOM'],
    'USA Internal': ['USA']
}

# Assign each country to a region
df['Region'] = 'Other'
for region, countries in regions.items():
    mask = df['Partner'].isin(countries)
    df.loc[mask, 'Region'] = region

# Count conflicts by region
region_stats = df.groupby(['Region', 'QuadClass']).size().unstack(fill_value=0)
region_stats['Total'] = region_stats.sum(axis=1)
region_stats = region_stats.sort_values('Total', ascending=True)

print("🌍 US Conflicts by Region:")
print(region_stats.round(0))

# Create bar chart
fig, ax = plt.subplots(figsize=(14, 8))
regions_list = region_stats.index[::-1]  # Largest on top
totals = region_stats['Total'][::-1]

bars = ax.barh(regions_list, totals, color='steelblue', alpha=0.8)
ax.set_xlabel('Total Conflict Events')
ax.set_title('US Conflicts by Global Region (2026)', fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add count labels on bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 50, bar.get_y() + bar.get_height()/2, 
            f'{int(width)}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('us_conflicts_by_region.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Bar chart saved: us_conflicts_by_region.png")
print(f"📈 Top region: {region_stats['Total'].idxmax()} ({region_stats['Total'].max()} events)")