import pandas as pd
import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Dashboard - Oculos Masculino ",
    layout="wide",
    initial_sidebar_state="expanded",
)


conn = sqlite3.connect('../ml-scraping/data/database.db')

df = pd.read_sql_query("SELECT * FROM ml_items", conn)

conn.close()

st.title("Amazon Web Scraping - Oculos Masculino")



col1, col2,col33 = st.columns(3)



total_produtos = df.shape[0]
col1.metric("Total de Produtos", value=total_produtos, delta=0,     delta_color="off",
    border=True)

unique_brands = df['brand'].nunique()
col2.metric("Total de Marcas", value=unique_brands,   delta=0,  delta_color="off",
    border=True)

avg_price = df['price'].mean()
avg_price = "{:,.2f}".format(avg_price).replace(",", "X").replace(".", ",").replace("X", ".")
col33.metric("Average Price", value=avg_price, delta=0,     delta_color="off",    
    border=True)






c1,c2,c3,c4,c5 = st.columns([4,2,1,4,2])

c1.subheader("Marcas mais presentes")
#col1,col2 = st.columns([4,2])
top10pages_brands = df['brand'].value_counts().sort_values(ascending=False).head(10)
c1.bar_chart(top10pages_brands)
c2.write(top10pages_brands)


c4.subheader("Média por Marca")
#col1,col2 = st.columns([4,2])
df_non_zero_prices = df[df['price'] > 0]
price_by_brand = df_non_zero_prices.groupby('brand')['price'].mean().sort_values(ascending=False).head(10)
c4.bar_chart(price_by_brand)
c5.write(price_by_brand)


coll1, coll2, coll3, coll4 = st.columns([2,2,2,4])

coll1.write("### Marcas mais caras")
df_non_zero_prices = df[df['rating'] > 0]
top_brand = df_non_zero_prices.groupby('brand')['price'].max().sort_values(ascending=False).head(10)
coll1.dataframe(top_brand)#.nlargest(10, 'price'))


coll2.write("### Marcas mais barata")
df_non_zero_prices = df[df['price'] > 0]
low_brand = df_non_zero_prices.groupby('brand')['price'].min().sort_values(ascending=True).head(10)
coll2.dataframe(low_brand)

coll3.write("### Marcas mais avaliadas")
unique_brands = df.groupby('brand')['rating'].mean().reset_index()
coll3.dataframe(unique_brands.nlargest(10, 'rating'))

coll4.write("### Todos Produtos")
df_display = df.drop(columns=["title"])
df_display["Created_at"] = pd.to_datetime(df_display["Created_at"]).dt.strftime("%Y-%m-%d")
coll4.dataframe(df_display)


coll4,joker,coll5 = st.columns([6,1,6])

coll4.write("### Gráfico de Preços")
df_non_zero_prices = df[df['price'] > 0].copy()
coll4.bar_chart(df_non_zero_prices['price'].value_counts())


coll5.write("### Gráfico de Marcas")
coll5.bar_chart(df['brand'].value_counts())