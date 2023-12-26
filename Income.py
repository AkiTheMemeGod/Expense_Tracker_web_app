from functions import *


def app():
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