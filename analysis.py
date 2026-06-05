import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# ── LOAD DATA INTO SQLite ──
df = pd.read_csv('sales.csv')
conn = sqlite3.connect('sales.db')
df.to_sql('sales', conn, if_exists='replace', index=False)
print("✅ Data loaded into database!")
print(f"Total orders: {len(df)}")
print()

# ── SQL QUERIES ──
print("📊 SALES ANALYSIS RESULTS")
print("="*45)

# Query 1 — Total revenue
q1 = pd.read_sql_query("SELECT SUM(TotalAmount) as TotalRevenue FROM sales", conn)
print(f"💰 Total Revenue: ₹{q1['TotalRevenue'][0]:,.0f}")

# Query 2 — Revenue by category
q2 = pd.read_sql_query("""
    SELECT Category, 
           SUM(TotalAmount) as Revenue,
           COUNT(*) as Orders
    FROM sales 
    GROUP BY Category 
    ORDER BY Revenue DESC
""", conn)
print("\n📦 Revenue by Category:")
for _, row in q2.iterrows():
    print(f"  {row['Category']}: ₹{row['Revenue']:,.0f} ({row['Orders']} orders)")

# Query 3 — Revenue by region
q3 = pd.read_sql_query("""
    SELECT Region,
           SUM(TotalAmount) as Revenue,
           COUNT(*) as Orders
    FROM sales
    GROUP BY Region
    ORDER BY Revenue DESC
""", conn)
print("\n🗺️ Revenue by Region:")
for _, row in q3.iterrows():
    print(f"  {row['Region']}: ₹{row['Revenue']:,.0f} ({row['Orders']} orders)")

# Query 4 — Top 5 products
q4 = pd.read_sql_query("""
    SELECT Product,
           SUM(TotalAmount) as Revenue,
           SUM(Quantity) as UnitsSold
    FROM sales
    GROUP BY Product
    ORDER BY Revenue DESC
    LIMIT 5
""", conn)
print("\n🏆 Top 5 Products by Revenue:")
for _, row in q4.iterrows():
    print(f"  {row['Product']}: ₹{row['Revenue']:,.0f} ({row['UnitsSold']} units)")

# Query 5 — Monthly revenue
q5 = pd.read_sql_query("""
    SELECT strftime('%Y-%m', Date) as Month,
           SUM(TotalAmount) as Revenue,
           COUNT(*) as Orders
    FROM sales
    GROUP BY Month
    ORDER BY Month
""", conn)
print("\n📅 Monthly Revenue:")
for _, row in q5.iterrows():
    print(f"  {row['Month']}: ₹{row['Revenue']:,.0f}")

# ── CHARTS ──
os.makedirs('charts', exist_ok=True)
plt.style.use('seaborn-v0_8-darkgrid')

# Chart 1 — Revenue by Category
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#4e79a7', '#f28e2b']
bars = ax.bar(q2['Category'], q2['Revenue'], color=colors, width=0.4)
ax.set_title('Revenue by Category', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Revenue (₹)', fontsize=12)
for bar, val in zip(bars, q2['Revenue']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
            f'₹{val:,.0f}', ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/revenue_by_category.png', dpi=150)
plt.close()
print("\n✅ Chart 1 saved: revenue_by_category.png")

# Chart 2 — Revenue by Region
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#59a14f','#e15759','#76b7b2','#f28e2b']
bars = ax.bar(q3['Region'], q3['Revenue'], color=colors, width=0.4)
ax.set_title('Revenue by Region', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Revenue (₹)', fontsize=12)
for bar, val in zip(bars, q3['Revenue']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
            f'₹{val:,.0f}', ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/revenue_by_region.png', dpi=150)
plt.close()
print("✅ Chart 2 saved: revenue_by_region.png")

# Chart 3 — Monthly Revenue trend
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(q5['Month'], q5['Revenue'], marker='o', linewidth=2.5,
        color='#4e79a7', markersize=8, markerfacecolor='#f28e2b')
ax.fill_between(range(len(q5)), q5['Revenue'], alpha=0.15, color='#4e79a7')
ax.set_xticks(range(len(q5)))
ax.set_xticklabels(q5['Month'], rotation=45)
ax.set_title('Monthly Revenue Trend', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Revenue (₹)', fontsize=12)
for i, val in enumerate(q5['Revenue']):
    ax.text(i, val + 2000, f'₹{val:,.0f}', ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/monthly_revenue.png', dpi=150)
plt.close()
print("✅ Chart 3 saved: monthly_revenue.png")

# Chart 4 — Top products
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#4e79a7','#f28e2b','#59a14f','#e15759','#76b7b2']
bars = ax.barh(q4['Product'], q4['Revenue'], color=colors)
ax.set_title('Top 5 Products by Revenue', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Revenue (₹)', fontsize=12)
for bar, val in zip(bars, q4['Revenue']):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'₹{val:,.0f}', va='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/top_products.png', dpi=150)
plt.close()
print("✅ Chart 4 saved: top_products.png")

conn.close()
print("\n🎉 Sales analysis complete!")