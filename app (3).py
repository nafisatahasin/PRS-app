import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Nykaa Product Recommendation System",
    page_icon="✨💄🛍️",
    layout="wide"
)

# Title and description
st.title('Nykaa Product Recommendation System ✨💄🛍️')
st.markdown("""
Welcome to the Nykaa Product Recommendation System! Explore and find the best products based on your preferences.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Nykaa_Product_Review.csv')
    df['Product Price'] = pd.to_numeric(df['Product Price'], errors='coerce')
    df['Product Rating'] = pd.to_numeric(df['Product Rating'], errors='coerce')
    df['Product Reviews Count'] = pd.to_numeric(df['Product Reviews Count'], errors='coerce')
    df.dropna(subset=['Product Price', 'Product Rating', 'Product Reviews Count'], inplace=True)
    return df

df = load_data()

# Dataset overview
st.subheader('Dataset Overview 📊')
st.write(df.head(10))
st.write(df.describe())
st.markdown("Here's an overview of the dataset, showing the first 10 products and statistical summaries.")

# EDA section
st.subheader('Exploratory Data Analysis 🔍')

col1, col2 = st.columns(2)
with col1:
    st.markdown('### Distribution of Product Prices 💲')
    fig = px.histogram(df, x='Product Price', nbins=30, title='Distribution of Product Prices', color_discrete_sequence=['#FFA07A'])
    fig.update_xaxes(title='Price')
    fig.update_yaxes(title='Frequency')
    st.plotly_chart(fig)
    st.markdown("Visual representation of how product prices are distributed.Most products are moderately priced, with fewer high-priced items.")

with col2:
    st.markdown('### Product Category Distribution 🛍️')
    category_count = df['Product Category'].value_counts().reset_index()
    category_count.columns = ['Product Category', 'Count']
    fig = px.bar(category_count, x='Product Category', y='Count', title='Product Category Distribution', color='Count', color_continuous_scale='Viridis')
    fig.update_xaxes(title='Category')
    fig.update_yaxes(title='Count')
    st.plotly_chart(fig)
    st.markdown("Shows the number of products in each category. Certain categories have a much higher variety of products than others.")

st.markdown('### Distribution of Product Ratings ⭐')
fig = px.histogram(df, x='Product Rating', nbins=30, title='Distribution of Product Ratings', color_discrete_sequence=['#FF69B4'])
fig.update_xaxes(title='Rating')
fig.update_yaxes(title='Frequency')
st.plotly_chart(fig)
st.markdown("Displays the spread of product ratings.Most products are highly rated, indicating customer satisfaction.")

st.markdown('### Price vs Rating Scatter Plot 📈')
fig = px.scatter(df, x='Product Price', y='Product Rating', title='Price vs Rating', hover_data=['Product Name'], color='Product Category', symbol='Product Category')
fig.update_xaxes(title='Price')
fig.update_yaxes(title='Rating')
st.plotly_chart(fig)
st.markdown("Correlation between product price and rating. No clear correlation between price and rating, suggesting quality doesn't always increase with price.")

# Most Reviewed Products
st.subheader('Most Reviewed Products 📚')

# Top 10 most reviewed products
st.markdown('#### Top 10 Most Reviewed Products')
top_10_most_reviewed = df.sort_values(by='Product Reviews Count', ascending=False).head(10)
st.write(top_10_most_reviewed[['Product Name', 'Product Brand', 'Product Rating', 'Product Reviews Count', 'Product Price', 'Product Url']])
st.markdown("Listing the top 10 products based on the number of reviews.Popular products with many reviews often have high ratings, indicating trustworthiness.")

# Sidebar for user input
st.sidebar.header('Customize Your Recommendation 🎨')

def user_input_features():
    product_brand = st.sidebar.selectbox('Product Brand', df['Product Brand'].unique())
    product_category = st.sidebar.selectbox('Product Category', df['Product Category'].unique())
    min_price = st.sidebar.slider('Min Price', min_value=int(df['Product Price'].min()), max_value=int(df['Product Price'].max()), value=int(df['Product Price'].min()))
    max_price = st.sidebar.slider('Max Price', min_value=int(df['Product Price'].min()), max_value=int(df['Product Price'].max()), value=int(df['Product Price'].max()))
    return {'Product Brand': product_brand, 'Product Category': product_category, 'Min Price': min_price, 'Max Price': max_price}

user_inputs = user_input_features()
st.subheader('User Input Parameters 📝')
st.write(user_inputs)
st.markdown("Input your preferences for brand, category, and price range to get personalized recommendations.")

# Recommendation Logic
filtered_data = df[(df['Product Brand'] == user_inputs['Product Brand']) & 
                   (df['Product Category'] == user_inputs['Product Category']) & 
                   (df['Product Price'] >= user_inputs['Min Price']) &
                   (df['Product Price'] <= user_inputs['Max Price'])]

st.subheader('Recommended Products 🎁')
st.write(filtered_data[['Product Name', 'Product Price', 'Product Rating', 'Product Reviews Count', 'Product Url']])
st.markdown("Products matching your criteria are displayed here.")

# Add a footer
st.markdown("""
<footer style='text-align: center;'>
    Created with ❤️ by Nafisa
</footer>
""", unsafe_allow_html=True)
