# Import Library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

# Database
import sqlite3

# Page Config
st.set_page_config(
    page_title="Journal Web",
    page_icon="📚",
)

# Connection to Database
conn = sqlite3.connect("data.db")
c = conn.cursor()


# function
def create_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS journaltable(title TEXT, author TEXT, reference TEXT, date DATE, category TEXT, abstract TEXT, keywords TEXT, links TEXT)"
    )


def add_data(title, author, reference, date, category, abstract, keywords, links):
    c.execute(
        "INSERT INTO journaltable(title, author, reference, date, category, abstract, keywords, links) VALUES(?,?,?,?,?,?,?,?)",
        (title, author, reference, date, category, abstract, keywords, links),
    )
    conn.commit()


def view_all_notes():
    c.execute("SELECT * FROM journaltable")
    data = c.fetchall()
    return data


def view_all_titles():
    c.execute("SELECT DISTINCT title FROM journaltable")
    data = c.fetchall()
    return data


def view_all_category():
    c.execute("SELECT DISTINCT category FROM journaltable")
    data = c.fetchall()
    return data


def get_journal_by_category(category):
    c.execute("SELECT * FROM journaltable WHERE category='{}'".format(category))
    data = c.fetchall()
    return data


def delete_data(title):
    c.execute('DELETE FROM journaltable WHERE title="{}"'.format(title))
    conn.commit()


# Layour Template
title_temp = """
<div style="background-color:#262730;padding:20px;border-radius:12px;margin-top:20px;">
    <p style="color:white;font-size:32px;font-weight:bold;">{}</p>
    <p style="color:white;font-size:20px;padding-bottom:4px;">Author: {}</p>
    <p style="color:white;">{}</p>
    <p style="color:#67b0f6;">{}</p>
    <p style="color:white;font-weight:bold;font-size:18px;">Category: <span style="color:#67b0f6;">{}</span></p>
    <p style="text-align:justify;color:white;">{}</p>
    <p style="padding-bottom:10px;color:white;">Keywords: {}</p>
    <a href="{}" target="_blank" style="text-decoration: none;color:#101414;background-color:#67b0f6;padding:8px 12px;border-radius:4px;">Journal Links</a>
</div>

"""


# Main Function
def main():
    menu = [
        "Home",
        "Journal Category",
        "Add Journal",
        "Search Journal",
        "Manage Journal",
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.title("""Welcome to :blue[Bibrary]""")
        st.subheader(
            "Explore a world of knowledge, insights, and expertise from writers across various topics."
        )
        result = view_all_notes()
        for i in result:
            j_links = i[0]
            j_date = i[1]
            j_title = i[2]
            j_author = i[3]
            j_reference = i[4]
            j_category = i[5]
            j_abstract = i[6]
            j_keywords = i[7]
            st.markdown(
                title_temp.format(
                    j_links,
                    j_date,
                    j_title,
                    j_author,
                    j_reference,
                    j_category,
                    j_abstract,
                    j_keywords,
                ),
                unsafe_allow_html=True,
            )

    # Journal Category Menu
    elif choice == "Journal Category":
        st.subheader("Journal Category")
        st.write(":blue[View Our Jurnal by Category]")

        all_category = [i[0] for i in view_all_category()]
        postlist = st.sidebar.selectbox("Category", all_category)
        postresult = get_journal_by_category(postlist)
        for i in postresult:
            j_links = i[0]
            j_date = i[1]
            j_title = i[2]
            j_author = i[3]
            j_reference = i[4]
            j_category = i[5]
            j_abstract = i[6]
            j_keywords = i[7]
            st.markdown(
                title_temp.format(
                    j_links,
                    j_date,
                    j_title,
                    j_author,
                    j_reference,
                    j_category,
                    j_abstract,
                    j_keywords,
                ),
                unsafe_allow_html=True,
            )

    # Add Journal Menu
    elif choice == "Add Journal":
        st.subheader("Add Journal")
        st.write(":blue[Add Your Journal to Database]")
        category = [
            "Text Mining",
            "Knowledge Discovery and Management",
            "Music Information Retrieval",
            "Multimedia System",
            "Digital Security",
            "Wireless Sensor Network",
            "Smart Computing",
            "Big Data Processing and Bussiness Management",
            "User Interaction and Experience",
        ]
        create_table()
        journal_title = st.text_input("Enter Title : ")
        journal_author = st.text_input("Enter Author : ")
        journal_reference = st.text_input("Enter Publication : ")
        journal_date = st.date_input("Enter Date :")
        journal_category = st.selectbox("Select Category", category)
        journal_abstract = st.text_area("Enter Abstract : ", height=200)
        journal_keywords = st.text_input("Enter Keywords : ")
        journal_links = st.text_input("Enter Links : ")

        if st.button("Add"):
            add_data(
                journal_title,
                journal_author,
                journal_reference,
                journal_date,
                journal_category,
                journal_abstract,
                journal_keywords,
                journal_links,
            )
            st.success("Post:{} saved".format(journal_title))

    # Search Journal Menu
    elif choice == "Search Journal":
        category = [
            "Text Mining",
            "Knowledge Discovery and Management",
            "Music Information Retrieval",
            "Multimedia System",
            "Digital Security",
            "Wireless Sensor Network",
            "Smart Computing",
            "Big Data Processing and Bussiness Management",
            "User Interaction and Experience",
        ]
        st.subheader("Search Journal")
        st.write(":blue[Search Your Journal by Category]")
        search_term = st.text_input("Search by Category")
        journal_result = get_journal_by_category(search_term)

        for i in journal_result:
            j_links = i[0]
            j_date = i[1]
            j_title = i[2]
            j_author = i[3]
            j_reference = i[4]
            j_category = i[5]
            j_abstract = i[6]
            j_keywords = i[7]
            st.markdown(
                title_temp.format(
                    j_links,
                    j_date,
                    j_title,
                    j_author,
                    j_reference,
                    j_category,
                    j_abstract,
                    j_keywords,
                ),
                unsafe_allow_html=True,
            )

    # Manage Journal Menu
    elif choice == "Manage Journal":
        st.subheader("Manage Journal")
        result = view_all_notes()
        clean_db = pd.DataFrame(
            result,
            columns=[
                "title",
                "author",
                "reference",
                "date",
                "category",
                "abstract",
                "keywords",
                "links",
            ],
        )
        st.dataframe(clean_db)
        unique_title = [i[0] for i in view_all_titles()]
        delete_journal_by_titles = st.selectbox("Uniq Title", unique_title)

        if st.button("Delete"):
            delete_data(delete_journal_by_titles)
            st.warning("Deleted: '{}'".format(delete_journal_by_titles))


# Running Program
main()
