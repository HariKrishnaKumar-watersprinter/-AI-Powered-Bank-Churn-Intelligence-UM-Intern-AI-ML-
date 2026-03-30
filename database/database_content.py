import streamlit as st
from database.database_create import get_all_data, engine, db_path
import pandas as pd
import os

def database_content_view():
    
    all_data = get_all_data()
    if not all_data:
        st.info("The database is currently empty. Predicted results will be saved here automatically.")
    else:
        # Fetch data using the existing SQLAlchemy engine
        data = pd.read_sql_query("select * from bank_customers", engine)
        
        # Display the data table
        st.dataframe(data, use_container_width=True)
        st.write(f"**Total number of records:** {len(data)}")

        # Generate CSV for download
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Database (CSV)",
            data=csv,
            file_name="bank_churn_history.csv",
            mime="text/csv",
            help="Click to download all saved prediction records as a CSV file."
        )

        # Generate Binary Download for the SQLite .db file
        if os.path.exists(db_path):
            with open(db_path, "rb") as f:
                st.download_button(
                    label="📂 Download Raw Database (.db)",
                    data=f,
                    file_name="bank_data.db",
                    mime="application/x-sqlite3",
                    help="Download the actual SQLite database file for use in other applications."
                )
