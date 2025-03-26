import streamlit as st
from . import labelless_list as li

def generate_multicolumn_interface(header, inputs, column_widths=None):
    if header not in st.session_state:
        st.session_state[header] = [0]
        st.session_state["header_cnt"] = 0

    # フォームの増減を制御
    def add_form():
        st.session_state["header_cnt"] += 1
        form_id = st.session_state["header_cnt"]  # 一意の行IDを作成
        st.session_state[header].append(form_id)

    def remove_form(form_id):
        st.session_state[header] = [fid for fid in st.session_state[header] if fid != form_id]

    # デフォルトの列幅（均等割り）
    if column_widths is None:
        column_widths = [1] * (len(inputs)) + [0.5]  # 最後の列（削除ボタン）を小さめに

    # サブヘッダー
    st.subheader(header)

    # 増減ボタンを配置
    st.button("追加", on_click=add_form, key=f"add_button_{header}")

    # タイトル行（列幅指定）
    title_cols = st.columns(column_widths)
    for j, (title, _, _) in enumerate(inputs):
        with title_cols[j]:
            st.text(title)  # タイトルは常に表示

    # 値を格納する辞書
    input_values = {}

    # フォームの動的配置
    for i in st.session_state[header]:
        cols = st.columns(column_widths)
        row_values ={}

        for j, (title, form_type, options) in enumerate(inputs):
            with cols[j]:
                if form_type == "select_box":
                    row_values[title] = li.labelless_selectbox(options, f"{header}_{title}_{i}_{j}")
                elif form_type == "number_input":
                    row_values[title] = li.labelless_number_input(0.00, 0.01, f"{header}_{title}_{i}_{j}")
                elif form_type == "number_input2":
                    row_values[title] = li.labelless_number_input(0, 1, f"{header}_{title}_{i}_{j}")
                elif form_type == "text_input":
                    row_values[title] = li.labelless_text_input(f"{header}_{title}_{i}_{j}")
                elif form_type == "checkbox":
                    row_values[title] = li.labelless_checkbox(f"{header}_{title}_{i}_{j}")

        input_values[i] = row_values
        
        with cols[-1]:
            st.button("削除", on_click=remove_form, key=f"remove_button_{header}_{i}_{st.session_state['header_cnt']}", args=(i,))

    # 入力値を返す
    return input_values

# ★★★単一入力フォーム★★★
def generate_single_interface(title,form_type,lists):
    col1, col2 = st.columns([1,1])
    with col1:
        st.text(title)
    with col2:
        if form_type == "select_box":
            return li.labelless_selectbox(options=lists, key=title)
        elif form_type == "number_input":
            return li.labelless_number_input(min_value=0.00, step=0.01, key=title)
        elif form_type == "text_input":
            return li.labelless_text_input(key=title)
        elif form_type == "checkbox":
            return li.labelless_checkbox(key=title)
        
