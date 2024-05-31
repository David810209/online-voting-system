import streamlit as st

# 設定頁面標題
st.title('投票系統登入')

# 創建一個表單用於登入
with st.form("login_form", clear_on_submit=False):
    # 創建輸入框讓用戶輸入姓名和學號
    name = st.text_input("姓名")
    student_id = st.text_input("學號")

    # 創建一個核對框讓用戶選擇是否為南友會成員
    member_check = st.checkbox("是不是南友會成員")

    # 創建一個提交按鈕
    submit_button = st.form_submit_button("登入")

    # 當用戶點擊登入按鈕後顯示歡迎信息
    if submit_button:
        st.success(f"歡迎 {name}！學號：{student_id}。{'您是南友會成員。' if member_check else '您不是南友會成員。'}")
