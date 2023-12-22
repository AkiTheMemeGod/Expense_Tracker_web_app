import streamlit as st
from functions import *
from streamlit_option_menu import option_menu


def expense_tracker():
    st.title("Expense Tracker")

    expense = get_types()

    types = st.selectbox(label="Select the type of expense:red[*]",
                         options=expense, key="type")
    if types == "Other\n":
        other = st.text_input(label="Enter the type of expense: ")
        if other:
            expense.append(f"{other}\n")
            put_todos(expense)
    amount = st.text_input(label="Amount:red[*]", placeholder="Enter the amount")
    desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)")
    st.button("Add Expense", on_click=track(types, amount))

def income_tracker():
    st.title("Income Tracker")

    expense = get_types()

    types = st.selectbox(label="Select the type of expense:red[*]",
                         options=expense, key="type")
    if types == "Other\n":
        other = st.text_input(label="Enter the type of expense: ")
        if other:
            expense.append(f"{other}\n")
            put_todos(expense)
    amount = st.text_input(label="Amount:red[*]", placeholder="Enter the amount")
    desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)")
    st.button("Add Expense", on_click=track(types, amount))

def track(type: str, amt: str):
    if amt.startswith("0"):
        amt = amt[1:]
    print(type.strip("\n") + " : " + amt + " ₹")


#with st.sidebar:
option = option_menu(
    menu_title=None,
    options=["Expense", "Income", "Report"],
    orientation="horizontal",
    default_index=0
)

if option == "Expense":
    expense_tracker()
if option == "Income":
    income_tracker()
if option == "Report":
    expense_tracker()

