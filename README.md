# PRS-app
Nykaa Product Recommendation System

Aim
The aim of this project is to build a recommendation system for Nykaa beauty products. The system uses machine learning to suggest the best products based on user preferences, such as brand, category, and price range.

What We Did
Set Up Streamlit: Configured the Streamlit app for a user-friendly interface and wide layout.

Load and Clean Data: Loaded the Nykaa product review dataset, ensured numeric values for price, rating, and reviews count, and handled any missing values.

Display Dataset: Provided an overview of the dataset, including a summary of key statistics and a sample of the data.

Exploratory Data Analysis (EDA):

Analyzed the distribution of product prices.

Examined the variety of products in different categories.

Studied the distribution of product ratings.

Created a scatter plot to visualize the relationship between price and rating.

Top Reviewed Products: Displayed the top 10 most reviewed products to highlight popular items.

User Input Parameters: Added a sidebar for users to input their preferences for brand, category, and price range.

Train SVM Model: Trained a Support Vector Machine (SVM) model using product price and rating as features and reviews count as the target. Standardized the features for better model performance.

Make Recommendations: Used the trained SVM model to recommend top products based on user input. Displayed the recommended products with their details and recommendation scores.

This step-by-step approach ensures a comprehensive and user-friendly product recommendation system.

Link of Deployment-https://huggingface.co/spaces/nafisa27/PRS-app
