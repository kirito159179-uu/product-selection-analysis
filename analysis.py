# -*- coding: utf-8 -*-
"""
跨境电商选品分析：从 data/products.csv 里找"值得卖"的机会点。

回答三个选品核心问题：
1. 哪个品类的销量最好？（市场热度）
2. 什么价位是"甜点区"？（高评分 + 高销量的价格带）
3. 哪个品类是"被低估的机会"？（评分高但销量/竞争相对低）

图表文字全部用英文，方便放进英文作品集。
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")                            # 不弹窗，直接把图存成文件
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent           # 项目根目录
CHARTS = BASE / "charts"
CHARTS.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "data" / "products.csv")
print(f"共 {len(df)} 个商品，{df['category'].nunique()} 个品类\n")

# 1. 各品类月销量合计
sales_by_cat = df.groupby("category")["monthly_sales"].sum().sort_values()
sales_by_cat.plot(kind="barh", color="steelblue")
plt.title("Total Monthly Sales by Category")
plt.xlabel("Monthly Sales")
plt.tight_layout()
plt.savefig(CHARTS / "sales_by_category.png", dpi=120)
plt.close()

# 2. 价格分布
df["price_usd"].hist(bins=30, color="orange", edgecolor="white")
plt.title("Price Distribution of Products")
plt.xlabel("Price (USD)")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig(CHARTS / "price_distribution.png", dpi=120)
plt.close()

# 3. 价格 vs 评分（标出甜点区）
plt.scatter(df["price_usd"], df["rating"], alpha=0.5, s=20)
plt.axvspan(20, 60, color="green", alpha=0.15)   # 甜点区 $20~$60
plt.title("Price vs. Rating")
plt.xlabel("Price (USD)")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig(CHARTS / "price_vs_rating.png", dpi=120)
plt.close()

# 4. 各品类平均评分
rating_by_cat = df.groupby("category")["rating"].mean().sort_values()
rating_by_cat.plot(kind="barh", color="seagreen")
plt.title("Average Rating by Category")
plt.xlabel("Average Rating")
plt.tight_layout()
plt.savefig(CHARTS / "rating_by_category.png", dpi=120)
plt.close()

# 打印关键结论
print("各品类月销量合计：")
print(sales_by_cat.to_string(), "\n")

print("各品类平均评分：")
print(rating_by_cat.round(2).to_string(), "\n")

sweet = df[(df["price_usd"] >= 20) & (df["price_usd"] <= 60)]
outside = df[(df["price_usd"] < 20) | (df["price_usd"] > 60)]
print(f"甜点区 $20~$60：{len(sweet)} 个商品，平均评分 {sweet['rating'].mean():.2f}")
print(f"甜点区之外：{len(outside)} 个商品，平均评分 {outside['rating'].mean():.2f}\n")

print("图表已保存到 charts/ 目录")
