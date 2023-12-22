import pandas as pd
import csv2pdf as cp
def get_types(filepath):
    """This function helps to read the todos you enter into a text file"""
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos


def put_todos(tds, filepath):
    """This function helps to put the todos you enter into a text file"""
    with open(filepath, 'w') as file:
        file.writelines(tds)


def send_mail(msg):
    import smtplib as sm
    # = "This
    s = sm.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('akis.pwdchecker@gmail.com', 'tjjqhaifdobuluhg')
    s.sendmail('akis.pwdchecker@gmail.com', 'k.akashkumar@gmail.com', msg=msg)


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
    df.to_csv("report.csv",index=False,index_label=None)


def rd_csv(d: int, m, c, t, a: int, des: str):
    x = pd.read_csv("report.csv", sep=",")

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
    x.reset_index(drop=True,inplace=True)
    x.to_csv("report.csv",index=False,index_label=None)
    wrt_csv(date, month, cat, typ, amt, desc)


def generate_pdf():
    cp.convert("report.csv", "report.pdf",size=11, headersize=30, headerfont=r"RobotoMono-Bold.ttf", font=r"RobotoMono-BoldItalic.ttf")

generate_pdf()