import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

# Set page layout
st.set_page_config(page_title="Nykaa Product Recommendation", layout="wide")

# Title of the app
st.title('Nykaa Product Recommendation System🛍️')

# Description
st.markdown("""
Welcome to the **Nykaa Product Recommendation System**! 🌟

Our goal is to help you find the best beauty products tailored to your needs. Whether you're looking for skincare, makeup, or wellness products, we've got you covered. Use the filters on the sidebar to narrow down your choices, and let our SVM model recommend the top products just for you! 💅
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
st.subheader('Dataset Overview 📊')
st.write(df.head())
st.write(df.describe())

# Exploratory Data Analysis (EDA)
st.subheader('Exploratory Data Analysis 🔍')

# Distribution of product prices
st.markdown('### Distribution of Product Prices 💰')
fig = px.histogram(df, x='Product Price', nbins=30, title='Distribution of Product Prices')
fig.update_xaxes(title='Price')
fig.update_yaxes(title='Frequency')
st.plotly_chart(fig)
st.markdown('*Most products are moderately priced, with fewer high-priced items.*')

# Product category distribution
st.markdown('### Product Category Distribution 🛍️')
category_count = df['Product Category'].value_counts().reset_index()
category_count.columns = ['Product Category', 'count']
fig = px.bar(category_count, x='Product Category', y='count', title='Product Category Distribution')
fig.update_xaxes(title='Category')
fig.update_yaxes(title='Count')
st.plotly_chart(fig)
st.markdown('*Certain categories have a much higher variety of products than others.*')

# Distribution of product ratings
st.markdown('### Distribution of Product Ratings ⭐')
fig = px.histogram(df, x='Product Rating', nbins=30, title='Distribution of Product Ratings')
fig.update_xaxes(title='Rating')
fig.update_yaxes(title='Frequency')
st.plotly_chart(fig)
st.markdown('*Most products are highly rated, indicating customer satisfaction.*')

# Price vs Rating Scatter Plot
st.markdown('### Price vs Rating 💵⭐')
fig = px.scatter(df, x='Product Price', y='Product Rating', title='Price vs Rating', hover_data=['Product Name'])
fig.update_xaxes(title='Price')
fig.update_yaxes(title='Rating')
st.plotly_chart(fig)
st.markdown('*No clear correlation between price and rating, suggesting quality doesn\'t always increase with price.*')

# Most Reviewed Products
st.subheader('Most Reviewed Products 📝')

# Top 10 most reviewed products
st.markdown('#### Top 10 Most Reviewed Products 🔝')
top_10_most_reviewed = df.sort_values(by='Product Reviews Count', ascending=False).head(10)
st.write(top_10_most_reviewed[['Product Name', 'Product Brand', 'Product Rating', 'Product Reviews Count', 'Product Price', 'Product Url']])
st.markdown('*Popular products with many reviews often have high ratings, indicating trustworthiness.*')

# Sidebar for user input
st.sidebar.header('User Input Parameters 🎛️')

def user_input_features():
    product_brand = st.sidebar.selectbox('Product Brand', df['Product Brand'].unique())
    product_category = st.sidebar.selectbox('Product Category', df['Product Category'].unique())
    min_price = st.sidebar.slider('Min Price', min_value=int(df['Product Price'].min()), max_value=int(df['Product Price'].max()), value=int(df['Product Price'].min()))
    max_price = st.sidebar.slider('Max Price', min_value=int(df['Product Price'].min()), max_value=int(df['Product Price'].max()), value=int(df['Product Price'].max()))
    return {'Product Brand': product_brand, 'Product Category': product_category, 'Min Price': min_price, 'Max Price': max_price}

user_inputs = user_input_features()
st.subheader('User Input 🧍')
st.write(user_inputs)

# Train the SVM model
@st.cache_data
def train_svm_model():
    # Features and target
    X = df[['Product Price', 'Product Rating']]
    y = df['Product Reviews Count']
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train SVM model
    svm_model = SVR(kernel='linear')
    svm_model.fit(X_scaled, y)
    
    return svm_model, scaler

svm_model, scaler = train_svm_model()

# Recommendation Logic
def recommend_top_products(brand, category, min_price, max_price, top_n=10):
    # Filter products based on brand, category, and price range
    filtered_df = df[(df['Product Brand'] == brand) & 
                     (df['Product Category'] == category) & 
                     (df['Product Price'] >= min_price) & 
                     (df['Product Price'] <= max_price)]
    
    # Standardize the filtered data
    filtered_X = scaler.transform(filtered_df[['Product Price', 'Product Rating']])
    
    # Predict recommendations
    filtered_df['Recommendation_Score'] = svm_model.predict(filtered_X)
    
    # Sort by recommendation score
    top_products = filtered_df.sort_values(by='Recommendation_Score', ascending=False).head(top_n)
    
    return top_products[['Product Name', 'Product Brand', 'Product Price', 'Product Rating', 'Recommendation_Score']]

# Example usage
top_products = recommend_top_products(user_inputs['Product Brand'], user_inputs['Product Category'], user_inputs['Min Price'], user_inputs['Max Price'])
st.subheader('Recommended Products 🎯')
st.write(top_products)

st.markdown("""
The recommendations are based on a Support Vector Machine (SVM) model, which takes into account the product price and rating to calculate a recommendation score. Higher scores indicate stronger recommendations.
""")
