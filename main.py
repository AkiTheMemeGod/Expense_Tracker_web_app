import streamlit as st
from functions import *
from streamlit_option_menu import option_menu
import time as t
st.set_page_config("wide")

def chart():
    x = pd.read_csv("report.csv", sep=",")
    date = list(x["Date"])
    month = list(x["Month"])
    cat = list(x["Category"])
    typ = list(x["Type"])
    amt = list(x["Amount"])
    desc = list(x["Description"])

    data = {
        "Date": date,
        "Month": month,
        "Category": cat,
        "Type": typ,
        "Amount": amt,
        "Description": desc
    }
    return data


dat = chart()


def report():
    df = pd.read_csv("report.csv",index_col=False)
    st.dataframe(df,use_container_width=True)
    category = st.sidebar.multiselect(label="Select a Category",
        options=df["Category"].unique(),
        default=df["Category"].unique(),
    )
    st.bar_chart({"Type":dat["Type"]})


def expense_tracker():
    st.title("Expense Tracker")
    cat = "Expense"

    expense = get_types("expense_types.txt")

    types = st.selectbox(label="Select the type of expense:red[*]",
                         options=expense, key="type1")
    if types == "Other\n":
        other = st.text_input(label="Enter the type of expense: ")
        if other:
            expense.append(f"{other}\n")
            put_todos(expense,"expense_types.txt")
    amount = st.text_input(label="Amount:red[*]", placeholder="Enter the amount",key="amt")
    desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)",key="desc")
    col1, col2 = st.columns(2)
    with col1:
        clicked = st.button("Add Expense", on_click=lambda: track(cat, types, amount, desc), key="expense",use_container_width=True)

    with col2:
        st.button("Reset", on_click=reset_fields,use_container_width=True)


def income_tracker():
    st.title("Income Tracker")
    expense = get_types("income_types.txt")
    cat = "Income"

    types = st.selectbox(label="Select the type of expense:red[*]",
                         options=expense, key="type2")
    if types == "Other\n":
        other = st.text_input(label="Enter the type of expense: ")
        if other:
            expense.append(f"{other}\n")
            put_todos(expense, "income_types.txt")
    amount = st.text_input(label="Amount:red[*]", placeholder="Enter the amount")
    desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)")

    col1, col2 = st.columns(2)
    with col1:
        clicked = st.button("Add Expense", on_click=lambda: track(cat, types, amount, desc), key="expense",
                            use_container_width=True)
        if clicked:st.success("Recorded Successfully")

    with col2:
        st.button("Reset", on_click=reset_fields, use_container_width=True)


def track(cat: str, typ: str, amt: str, desc: str):
    if amt.startswith("0"):
        amt = amt[1:]
    if not all([cat, typ, amt, desc]):
        st.warning("Please fill in all fields before adding an entry.")
        return
    rd_csv(d=int(t.strftime("%d")), m=t.strftime("%B"), c=cat, t=typ, a=int(amt), des=desc)


def reset_fields():
    st.session_state["type1"] = None
    st.session_state["amt"] = None
    st.session_state["desc"] = None


option = option_menu(
    menu_title=None,
    options=["Expense", "Income", "Report"],
    orientation="horizontal",
    icons=["cash-coin", "cash", "file-earmark-bar-graph-fill"],
    default_index=0
)

if option == "Expense":
    expense_tracker()
if option == "Income":
    income_tracker()
if option == "Report":
    report()

