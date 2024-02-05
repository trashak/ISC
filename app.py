import streamlit as st
import pandas as pd

# Load your data from Google Sheets or any other source
# For simplicity, you can use a sample DataFrame
data = {
    "SKU-code": ["001", "002", "003"],
    "Sneaker name": ["Sneaker1", "Sneaker2", "Sneaker3"],
    "Size": [8, 9, 8],
    "Price": [100, 120, 90],
    "Image Link": [
        "https://image.goat.com/transform/v1/attachments/product_template_additional_pictures/images/078/081/308/original/144298_01.jpg.jpeg?action=crop&width=600",
        "https://image.goat.com/transform/v1/attachments/product_template_additional_pictures/images/079/325/277/original/522750_01.jpg.jpeg?action=crop&width=600",
        "https://image.goat.com/transform/v1/attachments/product_template_additional_pictures/images/059/084/576/original/767449_01.jpg.jpeg?action=crop&width=700",
    ],
}
df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.title("Filters")
selected_size = st.sidebar.selectbox("Select Size", ["All"] + list(df["Size"].unique()))
selected_price = st.sidebar.number_input("Enter Price", min_value=0)

# Filter data
filtered_df = df[
    ((selected_size == "All") | (df["Size"] == selected_size)) &
    ((selected_price == 0) | (df["Price"] == selected_price))
]

# Display catalog
st.title("Sneaker Catalog")
st.image(filtered_df["Image Link"].tolist(), width=200, caption=filtered_df["Sneaker name"].tolist())
