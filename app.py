import streamlit as st
import pandas as pd
from PIL import Image
from preprocess1 import prepro1
from preprocess2 import prepro2
import re
import sqlite3 

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


st.set_page_config(page_title="AI Ticket Classification", page_icon="fevicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Welcome To AI Ticket Classification")
def set_bg_hack_url():
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://img.freepik.com/free-vector/gray-abstract-wireframe-background_53876-99911.jpg?semt=ais_hybrid");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()


menu = ["Home","SignUp","Login"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.markdown(
    """
    <p align="justify">
    <b style="color:black">Effective bug and ticket classification is a critical task in software development, as it ensures efficient issue management and prioritization. Traditional manual classification of bugs and tickets is time-consuming and prone to inconsistencies, leading to delays in addressing software defects. By leveraging machine learning (ML) techniques, this process can be automated and enhanced. A machine learning approach to bug and ticket classification involves training models to automatically categorize tickets based on various features, such as text descriptions, severity, and historical data. Natural Language Processing (NLP) methods can be employed to extract meaningful insights from ticket descriptions, while supervised learning algorithms enable the model to learn from labeled data to predict the appropriate category. This approach improves the accuracy, speed, and consistency of ticket classification, reducing human intervention and allowing development teams to focus on critical issues more effectively. Additionally, it supports predictive analysis, helping teams identify high-priority tickets and potential bugs before they escalate, thus streamlining the software development lifecycle.</b>
    </p>
    """
    ,unsafe_allow_html=True)
    
elif choice == "SignUp":
    FirstName = st.text_input("Firstname")
    LastName = st.text_input("Lastname")
    Mobile = st.text_input("Mobile")
    City = st.text_input("City")
    Email = st.text_input("Email")
    new_password = st.text_input("Password",type='password')
    Cpassword = st.text_input("Confirm Password",type='password')
    if st.button("Signup"):
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (pattern.match(Mobile)):
            if re.fullmatch(regex, Email):
                create_usertable()
                add_userdata(FirstName,LastName,Mobile,City,Email,new_password,Cpassword)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            else:
                 st.warning("Not Valid Email")
        else:
             st.warning("Not Valid Mobile Number")
             
elif choice == "Login":
    st.subheader("Login Section")
    Email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password",type='password')
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if st.sidebar.checkbox("Login"):
        if re.fullmatch(regex, Email):
            if Email=="a@a.com" and password=="123":
                st.success("Welcome to Admin")
                create_usertable()
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
                
            else:
                
                result = login_user(Email,password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    task = st.selectbox("Selection Option",["Text Query","Upload .CSV"])
                    
                    if task == "Text Query":                    
                        ab1=st.text_input("Write Text in English")
                        task2 = st.selectbox("Selection ML",["Random Forest","Decision Tree","Extra Tree"])               
                        clss,score=prepro1(ab1,task2)
                        listToStr = ' '.join([str(elem) for elem in clss])
                        if st.button("Classify"):                        
                            st.success('The Query is '+listToStr)
                            st.success("Score is "+str(score))
                    elif task == "Upload .CSV":
                        st.subheader("Upload .CSV File Only")
                        uploaded_file = st.file_uploader("Choose a file")
                        if uploaded_file:
                            dataframe = pd.read_csv(uploaded_file)
                            st.dataframe(dataframe, 1500, 200)
                            task2 = st.selectbox("Selection ML",["Random Forest","Decision Tree","Extra Tree"])
                            clss,dff,score=prepro2(dataframe,task2)
                            listToStr = ','.join([str(elem) for elem in clss])
                            if st.button("Classify"):                        
                                st.dataframe(dff, 1500, 200)
                                st.success("Score is "+str(score))
                        else:
                            st.error("upload .csv file")
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
            