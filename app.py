import streamlit as st
from database import insert_entry, get_summary
from datetime import date

st.set_page_config(
    page_title="ReKYC Tracker",
    layout="wide"
)

st.title("📊 ReKYC Tracker")

with st.form("entry_form"):

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

        st.success("Record Saved Successfully!")

st.divider()

st.subheader("Summary by Area")

summary = get_summary()

st.dataframe(summary, use_container_width=True)

grand_total = 0

if not summary.empty:
    grand_total = summary["total"].sum()

st.metric(
    label="Grand Total",
    value=int(grand_total)
)