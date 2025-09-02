# 1. Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Load dataset
df = pd.read_csv("your_data.csv")   # or generate fake data

# 3. Explore data (quick checks)
print(df.head())
print(df.info())
print(df.describe())

# 4. Clean data
df.dropna(inplace=True)                     # drop missing values
df['date'] = pd.to_datetime(df['date'])     # convert to datetime if needed

# 5. Analyze (answer quick questions)
top_product = df['product'].value_counts().head(1)
print("Most sold product:\n", top_product)

daily_sales = df.groupby(df['date'].dt.date)['price'].sum()
print("Daily sales:\n", daily_sales.head())

avg_order = (df['price'] * df['quantity']).mean()
print("Average order value:", avg_order)

# 6. Visualize results
plt.figure(figsize=(8,4))
daily_sales.plot(kind="line", title="Daily Sales Over Time")
plt.show()

sns.barplot(x="product", y="quantity", data=df)
plt.title("Top Selling Products")
plt.xticks(rotation=45)
plt.show()

# 7. Wrap up
print("✅ Quick analysis done!")


