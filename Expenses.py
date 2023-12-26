from functions import *


def app():
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
    amount = st.number_input(label="Amount:red[*]", placeholder="Enter the amount", key="amt", min_value=0,
                             max_value=10000000000, value=None, format="%d")
    desc = st.text_area(label="Description", placeholder="Tell something about your expense (optional)", key="desc")
    col1, col2 = st.columns(2)
    with col1:
        clicked = st.button("Add Expense", on_click=lambda: track(cat, types, str(amount), desc), key="expense",
                            use_container_width=True)

    with col2:
        st.button("Reset", on_click=reset_fields, use_container_width=True)
    if clicked: st.success("Recorded Successfully")