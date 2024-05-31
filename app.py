import streamlit as st

from candidates import candidates
# 初始化或檢索頁面狀態
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
    
if 'selected_candidate' not in st.session_state:
    st.session_state['selected_candidate'] = None
        
# 登入頁面
if st.session_state['page'] == 'login':
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
            st.session_state['page'] = 'main'

elif st.session_state['page'] == 'main':
    with st.form("選擇會長") as form:
        for candidate in candidates:
            col1, col2, col3 = st.columns([1, 2, 3])
            with col1:
                st.image(candidate["image"], width=100)  # 調整圖片大小適合顯示
            with col2:
                # 創建一個勾選框，用來選擇候選人
                is_selected = st.checkbox(candidate['name'], key=candidate['name'])
            with col3:
                st.markdown(f"[更多資料]({candidate['details']})", unsafe_allow_html=True)
        submit_button = st.form_submit_button("確認選擇")
        if submit_button:
            st.session_state['page'] = 'confirm'
            
elif st.session_state['page'] == 'confirm':
    st.title('確認選擇')
    st.write('你已經選擇了會長，請確認你的選擇。')
            