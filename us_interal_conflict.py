import pandas as pd
import matplotlib.pyplot as plt

# Load filtered data (with headers)
df = pd.read_csv('filtered_data.csv')  # SQLDATE,Partner,QuadClass
df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d')  # Convert YYYYMMDD

# Filter USA vs USA ONLY (internal)
usa_internal_verbal = df[(df['Partner'] == 'USA') & (df['QuadClass'] == 3)]   # Verbal
usa_internal_material = df[(df['Partner'] == 'USA') & (df['QuadClass'] == 4)] # Material

# Monthly trends
usa_internal_verbal['Month'] = usa_internal_verbal['SQLDATE'].dt.to_period('M').astype(str)
usa_internal_material['Month'] = usa_internal_material['SQLDATE'].dt.to_period('M').astype(str)

monthly_verbal = usa_internal_verbal.groupby('Month').size()
monthly_material = usa_internal_material.groupby('Month').size()

# Summary table
summary = pd.DataFrame({
    'USA vs USA Verbal (3)': [len(usa_internal_verbal), monthly_verbal.sum()],
    'USA vs USA Material (4)': [len(usa_internal_material), monthly_material.sum()]
}, index=['Total Events', '2026 Events']).round(0)

print("USA vs USA Internal Conflicts (QuadClass 3 vs 4)")
print(summary)

# Chart: Monthly comparison
fig, ax = plt.subplots(figsize=(12, 6))
months = sorted(set(monthly_verbal.index) | set(monthly_material.index))
x = range(len(months))

ax.bar([i - 0.2 for i in x], monthly_verbal.reindex(months, fill_value=0), 0.4, 
       label='Verbal (3)', color='blue', alpha=0.7)
ax.bar([i + 0.2 for i in x], monthly_material.reindex(months, fill_value=0), 0.4, 
       label='Material (4)', color='red', alpha=0.7)

ax.set_xticks(x)
ax.set_xticklabels(months, rotation=45)
ax.set_ylabel('Events')
ax.set_title('USA Internal Conflicts: Verbal vs Material (2026)')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('usa_internal_verbal_vs_material.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Chart saved: usa_internal_verbal_vs_material.png")