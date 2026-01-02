import streamlit as st
import pdfplumber

# ページ設定
st.set_page_config(layout="wide", page_title="Trend-First Material Contextualizer")

# セッションステートの初期化
if 'trend_analysis' not in st.session_state:
    st.session_state.trend_analysis = ""
if 'material_raw_text' not in st.session_state:
    st.session_state.material_raw_text = ""
if 'material_name' not in st.session_state:
    st.session_state.material_name = ""
if 'synthesis_result' not in st.session_state:
    st.session_state.synthesis_result = ""

# サイドバー
st.sidebar.title("プロセスナビゲーション")
phase = st.sidebar.radio("フェーズを選択", 
    ["1. 美容・健康トレンド未来予測", 
     "2. 原材料情報の取り込み", 
     "3. トレンド × 原材料マッチング提案"]
)

st.title("🌊 Trend-First Material Contextualizer")
st.markdown("「原材料を売る」のではなく、「来るべきトレンドの不可欠なピース」として提案するための支援ツール")

# --- Phase 1: トレンド予測 ---
if phase == "1. 美容・健康トレンド未来予測":
    st.header("1. 向こう1〜2年の「食と健康」トレンドを掴む")
    st.info("まずは原材料のことを忘れ、市場環境と消費者の意識変化を分析します。商社担当者が「確かにそういう流れ来てるよね」と納得するエビデンスを集めます。")

    st.subheader("STEP 1: トレンド調査プロンプトの生成")
    st.markdown("以下のプロンプトをコピーして、Gemini (または Perplexity / ChatGPT) に入力してください。")
    
    # トレンド分析用プロンプト
    trend_prompt = """
あなたはフードトレンドの専門家であり、未来予測アナリストです。
向こう1〜2年（2025年後半〜2027年）の日本および世界の「美容・健康・食」に関するトレンドを予測・分析してください。

【調査・分析の視点】
単なる「流行り」ではなく、消費者の価値観の変化に基づいた予測をお願いします。

1. **マクロトレンド（大きな潮流）**:
   - 「腸活」「低糖質」の次にくる概念は何か？（例：脳腸相関、概日リズム、情緒的健康など）
   - サステナビリティと個人の健康はどう結びついているか？

2. **イノベーター・アーリーアダプターの動き**:
   - 今、感度の高い層（または海外の先進市場）で兆しが見えている新しい食材や習慣は？
   - 具体的なエビデンス（流行っているメニュー、ハッシュタグ、現象）

3. **キーワード予測**:
   - 1〜2年後にコンビニやスーパーの棚を席巻するであろうキーワードを3つ挙げてください。

出力は、商社担当者が「なるほど、次はここに向かっているのか」と納得できるような、論理的かつ具体的なレポート形式でお願いします。
"""
    st.code(trend_prompt, language="text")
    
    st.markdown("---")
    st.subheader("STEP 2: 分析結果の入力")
    trend_input = st.text_area("AIが出力した「トレンド分析レポート」をここに貼り付けてください", height=400)
    
    if st.button("トレンド情報を保存"):
        st.session_state.trend_analysis = trend_input
        st.success("トレンド情報をシステムに保存しました。フェーズ2へ進んでください。")

# --- Phase 2: 原材料情報の取り込み ---
elif phase == "2. 原材料情報の取り込み":
    st.header("2. 新規原材料の情報をインプット")
    st.info("メーカーや産地から取り寄せた資料（PDF）やWebサイトのテキストを取り込みます。手入力の手間を省きます。")

    st.subheader("資料のアップロード (PDF)")
    uploaded_file = st.file_uploader("原材料の資料（PDF）があればアップロードしてください", type="pdf")
    
    extracted_text = ""
    
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
        st.success("PDFからテキストを抽出しました。")
    
    st.subheader("またはテキストを直接入力・修正")
    st.markdown("Webサイトの情報をコピペする場合や、PDF抽出結果を修正する場合は以下を使用してください。")
    
    # PDFから抽出されたテキストがあればそれを初期値にする、なければ既存の保存データ
    initial_text = extracted_text if extracted_text else st.session_state.material_raw_text
    
    material_name_input = st.text_input("原材料名（必須）", value=st.session_state.material_name, placeholder="例：BarleyMAX")
    material_text_input = st.text_area("原材料の基礎情報テキスト", value=initial_text, height=300, 
                                       placeholder="ここにPDFの中身やWebサイトの紹介文をそのまま貼り付けてください。機能、ストーリー、スペックなどが混ざっていても構いません。")
    
    if st.button("原材料情報を保存"):
        st.session_state.material_name = material_name_input
        st.session_state.material_raw_text = material_text_input
        st.success(f"{material_name_input} の情報を保存しました。フェーズ3へ進んでください。")

# --- Phase 3: トレンド × 原材料マッチング提案 ---
elif phase == "3. トレンド × 原材料マッチング提案":
    st.header("3. 「未来のトレンド」に「原材料」をあてはめる")
    
    if not st.session_state.trend_analysis or not st.session_state.material_raw_text:
        st.warning("フェーズ1（トレンド）とフェーズ2（原材料）の入力を完了させてください。")
    else:
        st.markdown(f"**「{st.session_state.material_name}」** が、先ほど分析した **「未来の健康トレンド」** において、なぜ必要なのか？そのロジックを構築します。")
        
        st.subheader("STEP 1: マッチング・プロンプト生成")
        st.markdown("以下のプロンプトは、雑多な原材料情報から重要な要素（感覚・機能・背景）を自動抽出し、トレンドと結びつけるよう指示されています。")
        
        # 統合分析用プロンプト
        synthesis_prompt = f"""
あなたは大手商社の敏腕事業開発担当です。
「未来のトレンド」に基づき、特定の「新規原材料」をメーカーや小売に売り込むための企画書構成案を作成してください。

【1. ベースとなる市場環境（未来トレンド）】
{st.session_state.trend_analysis}

【2. 売り込みたい原材料の資料データ】
（以下から、名前、感覚的特徴、機能的特徴、背景ストーリーを読み取ってください）
---
{st.session_state.material_raw_text}
---

【依頼内容：価値創出のロジック構築】
上記【1】のトレンドにおいて、【2】の原材料が「不可欠な解決策（ピース）」になる理由を言語化してください。

以下の4ステップで出力してください。

1. **原材料の再定義（Profiling）**:
   - 資料データから、この素材の「機能」だけでなく「情緒的価値（食感、色、雰囲気）」と「ストーリー」を抽出して整理してください。

2. **トレンド・フィット（Why Now?）**:
   - 予測された1〜2年後のトレンド（例：〇〇という健康概念）に対し、なぜこの素材がベストマッチするのか？
   - 既存の素材（小麦や通常の雑穀など）では満たせない、どの「穴」を埋めることができるか？

3. **提案コンセプト（Concept）**:
   - この素材を使った、未来のヒット商品イメージ（コンビニおにぎり、パン、スイーツ、飲料など）。
   - 「売れるもの」ではなく、消費者が「納得するもの（確かに今の気分だよね）」という観点で。

4. **商社担当者のための「キラーフレーズ」**:
   - 担当者がバイヤーに説明する際に使うべき、一言で刺さるキャッチコピーや例え話（メタファー）。
   - 例：「これは、腸活界のピスタチオ（映え×機能）です」など。

"""
        st.code(synthesis_prompt, language="text")
        
        st.markdown("---")
        st.subheader("STEP 2: 企画案の確認と保存")
        final_output = st.text_area("AIが生成した企画ロジックをここに貼り付けてください", height=400)
        
        if st.button("企画案を保存"):
            st.session_state.synthesis_result = final_output
            st.success("企画案を保存しました。これを元にGenspark等で資料化してください。")
            
        if st.session_state.synthesis_result:
            st.markdown("### Next Action")
            st.markdown("このテキストを元に、GensparkやGammaなどのスライド生成AIに投げると、そのまま商談資料の骨子が完成します。")
