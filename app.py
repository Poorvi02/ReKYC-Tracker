import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

from database import (
    insert_entry,
    get_summary,
    get_all_entries,
    get_datewise_summary
)

st.set_page_config(
    page_title="ReKYC Tracker",
    layout="wide"
)

st.title("📊 ReKYC Tracker")

# ------------------------
# Success Message
# ------------------------

if st.session_state.get("saved", False):
    st.success("Record Saved Successfully!")
    st.session_state.saved = False


# ------------------------
# Excel Converter
# ------------------------

def convert_to_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")

    return output.getvalue()


# ------------------------
# Entry Form
# ------------------------

with st.form("entry_form", clear_on_submit=True):

    name = st.text_input("Name")

    areas = [
        "Area 1",
        "Area 2",
        "Area 3",
        "Area 4"
    ]

    area = st.selectbox("Area", areas)

    rekyc_number = st.number_input(
        "ReKYC Number",
        min_value=0,
        step=1
    )

    dt = st.date_input(
        "Date",
        value=date.today()
    )

    submitted = st.form_submit_button("Submit")

    if submitted:

        insert_entry(
            name,
            area,
            rekyc_number,
            dt
        )

        st.session_state.saved = True
        st.rerun()


# ------------------------
# Summary
# ------------------------

st.divider()

st.subheader("Summary")

selected_date = st.date_input(
    "Select Summary Date",
    value=date.today(),
    key="summary_date"
)

summary = get_summary(selected_date)

st.write(f"### Summary for {selected_date.strftime('%d-%b-%Y')}")

if summary.empty:
    st.info("No records found for this date.")
else:
    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

grand_total = summary["total"].sum() if not summary.empty else 0

st.metric(
    "Grand Total",
    int(grand_total)
)


# ------------------------
# Downloads
# ------------------------

st.divider()

st.subheader("📥 Download Reports")

col1, col2, col3 = st.columns(3)

with col1:

    st.download_button(
        label="Today's Summary",
        data=convert_to_excel(summary),
        file_name=f"Summary_{selected_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col2:

    all_entries = get_all_entries()

    st.download_button(
        label="All Entries",
        data=convert_to_excel(all_entries),
        file_name="All_Entries.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col3:

    datewise = get_datewise_summary()

    st.download_button(
        label="Date-wise Summary",
        data=convert_to_excel(datewise),
        file_name="Datewise_Summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )