import streamlit as st
from google.oauth2 import service_account
import googleapiclient.discovery

# Google Sheets API Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'mnst-isc-key.json'  # Replace with your credentials file

# Google Sheets Information
SPREADSHEET_ID = '1lddX0HRm9Nv7SFd4ldcyv8UZOzyeJ3VAtZedzPh0goY'  # Replace with your actual Google Sheet ID
RANGE_NAME = 'ISC'  # Replace with your sheet name or range

# Load data from Google Sheets
def load_data():
    creds = None
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except Exception as e:
        st.error(f"Error loading credentials: {e}")
    
    service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)

    try:
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            st.warning('No data found.')
            return None
        return values[1:], values[0]  # Data excluding header, and header
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {e}")
        return None

# Streamlit App
def main():
    st.title("Sneaker Catalog App")

    # Load data from Google Sheets
    data, header = load_data()

    if data is not None:
        # Sidebar filters
        st.sidebar.title("Filters")
        selected_size = st.sidebar.selectbox("Select Size", ["All"] + list(set(row[2] for row in data)))
        selected_price = st.sidebar.number_input("Enter Highest Price", min_value=0)

        # Filter data
        filtered_data = [row for row in data if
                         (selected_size == "All" or row[2] == selected_size) and float(row[1]) <= selected_price]

        # Display catalog
        st.title("Sneaker Catalog")

        if filtered_data:
            for row in filtered_data:
                st.image(row[3], caption=f"{row[0]} - ${row[1]} - Size {row[2]}", width=200)
        else:
            st.warning("No sneakers match the selected filters.")

if __name__ == '__main__':
    main()
