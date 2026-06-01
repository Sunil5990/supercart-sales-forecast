import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="SuperCart Sales Forecast", layout="centered")

st.title("🛒 SuperCart Sales Forecast Predictor")

# User inputs
product_weight = st.number_input("Product Weight", min_value=0.0)
product_mrp = st.number_input("Product MRP", min_value=0.0)
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_type = st.selectbox(
    "Store Type",
    ["Supermarket Type1", "Supermarket Type2", "Grocery Store"]
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

product_type = st.selectbox(
    "Product Type",
    [
        "Dairy",
        "Soft Drinks",
        "Meat",
        "Fruits and Vegetables",
        "Snack Foods",
        "Household"
    ]
)

store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1980,
    max_value=2026,
    value=2010
)

if st.button("Predict Sales"):
    try:
        model = joblib.load("src/superkart_pipeline.pkl")

        df = pd.read_csv("src/data/SuperKart.csv")

        # remove target column if present
        if "Product_Store_Sales_Total" in df.columns:
            df = df.drop("Product_Store_Sales_Total", axis=1)

        # remove ID columns
        for col in ["Product_Id", "Store_Id"]:
            if col in df.columns:
                df = df.drop(col, axis=1)

        if "Store_Establishment_Year" in df.columns:
            df["Store_Age"] = 2026 - df["Store_Establishment_Year"]
            df = df.drop("Store_Establishment_Year", axis=1)
    
        # encode text columns
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("category").cat.codes

        sample = pd.DataFrame({
            "Product_Weight": [product_weight],
            "Product_MRP": [product_mrp],
            "Product_Allocated_Area": [product_allocated_area],
            "Store_Age": [2026 - store_establishment_year],
            "Store_Size": [store_size],
            "Store_Type": [store_type],
            "Product_Sugar_Content": [product_sugar_content],
            "Store_Location_City_Type": [store_location_city_type],
            "Product_Type": [product_type]
        })
        # convert year → store age
        if "Store_Age" in sample.columns:
            sample["Store_Age"] = 2026 - store_establishment_year

        prediction = model.predict(sample)

        st.success(f"Predicted Sales: ₹ {prediction[0]:,.2f}")

    except Exception as e:
        st.error(f"Error: {e}")