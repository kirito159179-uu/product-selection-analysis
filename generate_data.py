# -*- coding: utf-8 -*-
"""
跨境电商商品数据生成器（模拟数据，贴近真实）。

目标：生成一份"商品表"给选品分析用，字段包括品类、价格、评分、
评论数、月销量——正是跨境电商选品时最关心的几个指标。

为什么先用模拟数据：
1. 今天就能完整跑通，不被网络 / 账号 / 下载卡住；
2. 顺便练习 pandas 创建 DataFrame（最基础的一步）。
将来可以无缝换成真实数据（如 Olist 公开数据集），分析代码基本不用改。
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent          # 项目根目录
np.random.seed(42)                              # 固定随机种子 → 结果可复现
N = 300                                         # 生成 300 个商品

# 每个品类：价格中位数（美元）、销售热度、以及拼商品名的词
CATEGORIES = {
    "Electronics":    {"price_med": 120, "hot": 1.2, "words": ["Bluetooth Speaker", "Wireless Mouse", "USB-C Hub", "LED Monitor", "Mechanical Keyboard", "Webcam"]},
    "Home & Kitchen": {"price_med": 45,  "hot": 1.0, "words": ["Coffee Maker", "Air Fryer", "Vacuum Cleaner", "Knife Set", "Storage Box", "Blender"]},
    "Beauty":         {"price_med": 25,  "hot": 0.9, "words": ["Face Cream", "Hair Dryer", "Lipstick Set", "Serum", "Sunscreen", "Eye Mask"]},
    "Sports":         {"price_med": 35,  "hot": 0.7, "words": ["Yoga Mat", "Dumbbell Set", "Running Shoes", "Resistance Band", "Water Bottle", "Jump Rope"]},
    "Toys":           {"price_med": 20,  "hot": 0.8, "words": ["Building Blocks", "Remote Car", "Puzzle Set", "Plush Toy", "Board Game", "Drone"]},
    "Pet Supplies":   {"price_med": 18,  "hot": 0.6, "words": ["Cat Litter Box", "Dog Leash", "Pet Food Bowl", "Scratching Post", "Pet Bed", "Toy Ball"]},
}

rows = []
for cat, cfg in CATEGORIES.items():
    n = N // len(CATEGORIES)                     # 每个品类数量大致相同
    # 价格：对数正态分布（右偏，更贴近真实：便宜的商品比贵的多）
    price = np.random.lognormal(mean=np.log(cfg["price_med"]), sigma=0.5, size=n)
    price = np.round(price, 2)

    rating = 3.6 + np.random.normal(0, 0.35, size=n)       # 基础评分
    sweet = (price >= 20) & (price <= 60)                  # 价格甜点区 $20~$60
    rating[sweet] += 0.35                                  # 甜点区评分更高
    rating = np.clip(rating, 1.0, 5.0).round(1)            # 限制在 1~5，保留 1 位小数

    sales = (np.random.lognormal(mean=6, sigma=0.8, size=n) * cfg["hot"]).astype(int)
    reviews = (sales * np.random.uniform(0.05, 0.15, size=n)).astype(int)

    for i in range(n):
        name = f"{np.random.choice(cfg['words'])} #{len(rows)+1:03d}"
        rows.append({
            "product_id": f"{len(rows)+1:04d}",
            "name": name,
            "category": cat,
            "price_usd": price[i],
            "rating": rating[i],
            "review_count": reviews[i],
            "monthly_sales": sales[i],
        })

df = pd.DataFrame(rows)
df.to_csv(BASE / "data" / "products.csv", index=False)
print(f"已生成 {len(df)} 条商品数据 → data/products.csv")
print(df.head())
