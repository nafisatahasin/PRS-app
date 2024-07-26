import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title('Nykaa Product Recommendation System ✨💄🛍️')

# Description
st.markdown("""
The primary aim of this project is to develop a robust and effective product recommendation system for Nykaa, an online beauty and wellness retailer.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Nykaa_Product_Review.csv')
    # Ensuring numeric conversion and handling errors
    df['Product Price'] = pd.to_numeric(df['Product Price'], errors='coerce')
    df['Product Rating'] = pd.to_numeric(df['Product Rating'], errors='coerce')
    df['Product Reviews Count'] = pd.to_numeric(df['Product Reviews Count'], errors='coerce')
    
    # Dropping rows with non-numeric values that couldn't be converted
    df.dropna(subset=['Product Price', 'Product Rating', 'Product Reviews Count'], inplace=True)
    
    return df

df = load_data()

# Display the dataset
st.subheader('Dataset Overview')
st.write(df.head())
st.write(df.describe())

# Exploratory Data Analysis (EDA)
st.subheader('Exploratory Data Analysis')

# Distribution of product prices
st.markdown('### Distribution of Product Prices')
fig = px.histogram(df, x='Product Price', nbins=30, title='Distribution of Product Prices')
fig.update_xaxes(title='Price')
fig.update_yaxes(title='Frequency')
st.plotly_chart(fig)

# Product category distribution
st.markdown('### Product Category Distribution')
category_count = df['Product Category'].value_counts().reset_index()
category_count.columns = ['Product Category', 'count']
fig = px.bar(category_count, x='Product Category', y='count', title='Product Category Distribution')
fig.update_xaxes(title='Category')
fig.update_yaxes(title='Count')
st.plotly_chart(fig)

# Distribution of product ratings
st.markdown('### Distribution of Product Ratings')
fig = px.histogram(df, x='Product Rating', nbins=30, title='Distribution of Product Ratings')
fig.update_xaxes(title='Rating')
fig.update_yaxes(title='Frequency')
st.plotly_chart(fig)

# Price vs Rating Scatter Plot
st.markdown('### Price vs Rating')
fig = px.scatter(df, x='Product Price', y='Product Rating', title='Price vs Rating', hover_data=['Product Name'])
fig.update_xaxes(title='Price')
fig.update_yaxes(title='Rating')
st.plotly_chart(fig)

# Most Reviewed Products
st.subheader('Most Reviewed Products')

# Top 10 most reviewed products
st.markdown('#### Top 10 Most Reviewed Products')
top_10_most_reviewed = df.sort_values(by='Product Reviews Count', ascending=False).head(10)
st.write(top_10_most_reviewed[['Product Name', 'Product Brand', 'Product Rating', 'Product Reviews Count', 'Product Price', 'Product Url']])

# Sidebar for user input
st.sidebar.header('User Input Parameters')

def user_input_features():
    product_brand = st.sidebar.selectbox('Product Brand', df['Product Brand'].unique())
    product_category = st.sidebar.selectbox('Product Category', df['Product Category'].unique())
    min_price = st.sidebar.slider('Min Price', min_value=int(df['Product Price'].min()), max_value=int(df['Product Price'].max()), value=int(df['Product Price'].min()))
    max_price = st.sidebar.slider('Max Price', min_value=int(df['Product Price'].min()), max_value=int(df['Product Price'].max()), value=int(df['Product Price'].max()))
    return {'Product Brand': product_brand, 'Product Category': product_category, 'Min Price': min_price, 'Max Price': max_price}

user_inputs = user_input_features()
st.subheader('User Input')
st.write(user_inputs)

# Recommendation Logic
filtered_data = df[(df['Product Brand'] == user_inputs['Product Brand']) & 
                   (df['Product Category'] == user_inputs['Product Category']) & 
                   (df['Product Price'] >= user_inputs['Min Price']) & 
                   (df['Product Price'] <= user_inputs['Max Price'])]

st.subheader('Recommended Products')
if not filtered_data.empty:
    st.write(filtered_data[['Product Name', 'Product Price', 'Product Rating', 'Product Reviews Count', 'Product Url']])
else:
    st.write("No products match the selected criteria.")
