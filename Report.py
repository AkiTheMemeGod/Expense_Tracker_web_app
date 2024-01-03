import streamlit

from functions import *


def app():
    try:
        df = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, index_col=False)
        with st.sidebar:
            st.sidebar.markdown("---")
            side_title = '<h1 style="font-family:monospace; color:red; font-size: 35px;", align="center">🎯 FILTERS</h1><br>'
            st.sidebar.markdown(side_title, unsafe_allow_html=True)
            # st.sidebar.title("₹ :rainbow[FILTERS]")

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

            PDFbyte = generate_pdf(df_selection)
            st.sidebar.markdown("---")

            clicked = st.sidebar.download_button(label=":rainbow[Download Report]",
                                                 data=PDFbyte,
                                                 file_name=st.session_state.user_pdf,
                                                 mime='application/octet-stream',
                                                 on_click=lambda: generate_pdf(df_selection),
                                                 use_container_width=True)
            if clicked:
                st.sidebar.success("Downloaded Successfully")


        with st.container(border=True):
            st.title(":rainbow[Report]")
            st.dataframe(df_selection, use_container_width=True)



        with st.container(border=True):
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

        with st.container(border=True):

            st.title(":rainbow[Total:]")
            st.markdown("#")
            try:
                total_income = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][1])
                total_expense = int(df.groupby(by=['Category']).sum()[['Amount']]['Amount'][0])
                savings = total_income - total_expense

                col4, col5, col6 = st.columns(3)
                with col4:
                    st.success(f"Total Income : {total_income}₹")
                with col5:
                    st.error(f"Total Expenses : {total_expense}₹")
                with col6:
                    if savings < 0:
                        st.error(f"Total Balance : {savings}₹")
                    if savings == 0:
                        st.warning(f"Total Balance : {savings}₹")
                    if savings > 0:
                        st.success(f"Total Balance : {savings}₹")
            except IndexError:
                st.error("Enter at-least one entry in Income/Expenses")
    except AttributeError:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.error("Login to see your report", icon="⚠️")
    except FileNotFoundError:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.error("You dont have any expense or income entries yet!", icon="⚠️")
