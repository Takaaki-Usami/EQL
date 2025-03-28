import streamlit as st
from src.modules import formula
from src.modules import write_excel
import pyodbc
from datetime import datetime
from src.xserver_db import xserver_class

# 選択肢を配列に格納(グローバル変数削減のため関数化)
def list_structure():
    return ["RC造", "S造", "SRC造", "CB造他", "木造"]
def list_use_options():
    return ["事務所", "ホテル・旅館", "病院・診療所", "物販店舗", "学校（小中高）", "学校（大学高専）", "飲食店", "集会施設", "独身寮", "流通施設", "工場", "集合住宅", "共用部", "駐車場"]
def list_pile_types():
    return ["現場打杭","既製杭"]
def list_cement_types():
    return ["ポルトランドセメント", "高炉セメントB種"]
def list_precast_piles():
    return ["PC杭", "PHC杭" , "SC杭", "CPRC杭"]

# 画面作成
st.title("Estem Quick LCA")
st.text("建物情報を入力すると、J-CATによる簡易算定ファイルに自動で入力が出来るExcelファイルが生成されます。")
# ■■■物件情報■■■
st.header("物件情報")
main_structure = formula.generate_single_interface("主要構造","select_box",list_structure())
use_options_data = formula.generate_multicolumn_interface("用途別面積",[
    ("建物用途", "select_box", list_use_options()),
    ("床面積(m2)", "number_input", "")
],[5,5,2])

# ■■■杭地業■■■
st.header("杭地業")
pile_type = formula.generate_single_interface("杭種","select_box",list_pile_types())

cast_pile_data = {}
precast_pile_data = {}
# 現場打杭入力
if pile_type == "現場打杭":
    cement_type = formula.generate_single_interface("セメント種別","select_box",list_cement_types())
    cast_pile_data = formula.generate_multicolumn_interface("現場打杭",[
        ("設計基準強度(N/mm2)","number_input2",""),  
        ("コンクリート数量(m3)","number_input","")
    ],[5,5,2])
    
# 既製杭入力
elif pile_type == "既製杭":
    st.text("※記号、杭記号については任意入力")
    precast_pile_data = formula.generate_multicolumn_interface("既製杭", [
        ("記号", "text_input", ""),
        ("杭種", "select_box", list_precast_piles()),
        ("φ(mm)", "number_input2", ""),
        ("L(mm)", "number_input2", ""),
        ("t(mm)", "number_input", ""),
        ("員数", "number_input2", "")
    ],[1,3,1.5,1.5,1.5,1.5,2])

# ■■■土工・地業■■■
st.header("土工・地業")
purchased_soil = formula.generate_single_interface("購入土(m3)","number_input","")
sand = formula.generate_single_interface("砂(m3)","number_input","")
gravel = formula.generate_single_interface("砂利(m3)","number_input","")
crushed_stone = formula.generate_single_interface("砕石(m3)","number_input","")

# ■■■地盤改良材■■■
st.header("地盤改良材")
solidifying = formula.generate_single_interface("改良土量(m3)","number_input","")

# ■■■コンクリート■■■
st.header("コンクリート")
cast_concrete_data = formula.generate_multicolumn_interface("現場打コンクリート", [
    ("セメント種別", "select_box", list_cement_types()),
    ("設計基準強度(N/mm2)", "number_input2", ""),
    ("数量(m3)", "number_input", "")
],[4,3,3,2])
st.subheader("PCaコンクリート(鉄筋あり)")
precast_concrete_raber = formula.generate_single_interface("PCaコンクリート(m3)","number_input","")
precast_concrete_data = formula.generate_multicolumn_interface("PCaコンクリート(鉄筋なし)",[
    ("設計基準強度(N/mm2)", "number_input2", ""),
    ("数量(m3)", "number_input", "")
],[5,5,2])
st.text("※PCa内鉄筋は鉄筋数量に計上してください")

# ■■■鉄筋・鉄骨・デッキプレート■■■
st.header("鉄筋・鉄骨・その他")
rebar = formula.generate_single_interface("鉄筋(t)","number_input","")
formwork = formula.generate_single_interface("型枠(m2)","number_input","")
steel_frame = formula.generate_single_interface("鉄骨(t)","number_input","")
deck_plate = formula.generate_single_interface("デッキプレート(m2)","number_input","")

# ■■■企業情報■■■
st.markdown('<div class="gray-box">', unsafe_allow_html=True)
st.header("企業情報")
affiliation = formula.generate_single_interface("所属","text_input","")
lastname = formula.generate_single_interface("姓 *","text_input","")
firstname = formula.generate_single_interface("名 *","text_input","")
department = formula.generate_single_interface("部署","text_input","")
phonenumber = formula.generate_single_interface("電話番号","text_input","")
email_address = formula.generate_single_interface("メールアドレス *","text_input","")
if "@" not in email_address and not email_address == "":
    st.warning("有効なメールアドレスを入力してください。")

# ■■■免責事項■■■
st.header("免責事項")
st.text("免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項免責事項")
st.markdown('</div>', unsafe_allow_html=True)

# ■■■実行ボタン■■■
st.header("実行")
st.caption("入力したデータを基にExcelファイルを生成します。")
button = st.button(label="計算を実行する",key="exe")

if button:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_single = [
        main_structure, pile_type, purchased_soil, sand, gravel,
        crushed_stone, solidifying, rebar, formwork, steel_frame, deck_plate,
        affiliation, lastname, firstname, department, phonenumber, email_address,
        now, now
    ]

    cement_type = cement_type or "未入力"

    link = write_excel.create_excel(
        data_single,
        use_options_data,
        cast_pile_data,
        cement_type,
        precast_pile_data,
        cast_concrete_data,
        precast_concrete_data)

    db = xserver_class()
    db.open()

    try:
        insert_construction_info = """
        INSERT INTO Construction_info (
            main_structure, pile_type, purchased_soil, sand, gravel, 
            crushed_stone, solidifying, rebar, formwork, steel_frame, deck_plate, 
            affiliation, lastname, firstname, department, phonenumber, email_address,
            creation_date, update_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        db.cur.execute(insert_construction_info, data_single)
        construction_id = db.cur.lastrowid

        if construction_id is None:
            raise ValueError("Construction_info にデータを挿入できませんでした。")

        insert_use_options = """
        INSERT INTO Use_options (
            Construction_ID, use_option, area, creation_date, update_date
        ) VALUES (%s, %s, %s, %s, %s)
        """
        for _, data in use_options_data.items():
            db.cur.execute(insert_use_options, (
                construction_id,
                data['建物用途'],
                data['床面積(m2)'],
                now,
                now
            ))

        if pile_type == "現場打杭":
            insert_cast_pile = """
            INSERT INTO Cast_pile (
                Construction_ID, cement_type, strength, cast_pile_quantity, creation_date, update_date
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            for _, data in cast_pile_data.items():
                db.cur.execute(insert_cast_pile, (
                    construction_id,
                    cement_type,
                    data['設計基準強度(N/mm2)'],
                    data['コンクリート数量(m3)'],
                    now,
                    now
                ))

        elif pile_type == "既製杭":
            insert_precast_pile = """
            INSERT INTO Precast_pile (
                Construction_ID, sign, pile_type, phi, pile_length, thickness, precast_pile_quantity, creation_date, update_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for _, data in precast_pile_data.items():
                db.cur.execute(insert_precast_pile, (
                    construction_id,
                    data['記号'],
                    data['杭種'],
                    data['φ(mm)'],
                    data['L(mm)'],
                    data['t(mm)'],
                    data['員数'],
                    now,
                    now
                ))

        insert_cast_concrete = """
        INSERT INTO Cast_concrete (
            Construction_ID, cement_type, strength, cast_concrete_quantity, creation_date, update_date
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        for _, data in cast_concrete_data.items():
            db.cur.execute(insert_cast_concrete, (
                construction_id,
                data['セメント種別'],
                data['設計基準強度(N/mm2)'],
                data['数量(m3)'],
                now,
                now
            ))

        insert_precast_concrete = """
        INSERT INTO Precast_concrete (
            Construction_ID, strength, precast_concrete_quantity, creation_date, update_date
        ) VALUES (%s, %s, %s, %s, %s)
        """
        for _, data in precast_concrete_data.items():
            db.cur.execute(insert_precast_concrete, (
                construction_id,
                data['設計基準強度(N/mm2)'],
                data['数量(m3)'],
                now,
                now
            ))

        db.con.commit()
        st.success(f"データベースへの登録が完了しました。Construction_info ID: {construction_id}")

    except Exception as e:
        db.con.rollback()
        st.error(f"エラーが発生しました: {e}")

    finally:
        db.close()

    if link:
        st.success("Excelファイルの作成が完了しました。以下のリンクからダウンロードしてください。")
        st.markdown(link, unsafe_allow_html=True)

# ■■■お問い合わせ■■■
st.header("お問い合わせ")
st.text("ご連絡はこちらまで。 ~~~~~~~~~")