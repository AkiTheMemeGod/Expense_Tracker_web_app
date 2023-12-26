from functions import *

# st.session_state.user_csv = f"account/{str(st.session_state.username)}/report.csv"
# st.session_state.user_pdf = f"account/{str(st.session_state.username)}/report.pdf"


def app():
    try:
        print(st.session_state.user_csv)
        df = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, index_col=False)
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
        st.title("Report")
        st.dataframe(df_selection, use_container_width=True)
        PDFbyte = generate_pdf()
        st.sidebar.markdown("---")
        clicked = st.sidebar.download_button(label="Download Report",
                                             data=PDFbyte,
                                             file_name=st.session_state.user_pdf,
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
    except:
        st.error("Login First")