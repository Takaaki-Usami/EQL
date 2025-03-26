import streamlit as st

# ★★★ラベルレスフォーム★★★
# =========================== 
# ラベルレスフォーム
# 処理内容 : 
# ===========================
def labelless_selectbox(options,key):
    return st.selectbox(label="none",label_visibility="collapsed",options=options,key=key) or '未入力'
def labelless_number_input(min_value, step, key):
    return st.number_input(label="none",label_visibility="collapsed",min_value=min_value,step=step,key= key) or 0.00
def labelless_text_input(key):
    return st.text_input(label="none",label_visibility="collapsed",key=key) or '未入力'
def labelless_checkbox(key):
    return st.checkbox(label="none",label_visibility="collapsed",key=key)

