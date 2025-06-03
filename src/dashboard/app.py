import pandas as pd
import streamlit as st
import duckdb


#Configuration
DB_PATH = "C:/Users/W4rne4/git/ml-scraping/data/duckdb2.duckdb"
DASHBOARD_TITLE = "Amazon Web Scraping - Óculos Masculino"


@st.cache_data
def get_data_from_duckdb(db_path: str) -> pd.DataFrame: #Fetch data from DuckDB and return as DataFrame.
    try:
        with duckdb.connect(db_path) as conn:
            df = conn.execute("SELECT * FROM ml_items").fetchdf()
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def filter_data_by_price(df: pd.DataFrame, min_price: float, max_price: float) -> pd.DataFrame:
    return df[(df['price'] >= min_price) & (df['price'] <= max_price)]

def display_metrics(df: pd.DataFrame) -> None:
    col1, col2, col3 = st.columns(3)

    total_products = df.shape[0]
    unique_brands = df['brand'].nunique()
    avg_price = format_currency(df['price'].mean())

    col1.metric("Total Products", value=total_products)
    col2.metric("Total Brands", value=unique_brands)
    col3.metric("Average Price", value=avg_price)

def display_brand_analysis(df: pd.DataFrame) -> None:
    with st.expander("See more"):
        col1, col2, col3 = st.columns(3)

        highest_brand = df['brand'].value_counts().idxmax()
        most_rated_brand = df.groupby('brand')['rating'].mean().idxmax()

        if df['brand'].notna().any():
            max_price = df[df['brand'].notna()]['price'].max().round(0).astype(int)
            col3.metric("Highest Price", value=max_price)

        col1.metric("Highest Frequency Brand", value=highest_brand)
        col2.metric("Most Rated Brand", value=most_rated_brand)

        st.markdown("""
        - **Total Products**: Total number of rows in the dataset.
        - **Total Brands**: Number of unique brand values.
        - **Average Price**: Mean price of all products.
        - **Highest Frequency Brand**: Most common brand.
        - **Most Rated Brand**: Brand with highest average rating.
        """)

def display_price_analysis(df: pd.DataFrame) -> None:#Display price analysis with interactive filters.
    column1, _, column2 = st.columns([3.5, 0.3, 4.5])

    with column1:
        tab1, tab2, tab3 = st.tabs(["📉 Min Price", "📈 Max Price", "➗ Avg Price"])

        with tab1:
            col1, col2 = st.columns([4,2])
            with col1:
                st.write("### Cheapest Brands")
                df_non_zero_prices = df[df['price'] > 0]
            with col2: 
                low_brand = df_non_zero_prices.groupby('brand')['price'].min().sort_values(ascending=True)
                price_range = st.slider("Prices", 10, 100, (13, 50)) # Use the slider to filter the minimum prices
                low_brand_filtered = low_brand[(low_brand >= price_range[0]) & (low_brand <= price_range[1])].head(10)
                st.dataframe(low_brand_filtered)
            col1.bar_chart(low_brand_filtered, height= 400)

        with tab2:
            col1, col2 = st.columns([4,2])
            with col1:
                st.write("### Most Expensive Brands")
                df_non_zero_prices = df[df['rating'] > 0]
                
            with col2:
                price_range = st.slider("Prices", min_value=101, max_value=2050, value=(500, 2050)) 
                min_price, max_price = price_range
                df_filtered = df_non_zero_prices[(df_non_zero_prices["price"] >= min_price) & (df_non_zero_prices["price"] <= max_price)] # Filter based on selected price range
                top_brand = df_filtered.groupby('brand')['price'].max().sort_values(ascending=False).head(10) # Group by brand and show the max price for each brand
                st.dataframe(top_brand)
            col1.bar_chart(top_brand, height= 400)

        with tab3:
            st.subheader("Average Price by Brand")
            avg_price = df[df['price'] > 0].groupby('brand')['price'].mean().round(2)
            st.bar_chart(avg_price.head(10), height=400)

    with column2:
        col1, col2 = st.columns([4, 2])
        st.subheader("Most Present Brands")
        brand_counts = df['brand'].value_counts()
        filter_range = col2.slider(
            "Filter by Count",
            min_value=int(brand_counts.min()),
            max_value=int(brand_counts.max()),
            value=(int(brand_counts.min()), int(brand_counts.max()))
        )
        filtered_brands = brand_counts[
            (brand_counts >= filter_range[0]) &
            (brand_counts <= filter_range[1])
        ].reset_index()
        filtered_brands['percentage'] = (filtered_brands['count'] / df.shape[0] * 100).round(2).astype(str) + '%'

        
        col1.bar_chart(filtered_brands.set_index('brand')['count'], height=450)
        col2.dataframe(filtered_brands, height=450, hide_index=True)

def display_product_tables(df: pd.DataFrame) -> None:
    """Display product tables with ratings and full dataset."""
    col1, _, col2 = st.columns([1.3, 0.3, 5])

    with col1:
        st.subheader("Most Rated Brands")
        unique_brands = df.groupby('brand')['rating'].mean().reset_index()
        unique_brands['rating'] = unique_brands['rating'].round(0).astype(int)
        st.dataframe(unique_brands.nlargest(10, 'rating'), use_container_width=True, hide_index=True)

    with col2:
        st.subheader("All Products")
        clean_df = df[df['price'] > 0].copy()
        clean_df['Created_at'] = pd.to_datetime(clean_df['Created_at']).dt.strftime("%Y-%m-%d")
        clean_df = clean_df.sort_values('Created_at')
        clean_df[['price', 'rating']] = clean_df[['price', 'rating']].fillna(0).astype(int)
        st.dataframe(clean_df, use_container_width=True, hide_index=True)



def main():#run the Streamlit dashboard
    st.set_page_config(
        page_title="Dashboard - Óculos Masculino",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title(DASHBOARD_TITLE)

    # Load data
    df = get_data_from_duckdb(DB_PATH)
    if df.empty:
        st.warning("No data available. Please check the database connection.")
        return

    # Display sections
    display_metrics(df)
    st.divider()
    display_brand_analysis(df)
    st.divider()
    display_price_analysis(df)
    st.divider()
    display_product_tables(df)

if __name__ == "__main__":
    main()