import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
import subprocess
import sys

PASTA_DADOS = Path(__file__).parent / "archive"

orders = pd.read_csv(
    PASTA_DADOS / "olist_orders_dataset.csv"
)

customers = pd.read_csv(
    PASTA_DADOS / "olist_customers_dataset.csv"
)

products = pd.read_csv(
    PASTA_DADOS / "olist_products_dataset.csv"
)

items = pd.read_csv(
    PASTA_DADOS / "olist_order_items_dataset.csv"
)

payments = pd.read_csv(
    PASTA_DADOS / "olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    PASTA_DADOS / "olist_order_reviews_dataset.csv"
)

sellers = pd.read_csv(
    PASTA_DADOS / "olist_sellers_dataset.csv"
)
#APENAS PARA VISUALIZAÇAO

print("="*90)
# print(f"arquivo:{orders.Name}, {orders.head()}")
print("="*90)
print(customers.head().columns)
print("="*90)
print(products.head().columns)
print("="*90)
print(items.head().columns)
print("="*90)
print(payments.head().columns)
print("="*90)
print(reviews.head().columns)
print(reviews.head().shape)

print("="*90)
print(sellers.head().columns)

# print("="*90)

# # print("="*90)
# print(orders.head().columns)
# # print("="*90)
# # print(customers.info())
# # print("="*90)
# # print(products.info())
# print("="*90)
# # print(items.info())
# # print("="*90)
# print(payments.head(20).columns)
# print("="*90)
# print(reviews.head(20).columns)
# # print("="*90)
# # print(sellers.info())

