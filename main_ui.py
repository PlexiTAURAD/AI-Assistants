import streamlit as st
import pandas as pd
import time

user_input = st.text_input("Enter query")

#to handle warranty
#def is_waranty (text : str) -> bool:
#    return True

#warrant_info : str
#if is_waranty(user_input):
#    warrant_info = st.text_input("enter warranty info")


#store your response text here
response : str = user_input

#dont touch this guy
pr_buff : str = ''
resp_text = st.text('')
for c in response:
    pr_buff = pr_buff.join(['',str(c)])
    resp_text.text(pr_buff)
    time.sleep(0.1)


anl = st.code('analysis : %s' % user_input)