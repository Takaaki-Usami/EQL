import base64
import os
import shutil
import streamlit as st
import openpyxl
import datetime
import threading

# 日本標準時（JST）
JST = datetime.timezone(datetime.timedelta(hours=9))

def create_excel(data_single, use_options_data, cast_pile_data, cement_type, precast_pile_data, cast_concrete_data, precast_concrete_data):
    # 現在時刻
    dt_now = datetime.datetime.now(JST)
    
    # ブックのコピー
    file_name = "J-CAT読込用.xlsm"
    copy_file_name = 'J-CAT転記用マクロ' + dt_now.strftime('%Y%m%d_%H%M') + '.xlsm'

    if os.path.exists(copy_file_name):
        os.remove(copy_file_name)
    shutil.copy(file_name, copy_file_name)

    wb = openpyxl.load_workbook(copy_file_name, keep_vba=True)

    if not data_single:
        st.error("データが取得できませんでした。")
        return

    # 【単一入力】書き込み
    sheet_single = wb["【【単一入力】】"]
    for i, element in enumerate(data_single):
        sheet_single[f"D{i+2}"].value = element

    # 【複数入力】書き込み
    sheet_multi = wb["【【複数入力】】"]
    j = 0
    for _, element in use_options_data.items():
        sheet_multi[f"A{j+3}"].value = element['建物用途']
        sheet_multi[f"B{j+3}"].value = element['床面積(m2)']
        j += 1

    if isinstance(cast_pile_data, dict):
        j = 0
        for _, element in cast_pile_data.items():
            sheet_multi[f"G{j+3}"].value = cement_type
            sheet_multi[f"H{j+3}"].value = element['設計基準強度(N/mm2)']
            sheet_multi[f"I{j+3}"].value = element['コンクリート数量(m3)']
            j += 1

    if isinstance(precast_pile_data, dict):
        j = 0
        for _, element in precast_pile_data.items():
            sheet_multi[f"N{j+3}"].value = element['記号']
            sheet_multi[f"O{j+3}"].value = element['杭種']
            sheet_multi[f"P{j+3}"].value = element['φ(mm)']
            sheet_multi[f"Q{j+3}"].value = element['L(mm)']
            sheet_multi[f"R{j+3}"].value = element['t(mm)']
            sheet_multi[f"S{j+3}"].value = element['員数']
            j += 1

    j = 0
    for _, element in cast_concrete_data.items():
        sheet_multi[f"X{j+3}"].value = element['セメント種別']
        sheet_multi[f"Y{j+3}"].value = element['設計基準強度(N/mm2)']
        sheet_multi[f"Z{j+3}"].value = element['数量(m3)']
        j += 1

    j = 0
    for _, element in precast_concrete_data.items():
        sheet_multi[f"AE{j+3}"].value = element['設計基準強度(N/mm2)']
        sheet_multi[f"AF{j+3}"].value = element['数量(m3)']
        j += 1

    # 保存
    wb.save(copy_file_name)

    # 🔁 3分後に削除
    def delete_file_later(path):
        if os.path.exists(path):
            os.remove(path)

    threading.Timer(180, delete_file_later, args=(copy_file_name,)).start()

    # ダウンロードリンク作成
    with open(copy_file_name, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    href = f'<a href="data:application/octet-stream;base64,{base64_data}" download="{copy_file_name}">ダウンロード</a>'

    return href
