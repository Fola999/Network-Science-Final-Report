import pandas as pd
import networkx as nx
from datetime import datetime
import os

# Load cleaned data WITH dates
df = pd.read_csv('us_conflict_data_CLEAN_with_dates.csv')

print(f"📊 Processing {len(df)} conflict events\n")

# Create output directories
os.makedirs('monthly_networks', exist_ok=True)
os.makedirs('conflict_type_networks', exist_ok=True)

# ============================================================================
# PART 1: SEPARATE BY MONTH
# ============================================================================
print("="*60)
print("📅 CREATING MONTHLY NETWORKS")
print("="*60)

# Check if SQLDATE column exists
if 'SQLDATE' in df.columns:
    # Convert SQLDATE (format: YYYYMMDD) to datetime
    df['Date'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d', errors='coerce')
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    # Group by month
    monthly_summary = []
    for month, month_df in df.groupby('YearMonth'):
        if len(month_df) == 0:
            continue
            
        month_str = str(month)  # Format: 2023-01
        
        # Count conflicts per partner
        partner_counts = month_df['Partner'].value_counts().to_dict()
        
        # Create network
        G = nx.Graph()
        G.add_node('USA', label='USA', size=1000, conflicts=sum(partner_counts.values()))
        
        for country, count in partner_counts.items():
            G.add_node(country, label=country, size=count * 2, conflicts=count)
            G.add_edge('USA', country, weight=count)
        
        # Save
        filename = f'monthly_networks/us_conflicts_{month_str}.gexf'
        nx.write_gexf(G, filename)
        
        # Track for summary
        top_country = max(partner_counts.items(), key=lambda x: x[1])
        monthly_summary.append({
            'month': month_str,
            'events': len(month_df),
            'countries': len(partner_counts),
            'top_partner': f"{top_country[0]} ({top_country[1]})"
        })
        
        print(f"✅ {month_str}: {len(month_df):4d} events, {len(partner_counts):3d} countries, top: {top_country[0]} ({top_country[1]})")
    
    print(f"\n💾 {len(monthly_summary)} monthly networks saved to 'monthly_networks/' folder")
    
    # Monthly summary table
    summary_df = pd.DataFrame(monthly_summary)
    summary_df.to_csv('monthly_summary.csv', index=False)
    print(f"📋 Monthly summary saved to monthly_summary.csv")
    
else:
    print("❌ No SQLDATE column found!")
    print("   Make sure you ran clean_with_dates.py first")
    exit()

# ============================================================================
# PART 2: SEPARATE BY CONFLICT TYPE (QuadClass 3 vs 4)
# ============================================================================
print("\n" + "="*60)
print("⚔️ CREATING CONFLICT TYPE NETWORKS")
print("="*60)

# Verbal Conflicts (QuadClass 3)
df_verbal = df[df['QuadClass'] == '3'].copy()
verbal_counts = df_verbal['Partner'].value_counts().to_dict()

G_verbal = nx.Graph()
G_verbal.add_node('USA', label='USA', size=1000, conflicts=sum(verbal_counts.values()))

for country, count in verbal_counts.items():
    G_verbal.add_node(country, label=country, size=count * 2, conflicts=count)
    G_verbal.add_edge('USA', country, weight=count)

verbal_file = 'conflict_type_networks/us_conflicts_VERBAL.gexf'
nx.write_gexf(G_verbal, verbal_file)
print(f"✅ Verbal Conflicts (QuadClass 3): {len(df_verbal)} events, {len(verbal_counts)} countries")
print(f"   Top 5: {dict(list(verbal_counts.items())[:5])}")
print(f"   Saved to: {verbal_file}")

# Material Conflicts (QuadClass 4)
df_material = df[df['QuadClass'] == '4'].copy()
material_counts = df_material['Partner'].value_counts().to_dict()

G_material = nx.Graph()
G_material.add_node('USA', label='USA', size=1000, conflicts=sum(material_counts.values()))

for country, count in material_counts.items():
    G_material.add_node(country, label=country, size=count * 2, conflicts=count)
    G_material.add_edge('USA', country, weight=count)

material_file = 'conflict_type_networks/us_conflicts_MATERIAL.gexf'
nx.write_gexf(G_material, material_file)
print(f"\n✅ Material Conflicts (QuadClass 4): {len(df_material)} events, {len(material_counts)} countries")
print(f"   Top 5: {dict(list(material_counts.items())[:5])}")
print(f"   Saved to: {material_file}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("📊 FINAL SUMMARY")
print("="*60)
print(f"Total events: {len(df)}")
print(f"Date range: {df['SQLDATE'].min()} to {df['SQLDATE'].max()}")
print(f"Unique countries: {df['Partner'].nunique()}")
print(f"Verbal conflicts: {len(df_verbal)} ({100*len(df_verbal)/len(df):.1f}%)")
print(f"Material conflicts: {len(df_material)} ({100*len(df_material)/len(df):.1f}%)")
print(f"\n📁 Files created:")
print(f"   - {len(monthly_summary)} monthly networks in: monthly_networks/")
print(f"   - Verbal network: {verbal_file}")
print(f"   - Material network: {material_file}")
print(f"   - Monthly summary table: monthly_summary.csv")
print("\n✅ Import any .gexf file into Gephi to visualize!")
