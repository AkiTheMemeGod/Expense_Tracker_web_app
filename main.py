import streamlit as st
from functions import *
from streamlit_option_menu import option_menu
import time as t
import os
import csv2pdf as cp

st.set_page_config(page_title="Spend It", layout="centered", page_icon="💵")


def app():
    def generate_pdf():
        cp.convert("report.csv", "report.pdf",
                   size=11,
                   headersize=30,
                   headerfont=r"dependencies/RobotoMono-Bold.ttf",
                   font=r"dependencies/RobotoMono-BoldItalic.ttf")

        with open("report.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        os.remove("report.pdf")
        return PDFbyte


    def report():

        df = pd.read_csv("report.csv", index_col=False)
        # st.dataframe(df, use_container_width=True)
        st.sidebar.title("🛞 FILTERS")

        month = st.sidebar.multiselect(label="Select a Month",
                                       options=df["Month"].unique(),
                                       default=df["Month"].unique(),
                                       )
        st.sidebar.markdown("---")

        category = st.sidebar.multiselect(label="Select a Category",
                                          options=df["Category"].unique(),
                                          default=df["Category"].unique(),
                                          )
        st.sidebar.markdown("---")

        exp_type = st.sidebar.multiselect(label="Select a Type",
                                          options=df["Type"].unique(),
                                          default=df["Type"].unique(),
                                          )
        color = '#da7070'
        df_selection = df.query(
            "Month == @month & Category == @category & Type == @exp_type")
        st.title("Report Table :")
        st.dataframe(df_selection, use_container_width=True)
        PDFbyte = generate_pdf()
        st.sidebar.markdown("---")
        clicked = st.sidebar.download_button(label="Download Report",
                                             data=PDFbyte,
                                             file_name="report.pdf",
                                             mime='application/octet-stream',
                                             on_click=generate_pdf,
                                             use_container_width=True)
        if clicked: st.sidebar.success("Downloaded Successfully")

        st.markdown("#")
        st.markdown("---")
        st.markdown("#")

        st.title("Your Expenditure Spree :")
        st.markdown("#")
        st.markdown("#")

        col1, col2, col3 = st.columns(3)

        with col1:
            df_selection = df_selection.rename(
                columns={'Type': 'index'}
            ).set_index('index')
            st.bar_chart(df_selection['Amount'],
                         color=color)
        with col2:
            st.markdown("#")
            df_selection = df_selection.rename(
                columns={'Category': 'index'}
            ).set_index('index')
            st.bar_chart(df_selection['Amount'],
                         color=color)
        with col3:
            df_selection = df_selection.rename(
                columns={'Date': 'index'}
            ).set_index('index')
            st.line_chart(df_selection['Amount'],
                          color=color)
        st.markdown("#")
        st.markdown("---")
        st.markdown("#")

        st.title("Total:")
        st.markdown("#")
        st.markdown("#")
        col4, col5 = st.columns(2)
        with col4:
            st.header(f"Total Income: ")
            st.header(f"Total Expenses: ")
            st.header(f"Total Savings: ")
        with col5:
            total_income = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
            total_expense = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])
            savings = total_income - total_expense
            st.info(f"{total_income}₹")
            st.info(f"{total_expense}₹")
            if savings < 0:
                st.error(str(savings) + "₹")
            elif savings > 0:
                st.success(str(savings) + "₹")
            else:
                st.warning(str(savings) + "₹")


    def expense_tracker():
        st.title("Expense Tracker")
        cat = "Expense"

        expense = get_types("dependencies/expense_types.txt")

        types = st.selectbox(label="Select the type of expense:red[*]",
                             options=expense, key="type1")
        if types == "Other\n":
            other = st.text_input(label="Enter the type of expense: ")
            if other:
                expense.append(f"{other}\n")
                put_todos(expense, "dependencies/expense_types.txt")
        amount = st.number_input(label="Amount:red[*]", placeholder="Enter the amount", key="amt",min_value=0,max_value=10000000000, value=None,format="%d")
        desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)", key="desc")
        col1, col2 = st.columns(2)
        with col1:
            clicked = st.button("Add Expense", on_click=lambda: track(cat, types, str(amount), desc), key="expense",
                                use_container_width=True)

        with col2:
            st.button("Reset", on_click=reset_fields, use_container_width=True)
        if clicked: st.success("Recorded Successfully")


    def income_tracker():
        st.title("Income Tracker")
        expense = get_types("dependencies/income_types.txt")
        cat = "Income"

        types = st.selectbox(label="Select the type of expense:red[*]",
                             options=expense, key="type2")
        if types == "Other\n":
            other = st.text_input(label="Enter the type of expense: ")
            if other:
                expense.append(f"{other}\n")
                put_todos(expense, "dependencies/income_types.txt")
        amount = st.text_input(label="Amount:red[*]", placeholder="Enter the amount")
        desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)")

        col1, col2 = st.columns(2)
        with col1:
            clicked = st.button("Add Expense", on_click=lambda: track(cat, types, amount, desc), key="expense",
                                use_container_width=True)

        with col2:
            st.button("Reset", on_click=reset_fields, use_container_width=True)
        if clicked: st.success("Recorded Successfully")


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


    st.title("$pend It.")


    option = option_menu(
        menu_title=None,
        options=["Expense", "Income", "Report"],
        orientation="horizontal",
        icons=["cash-coin", "cash", "file-earmark-bar-graph-fill"],
        default_index=2
    )

    if option == "Expense":
        expense_tracker()
    if option == "Income":
        income_tracker()
    if option == "Report":
        report()


def check(usr, pwd):
    e, x, y = fetch_acc()
    if usr in x and pwd in y:
        app()
    else:
        st.sidebar.error("Username/Password is incorrect")


with st.sidebar:
    username = st.sidebar.text_input(label="Username:", placeholder="Username")
    password = st.sidebar.text_input(label="Password", type="password")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        st.sidebar.button("Login", use_container_width=True,on_click=lambda: check(username,password))
    with c2:
        st.sidebar.button(label="Dont have an account?", use_container_width=True)

