import streamlit as st
from database.database import get_all_data,engine
import pandas as pd
def database_content_view():
    if st.button("Show Database Content", key="show_db_button"):
        if get_all_data() is None:
            st.write("No data found")
        else:
            st.header("💾 Database Content")
            data=pd.read_sql_query("select * from bank_customers",engine)
            st.dataframe(data)
            st.write("Total number of records: ", len(data))
