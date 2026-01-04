import streamlit as st
import pdfplumber

# --- ページ設定 ---
st.set_page_config(layout="wide", page_title="Trend-First Material Contextualizer v2.1")

# --- セッションステートの初期化 ---
# 画面遷移しても入力データを保持するために必要です
if 'trend_analysis' not in st.session_state:
    st.session_state.trend_analysis = ""
if 'material_raw_text' not in st.session_state:
    st.session_state.material_raw_text = ""
if 'material_name' not in st.session_state:
    st.session_state.material_name = ""
if 'synthesis_result' not in st.session_state:
    st.session_state.synthesis_result = ""

# --- サイドバー（ここで phase 変数を定義します） ---
st.sidebar.title("プロセスナビゲーション")
phase = st.sidebar.radio("フェーズを選択", 
    ["1. 高解像度トレンド予測", 
     "2. 原材料情報の取り込み", 
     "3. トレンド × 原材料マッチング提案"]
)

st.title("🌊 Trend-First Material Contextualizer v2.1")
st.markdown("「食のトレンド」起点で、新規原材料の価値を創出する支援ツール")

# ==========================================
# Phase 1: 高解像度トレンド予測 (食トレンド特化版)
# ==========================================
if phase == "1. 高解像度トレンド予測":
    st.header("1. 市場トレンドの解像度を高める（食領域特化）")
    st.markdown("""
    クライアント（メーカー・小売）が求めているのは、あくまで**「食品・飲料」に落とし込めるトレンド**です。
    指定した領域における「食のアプローチ」の変化を深掘りします。
    """)

    st.subheader("STEP 1: 調査スコープの定義")
    
    col1, col2 = st.columns(2)
    with col1:
        # 大分類の選択（すべて「食」に関連づける）
        domain = st.selectbox("調査する大領域（ドメイン）", 
            [
                "ヘルスケアに関する食トレンド（体調管理・機能性・未病）",
                "美容に関する食トレンド（美肌・痩身・アンチエイジング）",
                "ライフスタイルに関する食トレンド（サステナブル・タイパ・心理的満足）",
                "嗜好・フレーバーに関する食トレンド（味・食感・海外メニュー）"
            ]
        )
    
    with col2:
        # 具体的な深掘りテーマの入力
        focus_topic = st.text_input("深掘りしたい具体的テーマ（任意）", 
            placeholder="例：痩身（ダイエット）、睡眠の質、腸活、ストレスケア",
            help="入力すると、その悩みに対して「食でどう解決するか」のトレンド変遷を分析します。"
        )

    # プロンプトの構成ロジック（食限定の制約を追加）
    if focus_topic:
        # 【特化型プロンプト】 特定テーマの「食による解決策」の系譜
        target_instruction = f"""
        あなたは食品業界専門のトレンドアナリストです。
        今回は**「{domain}」**の観点から、特に**「{focus_topic}」**というテーマに絞って、
        **「食品・飲料・食事法」**におけるトレンド分析を行ってください。
        
        【重要】
        化粧品、美容医療、運動器具などの「非食品」情報は除外してください。
        あくまで「食」でどう解決しようとしているか、に焦点を当ててください。
        """
        
        analysis_points = f"""
        1. **「{focus_topic}」に対する食アプローチの変遷**:
           - 過去（Before）：以前はどのような成分や食事法が主流だったか？
           - 現在（Now）：今、スーパーやコンビニで「{focus_topic}」訴求の商品はどのようなものが売れているか？
           - **未来（Future 1〜2年後）**：次はどのような「食のソリューション」が来るか？（例：成分の変化、摂取スタイルの変化など）

        2. **イノベーター・アーリーアダプターの食卓**:
           - 海外や健康意識の高い層が、{focus_topic}のために新しく取り入れている食材（スーパーフードや新素材）は？
        
        3. **既存食品への不満**:
           - 現在の{focus_topic}対応食品（例：ダイエット食品など）に対して、消費者が感じている「味」や「イメージ」の不満は？
        """
    else:
        # 【全体型プロンプト】 領域全体の食の波を見る
        target_instruction = f"""
        あなたは食品業界専門のフューチャリストです。
        **「{domain}」**という切り口で、向こう1〜2年の食品市場のメガトレンドを予測してください。
        化粧品や雑貨ではなく、あくまで「食べるもの・飲むもの」のトレンドに限定してください。
        """
        
        analysis_points = """
        1. **食のマクロトレンド予測**:
           - 消費者はこの領域（ヘルスケア/美容など）に対し、食事で何を求めるようになっているか？
           - 「機能性」と「美味しさ」のバランスはどう変化しているか？

        2. **注目の食材・キーワード**:
           - 今後1〜2年でパッケージに記載されることが増えるであろうキーワードや原材料を3つ挙げてください。
        """

    # 最終的なプロンプトの結合
    trend_prompt = f"""
{target_instruction}

【調査・分析対象】
- 領域: {domain}
- フォーカス: {focus_topic if focus_topic else "領域全体"}
- 期間: 向こう1〜2年（2025年後半〜2027年）

【出力してほしいレポート内容】
食品メーカーやコンビニの商品開発担当者が「なるほど、次はこういう商品を作ればいいのか」と納得できる情報が必要です。
以下の構成でレポートを作成してください。

{analysis_points}

出力は、具体的な「メニュー例」「食材名」「ヒット商品の傾向」を交えて論理的に記述してください。
"""

    st.markdown("---")
    st.subheader("STEP 2: 調査プロンプトの生成")
    st.info("以下のプロンプトをGemini (Deep Research推奨) や Perplexity に入力してください。")
    st.code(trend_prompt, language="text")
    
    st.markdown("---")
    st.subheader("STEP 3: 分析結果の入力")
    trend_input = st.text_area("AIが出力した「食トレンド分析レポート」をここに貼り付けてください", height=400)
    
    if st.button("トレンド情報を保存"):
        st.session_state.trend_analysis = trend_input
        st.success(f"トレンド情報（{focus_topic if focus_topic else domain}）を保存しました。")

# ==========================================
# Phase 2: 原材料情報の取り込み
# ==========================================
elif phase == "2. 原材料情報の取り込み":
    st.header("2. 新規原材料の情報をインプット")
    st.info("メーカーや産地から取り寄せた資料（PDF）やWebサイトのテキストを取り込みます。手入力の手間を省きます。")

    st.subheader("資料のアップロード (PDF)")
    uploaded_file = st.file_uploader("原材料の資料（PDF）があればアップロードしてください", type="pdf")
    
    extracted_text = ""
    
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            st.success("PDFからテキストを抽出しました。")
        except Exception as e:
            st.error(f"PDFの読み込みに失敗しました: {e}")
    
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

# ==========================================
# Phase 3: トレンド × 原材料マッチング提案
# ==========================================
elif phase == "3. トレンド × 原材料マッチング提案":
    st.header("3. 「未来のトレンド」に「原材料」をあてはめる")
    
    if not st.session_state.trend_analysis or not st.session_state.material_raw_text:
        st.warning("【注意】フェーズ1（トレンド）とフェーズ2（原材料）の入力を完了させてください。")
    else:
        st.markdown(f"**「{st.session_state.material_name}」** が、先ほど分析した **「未来の食トレンド」** において、なぜ必要なのか？そのロジックを構築します。")
        
        st.subheader("STEP 1: マッチング・プロンプト生成")
        st.markdown("以下のプロンプトは、雑多な原材料情報から重要な要素（感覚・機能・背景）を自動抽出し、トレンドと結びつけるよう指示されています。")
        
        # 統合分析用プロンプト
        synthesis_prompt = f"""
あなたは大手商社の敏腕事業開発担当です。
「未来の食トレンド」に基づき、特定の「新規原材料」を食品メーカーやコンビニに売り込むための企画書構成案を作成してください。

【1. ベースとなる市場環境（未来の食トレンド）】
{st.session_state.trend_analysis}

【2. 売り込みたい原材料の資料データ】
（以下から、名前、感覚的特徴、機能的特徴、背景ストーリーを読み取ってください）
---
{st.session_state.material_raw_text}
---

【依頼内容：価値創出のロジック構築】
上記【1】のトレンド（食の悩み解決策）において、【2】の原材料が「不可欠な解決策（ピース）」になる理由を言語化してください。

以下の4ステップで出力してください。

1. **原材料の再定義（Profiling）**:
   - 資料データから、この素材の「機能（スペック）」だけでなく「情緒的価値（食感、色、雰囲気）」と「ストーリー」を抽出して整理してください。

2. **トレンド・フィット（Why Now?）**:
   - 予測された1〜2年後の食トレンドに対し、なぜこの素材がベストマッチするのか？
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
            st.success("企画案を保存しました。")
            
        if st.session_state.synthesis_result:
            st.markdown("### Next Action")
            st.markdown("このテキストを元に、GensparkやGammaなどのスライド生成AIに投げると、そのまま商談資料の骨子が完成します。")
