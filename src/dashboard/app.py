import pandas as pd
import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Dashboard - Oculos Masculino ",
    layout="wide",
    initial_sidebar_state="expanded",
)


conn = sqlite3.connect('../ml-scraping/data/amazon.db')

df = pd.read_sql_query("SELECT * FROM ml_items", conn)

conn.close()



st.title("Amazon Web Scraping - Oculos Masculino")



col1, col2,col33 = st.columns(3)

total_produtos = df.shape[0]
col1.metric("Total de Produtos", value=total_produtos, border=True)

unique_brands = df['brand'].nunique()
col2.metric("Total de Marcas", value=unique_brands,  border=True)

avg_price = df['price'].mean()
avg_price = "{:,.2f}".format(avg_price).replace(",", "X").replace(".", ",").replace("X", ".")
col33.metric("Average Price", value=avg_price, border=True)


with st.expander("See more"):
    colm1, colm2,colm33 = st.columns(3)

    #top_brand = df_non_zero_prices.groupby('brand')['price'].max().sort_values(ascending=False).head(10)

    highest_brand = df['brand'].value_counts().idxmax()
    colm1.metric("Highest Frequency Brand", value=highest_brand, border=True)

    most_rated_brand = df.groupby('brand')['rating'].mean().idxmax()
    colm2.metric("Most Rating", value=most_rated_brand, border=True)

    if df['brand'].notnull().any():
        max_price = df[df['brand'].notnull()]['price'].max().round(0).astype(int)
        colm33.metric("Highest Price", value=max_price, border=True)
    
    st.write('''
        The total number of products is the total number of rows in the dataset.
        The total number of brands is the number of unique values in the brand column.
        The average price is the mean of the price column.
        The average price is formatted to two decimal places and uses a comma as the decimal separator.
             The top brand is the brand with the highest frequency in the dataset.
    ''')



st.divider()  # 👈 Draws a horizontal rule

column1, joker,column2 = st.columns([3.5,0.3,4.5])



#coll1, coll2, coll3, coll4, coll5 = st.columns([4,2,1,4,2]) 
with column1:
    tab1, tab2, tab3 = st.tabs(["🗃 Min","📈 Max"," Mean"])
    with tab2:
        col1, col2 = st.columns([4,2])
        with col1:
            st.write("### Marcas mais caras")
            df_non_zero_prices = df[df['rating'] > 0]
            
        with col2:
            price_range = st.slider("Prices", min_value=101, max_value=2050, value=(500, 2050)) 
            min_price, max_price = price_range
            df_filtered = df_non_zero_prices[(df_non_zero_prices["price"] >= min_price) & (df_non_zero_prices["price"] <= max_price)] # Filter based on selected price range
            top_brand = df_filtered.groupby('brand')['price'].max().sort_values(ascending=False).head(10) # Group by brand and show the max price for each brand
            st.dataframe(top_brand)
        col1.bar_chart(top_brand, height= 400)



    with tab1:
        col1, col2 = st.columns([4,2])
        with col1:
            st.write("### Marcas mais baratas")
            df_non_zero_prices = df[df['price'] > 0]
        with col2: 
            low_brand = df_non_zero_prices.groupby('brand')['price'].min().sort_values(ascending=True)
            price_range = st.slider("Prices", 10, 100, (13, 50)) # Use the slider to filter the minimum prices
            low_brand_filtered = low_brand[(low_brand >= price_range[0]) & (low_brand <= price_range[1])].head(10)
            st.dataframe(low_brand_filtered)
        col1.bar_chart(low_brand_filtered, height= 400)
        




    with tab3:
        col1, col2 = st.columns([4,2])
        with col1:
            st.subheader("Média por Marca")
            df_non_zero_prices = df[df['price'] > 0]
            price_by_brand = df_non_zero_prices.groupby('brand')['price'].mean().round(2).sort_values(ascending=False).head(10)
            st.bar_chart(price_by_brand, height= 400)
        with col2:
            #price_range = st.slider("Prices", 10, 100, (13, 50)) # Use the slider to filter the average prices
            st.write(price_by_brand)




with column2:
    col1, col2 = st.columns([4,2])
    with col1:
        st.subheader("Marcas mais presentes")
        # Calculate brand counts and get top 10
        counts = df['brand'].value_counts()
        top10pages_brands = counts.sort_values(ascending=False).head(80)
    
    with col2:
        # Create a slider to filter by count range based on the min and max counts in top10pages_brands
        filter_range = st.slider(
            "Filter by count",
            min_value=int(top10pages_brands.min()),
            max_value=int(top10pages_brands.max()),
            value=(int(top10pages_brands.min()), int(top10pages_brands.max()))
        )
# Calculate total count of non-null brands
        total_count = df['brand'].notnull().sum()
        
        # Create a DataFrame with brand, count, and percentage
        filtered_brands_df = top10pages_brands[
            (top10pages_brands >= filter_range[0]) & 
            (top10pages_brands <= filter_range[1])
        ].reset_index()
        
        # Rename columns
        filtered_brands_df.columns = ['brand', 'count']
        
        # Calculate percentage
        filtered_brands_df['percentage'] = (filtered_brands_df['count'] / total_count * 100).round(2).astype(str) + '%'

    col1, col2 = st.columns([4,2])
    col1.bar_chart(filtered_brands_df.set_index('brand')['count'], height=450)
    col2.dataframe(filtered_brands_df, height=450, hide_index=True)




# c4.subheader("Média por Marca")
# df_non_zero_prices = df[df['price'] > 0]
# price_by_brand = df_non_zero_prices.groupby('brand')['price'].mean().sort_values(ascending=False).head(10)
# c4.bar_chart(price_by_brand)
# c5.write(price_by_brand)

st.divider() 



cc1, joker, cc2 = st.columns([1.3,0.3,5])

cc1.write("### Marcas mais avaliadas")
unique_brands = df.groupby('brand')['rating'].mean().reset_index()
unique_brands['rating'] = unique_brands['rating'].round(0).astype(int)
cc1.dataframe(unique_brands.nlargest(10, 'rating'), use_container_width=True, hide_index=True)

# coll4.write("### Todos Produtos")
# df_display = df.copy()
# df_display["Created_at"] = pd.to_datetime(df_display["Created_at"]).dt.strftime("%Y-%m-%d")
# coll4.dataframe(df_display)

cc2.write("### Todos Produtos")
df_display = df[df['price'] > 0]
df_display = df_display[df_display['brand'].notnull()]
df_display["Created_at"] = pd.to_datetime(df_display["Created_at"]).dt.strftime("%Y-%m-%d")
df_display = df_display.sort_values(by='Created_at', ascending=True)
df_display = df_display[['Created_at','brand', 'price', 'rating', 'title', 'Source']]
df_display['price'] = df_display['price'].fillna(0).astype(int)
df_display['rating'] = df_display['rating'].fillna(0).astype(int)
#cc2.dataframe(df_display.style.hide(axis='index'))
#cc2.write(df_display.style.hide(axis='index').to_html(index=False), unsafe_allow_html=True)
cc2.dataframe(df_display, use_container_width=True, hide_index=True)


# st.divider()  

# coll4,joker,coll5 = st.columns([6,1,6])

# coll4.write("### Gráfico de Preços")
# df_non_zero_prices = df[df['price'] > 0].copy()
# coll4.bar_chart(df_non_zero_prices['price'].value_counts())


# coll5.write("### Gráfico de Marcas")
# coll5.bar_chart(df['brand'].value_counts())