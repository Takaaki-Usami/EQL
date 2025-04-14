import streamlit as st
from src.modules import formula
from src.modules import write_excel
from datetime import datetime
from supabase import create_client, Client
import datetime

# Supabase接続
SUPABASE_URL = "https://gkejpglkzbwzkrjryasl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrZWpwZ2xremJ3emtyanJ5YXNsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM1NTExOTUsImV4cCI6MjA1OTEyNzE5NX0.lPGBqD_oT6GgRMpRBriEGs9HD5hPb__QAK1yggICGfg"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
use_options_data = formula.generate_multicolumn_interface("用途別面積", [
    ("建物用途", "select_box", list_use_options()),
    ("床面積(m2)", "number_input", "")
], [5,5,2])

# ■■■杭地業■■■
st.header("杭地業")
pile_type = formula.generate_single_interface("杭種","select_box",list_pile_types())
cast_pile_data = {}
precast_pile_data = {}
if pile_type == "現場打杭":
    cement_type = formula.generate_single_interface("セメント種別","select_box",list_cement_types())
    cast_pile_data = formula.generate_multicolumn_interface("現場打杭", [
        ("設計基準強度(N/mm2)","number_input2",""),  
        ("コンクリート数量(m3)","number_input","")
    ], [5,5,2])
elif pile_type == "既製杭":
    st.text("※杭記号については任意入力")
    precast_pile_data = formula.generate_multicolumn_interface("既製杭", [
        ("記号", "text_input", ""),
        ("杭種", "select_box", list_precast_piles()),
        ("φ(mm)", "number_input2", ""),
        ("L(mm)", "number_input2", ""),
        ("t(mm)", "number_input", ""),
        ("員数", "number_input2", "")
    ], [1,3,1.5,1.5,1.5,1.5,2])

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
], [4,3,3,2])
st.subheader("PCaコンクリート(鉄筋あり)")
precast_concrete_raber = formula.generate_single_interface("PCaコンクリート(m3)","number_input","")
precast_concrete_data = formula.generate_multicolumn_interface("PCaコンクリート(鉄筋なし)", [
    ("設計基準強度(N/mm2)", "number_input2", ""),
    ("数量(m3)", "number_input", "")
], [5,5,2])
st.text("※PCa内鉄筋は鉄筋数量に計上してください")

# ■■■鉄筋・鉄骨・その他■■■
st.header("鉄筋・鉄骨・その他")
rebar = formula.generate_single_interface("鉄筋(t)","number_input","")
formwork = formula.generate_single_interface("型枠(m2)","number_input","")
steel_frame = formula.generate_single_interface("鉄骨(t)","number_input","")
deck_plate = formula.generate_single_interface("デッキプレート(m2)","number_input","")

# ■■■企業情報■■■
st.header("企業情報")
affiliation = formula.generate_single_interface("所属","text_input","")
lastname = formula.generate_single_interface("姓 *","text_input","")
firstname = formula.generate_single_interface("名 *","text_input","")
department = formula.generate_single_interface("部署","text_input","")
phonenumber = formula.generate_single_interface("電話番号","text_input","")
email_address = formula.generate_single_interface("メールアドレス *","text_input","")
if "@" not in email_address and not email_address == "":
    st.warning("有効なメールアドレスを入力してください。")

# ■■■実行■■■
st.header("実行")

st.markdown("#### 免責事項")
with st.expander("入力情報の取り扱いについて（クリックで表示）"):
    st.markdown("""
    当ウェブサイト（以下「本サイト」といいます）では、ユーザーが入力フォーム等を通じて提供する情報（氏名、連絡先、物件情報、アンケート回答等を含みますがこれに限りません）について、以下の方針に基づき取り扱います。

    **1. 情報の利用目的**  
    ご提供いただいた情報は、以下の目的のために利用いたします。  
    - サービス提供に必要なご連絡および資料の送付  
    - 利用状況の分析や改善のための統計的データの作成  
    - 法令または利用規約に基づく対応  

    **2. 情報の第三者提供**  
    法令に基づく場合を除き、ご本人の同意なしに第三者に情報を提供することはありません。

    **3. 情報の管理**  
    ご提供いただいた情報は、漏えい・改ざん・不正アクセス等の防止に努め、適切に管理いたします。

    **4. 免責事項**  
    - 本サイトを通じて送信された情報の完全性・正確性・機密性について、当社は一切の保証をいたしかねます。  
    - 通信環境やシステム障害等により情報が正しく受信されなかった場合、当社は一切の責任を負いません。  
    - ユーザーが入力した内容に誤りや虚偽があった場合に生じるいかなる損害についても、当社は責任を負いかねます。

    **5. 改定について**  
    本免責事項は、必要に応じて予告なく改定されることがあります。最新の内容は本サイト上で随時ご確認ください。

    **6. 情報の活用に関する補足**  
    本サイトを通じてご提供いただいた情報は、今後のサービス品質の向上や機能改善等を目的として、
    内容を匿名化・統計化した上で、データ分析や研究開発に活用させていただくことがあります。  
    その際、個人や物件を識別できる形では一切利用いたしません。
    """)
agree = st.checkbox("上記の免責事項に同意する")
button = False
if agree:
    button = st.button("計算を実行する")
else:
    st.warning("免責事項に同意してください。")

if button:
    JST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
    data_single = {
        "main_structure": main_structure,
        "pile_type": pile_type,
        "purchased_soil": purchased_soil,
        "sand": sand,
        "gravel": gravel,
        "crushed_stone": crushed_stone,
        "solidifying": solidifying,
        "precast_concrete_raber": precast_concrete_raber,
        "rebar": rebar,
        "formwork": formwork,
        "steel_frame": steel_frame,
        "deck_plate": deck_plate,
        "affiliation": affiliation,
        "lastname": lastname,
        "firstname": firstname,
        "department": department,
        "phonenumber": phonenumber,
        "email_address": email_address,
        "creation_date": now,
        "update_date": now
    }

    cement_type = cement_type if pile_type == "現場打杭" else "未入力"

    link = write_excel.create_excel(
        list(data_single.values()),
        use_options_data,
        cast_pile_data,
        cement_type,
        precast_pile_data,
        cast_concrete_data,
        precast_concrete_data)

    try:
        res = supabase.table("construction_info").insert(data_single).execute()
        if not res.data or not isinstance(res.data, list) or "id" not in res.data[0]:
            raise ValueError("construction_info の登録に失敗しました。")
        construction_id = res.data[0]["id"]

        for _, data in use_options_data.items():
            supabase.table("use_options").insert({
                "construction_id": construction_id,
                "use_option": data['建物用途'],
                "area": data['床面積(m2)'],
                "creation_date": now,
                "update_date": now
            }).execute()

        if pile_type == "現場打杭":
            for _, data in cast_pile_data.items():
                supabase.table("cast_pile").insert({
                    "construction_id": construction_id,
                    "cement_type": cement_type,
                    "strength": data['設計基準強度(N/mm2)'],
                    "cast_pile_quantity": data['コンクリート数量(m3)'],
                    "creation_date": now,
                    "update_date": now
                }).execute()
        elif pile_type == "既製杭":
            for _, data in precast_pile_data.items():
                supabase.table("precast_pile").insert({
                    "construction_id": construction_id,
                    "sign": data['記号'],
                    "pile_type": data['杭種'],
                    "phi": data['φ(mm)'],
                    "pile_length": data['L(mm)'],
                    "thickness": data['t(mm)'],
                    "precast_pile_quantity": data['員数'],
                    "creation_date": now,
                    "update_date": now
                }).execute()

        for _, data in cast_concrete_data.items():
            supabase.table("cast_concrete").insert({
                "construction_id": construction_id,
                "cement_type": data['セメント種別'],
                "strength": data['設計基準強度(N/mm2)'],
                "cast_concrete_quantity": data['数量(m3)'],
                "creation_date": now,
                "update_date": now
            }).execute()

        for _, data in precast_concrete_data.items():
            supabase.table("precast_concrete").insert({
                "construction_id": construction_id,
                "strength": data['設計基準強度(N/mm2)'],
                "precast_concrete_quantity": data['数量(m3)'],
                "creation_date": now,
                "update_date": now
            }).execute()

        # st.success(f"Supabaseへの登録が完了しました。Construction_info ID: {construction_id}")

    except Exception as e:
        st.error(f"登録中にエラーが発生しました: {e}")

    if link:
        st.success("Excelファイルの作成が完了しました。以下のリンクからダウンロードしてください。")
        st.markdown(link, unsafe_allow_html=True)

# ■■■お問い合わせ■■■
st.header("お問い合わせ")
st.text("ご連絡はこちらまで。 ~~~~~~~~~")