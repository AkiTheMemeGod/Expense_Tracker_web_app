import pandas as pd
from streamlit_extras.app_logo import add_logo
from streamlit_extras.metric_cards import style_metric_cards
import csv2pdf as cp
import os
import streamlit as st
import time as t


# st.session_state.user_csv = f"account/{str(st.session_state.username)}/report.csv"
# st.session_state.user_pdf = f"account/{str(st.session_state.username)}/report.pdf"


def reset_fields():
    st.session_state["type1"] = None
    st.session_state["amt"] = None
    st.session_state["desc"] = None


def track(cat: str, typ: str, amt: str, desc: str):
    if amt.startswith("0"):
        amt = amt[1:]

    if not all([cat, typ, amt, desc]):
        st.warning("Please fill in all fields before adding an entry.")
        return

    rd_csv(d=int(t.strftime("%d")), m=t.strftime("%B"), c=cat, t=typ, a=int(amt), des=desc)


def get_types(filepath):
    """This function helps to read the todos you enter into a text file"""
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos


def put_todos(tds, filepath):
    """This function helps to put the todos you enter into a text file"""
    with open(filepath, 'w') as file:
        file.writelines(tds)


def wrt_csv(date: list, month: list, cat: list, typ: list, amt: list, desc: list):

    data = {
        "Date": date,
        "Month": month,
        "Category": cat,
        "Type": typ,
        "Amount": amt,
        "Description": desc
    }
    df = pd.DataFrame(data)
    df.to_csv(path_or_buf=st.session_state.user_csv, index=False,index_label=None)


def rd_csv(d: int, m, c, t, a: int, des: str):
    x = pd.read_csv(filepath_or_buffer=st.session_state.user_csv, sep=",")

    date = list(x["Date"])
    month = list(x["Month"])
    cat = list(x["Category"])
    typ = list(x["Type"])
    amt = list(x["Amount"])
    desc = list(x["Description"])

    date.append(d)
    month.append(m)
    cat.append(c)
    typ.append(t)
    amt.append(a)
    desc.append(des)
    x.reset_index(drop=True, inplace=True)
    x.to_csv(st.session_state.user_csv, index=False,index_label=None)
    wrt_csv(date, month, cat, typ, amt, desc)


def generate_pdf():
    cp.convert(source=st.session_state.user_csv, destination=st.session_state.user_pdf,
               size=11,
               headersize=30,
               headerfont=r"dependencies/RobotoMono-Bold.ttf",
               font=r"dependencies/RobotoMono-BoldItalic.ttf")

    with open(st.session_state.user_pdf, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    os.remove(st.session_state.user_pdf)
    return PDFbyte