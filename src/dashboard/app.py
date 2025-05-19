import pandas as pd
import streamlit as st
import sqlite3

conn = sqlite3.connect('../ml-scraping/data/database.db')

df = pd.read_sql_query("SELECT * FROM ml_items", conn)

conn.close()

st.title("Dashboard - Amazon Web Scraping")



col1, col2,col33 = st.columns(3)

total_produtos = df.shape[0]
col1.metric("Total de Produtos", value=total_produtos)

unique_brands = df['brand'].nunique()
col2.metric("Total de Marcas", value=unique_brands)

avg_price = df['price'].mean()
avg_price = "{:,.2f}".format(avg_price).replace(",", "X").replace(".", ",").replace("X", ".")
col33.metric("Average Price", value=avg_price)







st.write("### Marcas mais caras")
df_non_zero_prices = df[df['rating'] > 0]
top_brand = df_non_zero_prices.groupby('brand')['price'].max().sort_values(ascending=False).head(10)
st.dataframe(top_brand)#.nlargest(10, 'price'))


st.write("### Produtos mais baratos")
df_non_zero_prices = df[df['price'] > 0]
low_brand = df_non_zero_prices.groupby('brand')['price'].min().sort_values(ascending=True).head(10)
st.dataframe(low_brand)

st.write("### top 10 produtos mais avaliados")
unique_brands = df.groupby('brand')['rating'].mean().reset_index()
st.dataframe(unique_brands.nlargest(10, 'rating'))


st.subheader("Top 10 Marcas")
col1,col2 = st.columns([4,2])
top10pages_brands = df['brand'].value_counts().sort_values(ascending=False).head(10)
col1.bar_chart(top10pages_brands)
col2.write(top10pages_brands)


st.subheader("Avg price by Brand")
col1,col2 = st.columns([4,2])
df_non_zero_prices = df[df['price'] > 0]
price_by_brand = df_non_zero_prices.groupby('brand')['price'].mean().sort_values(ascending=False).head(10)
col1.bar_chart(price_by_brand)
col2.write(price_by_brand)


st.write("### Tabela de Produtos")
st.dataframe(df)


st.write("### Gráfico de Preços")
df_non_zero_prices = df[df['price'] > 0].copy()
st.bar_chart(df_non_zero_prices['price'].value_counts())


st.write("### Gráfico de Marcas")
st.bar_chart(df['brand'].value_counts())