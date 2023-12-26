from functions import *
from streamlit_option_menu import option_menu
import Expenses, Income, Report, Account


st.set_page_config(page_title="Spend It", layout="centered", page_icon="💵")


class Multiapp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():

        # st.title("$pend It.")

        with st.sidebar:
            add_logo("https://i.imgur.com/0LqV5Cv.png")
            option = option_menu(
                menu_title=None,
                options=["Account", "Expense", "Income", "Report"],
                orientation="vertical",
                icons=["person-fill", "cash-coin", "cash", "file-earmark-bar-graph-fill"],
                default_index=0
            )
        if option == "Account":
            Account.app()
        if option == "Expense":

            Expenses.app()

        if option == "Income":
            Income.app()

        if option == "Report":
            Report.app()
        st.session_state

    run()
