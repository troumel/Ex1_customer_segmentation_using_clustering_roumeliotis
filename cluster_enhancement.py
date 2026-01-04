cluster_names = {
    1: "Premium VIP",
    4: "High-Value Regulars",
    2: "Young Enthusiasts",
    0: "Average Customers",
    5: "Budget Conscious",
    3: "Conservative Wealthy"
}

df['Cluster_Name'] = df['Cluster'].map(cluster_names)

cluster_details = df.groupby('Cluster').agg({
    'Annual Income (k$)': 'mean',
    'Spending Score (1-100)': 'mean',
    'CustomerID': 'count'
}).rename(columns={'CustomerID': 'Count'}).round(2)

cluster_details['Cluster_Name'] = cluster_details.index.map(cluster_names)
cluster_details['Percentage'] = (cluster_details['Count'] / len(df) * 100).round(1)

cluster_details = cluster_details[['Cluster_Name', 'Count', 'Percentage', 'Annual Income (k$)', 'Spending Score (1-100)']]
cluster_details = cluster_details.sort_values('Spending Score (1-100)', ascending=False)

print("Detailed Cluster Analysis:")
print(cluster_details)
print("\n" + "="*70)
print("MARKETING REPORT")
print("="*70)

for cluster_id in cluster_details.index:
    name = cluster_names[cluster_id]
    count = cluster_details.loc[cluster_id, 'Count']
    pct = cluster_details.loc[cluster_id, 'Percentage']
    income = cluster_details.loc[cluster_id, 'Annual Income (k$)']
    spending = cluster_details.loc[cluster_id, 'Spending Score (1-100)']

    print(f"\nCluster {cluster_id}: {name}")
    print(f"  Size: {count} customers ({pct}% of total)")
    print(f"  Average Income: ${income}k")
    print(f"  Average Spending Score: {spending}/100")

    if spending > 70:
        priority = "HIGH"
        action = "Premium campaigns, VIP programs, exclusive offers"
    elif spending > 40:
        priority = "MEDIUM"
        action = "Standard marketing, seasonal promotions"
    else:
        priority = "LOW"
        action = "Minimal investment, clearance sales only"

    print(f"  Priority: {priority}")
    print(f"  Recommended Action: {action}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
high_value_count = cluster_details[cluster_details['Spending Score (1-100)'] > 70]['Count'].sum()
high_value_pct = (high_value_count / len(df) * 100).round(1)
print(f"High-value customers (spending > 70): {high_value_count} ({high_value_pct}%)")
print(f"Primary target: Cluster 4 (High-Value Regulars) - largest high-spending segment")
print(f"Secondary targets: Clusters 1 and 2 for specialized campaigns")
