from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd


def get_engine():
    return create_engine(st.secrets["DATABASE_URL"])


def insert_entry(name, area, rekyc_number, date):

    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO entries
                (name, area, rekyc_number, date)
                VALUES
                (:name, :area, :rekyc_number, :date)
            """),
            {
                "name": name,
                "area": area,
                "rekyc_number": rekyc_number,
                "date": date
            }
        )


def get_summary(selected_date):

    engine = get_engine()

    query = """
        SELECT
            area,
            SUM(rekyc_number) AS total
        FROM entries
        WHERE date = :selected_date
        GROUP BY area
        ORDER BY area
    """

    return pd.read_sql(
        text(query),
        engine,
        params={"selected_date": selected_date}
    )


def get_all_entries():

    engine = get_engine()

    query = """
        SELECT
            name,
            area,
            rekyc_number,
            date,
            timestamp
        FROM entries
        ORDER BY date DESC, timestamp DESC
    """

    return pd.read_sql(query, engine)


def get_datewise_summary():

    engine = get_engine()

    query = """
        SELECT
            date,
            area,
            SUM(rekyc_number) AS total
        FROM entries
        GROUP BY date, area
        ORDER BY date DESC, area
    """

    return pd.read_sql(query, engine)