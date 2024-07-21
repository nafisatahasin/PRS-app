# PRS-app
Product Recommendation System
1. Project Objective
Goal: Develop a product recommendation system to suggest top products based on user preferences using the Nykaa product reviews dataset.

2. Data Preparation
Load the Data: Import the dataset into a Pandas DataFrame.
Inspect the Data: Check the first few rows, data types, and summary statistics to understand the data structure.

3. Data Cleaning
Drop Irrelevant Columns: Remove columns that are not necessary for the analysis.
Handle Missing Values: Impute or drop rows with missing values in essential columns.
Convert Data Types: Ensure Price, Review Count, and Rating are numeric.

4. Exploratory Data Analysis (EDA):Performing EDA to get a visual representation of the dataset.

5. Model Training and Evaluation
Split the data into training and testing sets Train the model using Linear Regression,Logistic Regression and SVM.
Evaluate Model: Assess the model's performance using metrics like accuracy, precision, recall, and F1 score. COMPARISON WITH OTHER MODELS: Justification: SVM was chosen over linear and logistic regression due to: Non-linear Relationships: SVM can capture non-linear relationships between features better. Margin Maximization: SVM focuses on maximizing the margin between classes, which enhances generalization. Kernel Trick: Allows for complex decision boundaries using different kernels, providing flexibility.

6. Decision Boundary Visualization:For a simplified 2D plot, consider only two features(between prices and rating,recommended and not recommended).

7. Product Recommendation
User Input: Allow the user to input a product brand.
Recommend Products: Filter and sort the products by the given brand and recommend the top 10 based on predicted scores.
Summary: The SVM-based product recommendation system efficiently identifies top products based on user preferences, leveraging SVM's strengths in handling non-linear relationships and maximizing class separation margins.
