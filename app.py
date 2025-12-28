import streamlit as st

# ページ設定
st.set_page_config(layout="wide", page_title="New Material Contextualizer")

st.title("🌾 新規原材料 価値創出・提案支援アプリ")
st.markdown("""
原材料商社向け：BarleyMAXやKernzaなどの「まだ世にない原材料」を、
今の市場トレンド（受容の器）に適合させ、コンビニバイヤーが納得する「売れる文脈」を作るためのワークフロー支援ツールです。
""")

# サイドバーでフェーズ管理
phase = st.sidebar.radio("フェーズ選択", 
    ["1. 原材料の因数分解", 
     "2. 「受容の器」探索プロンプト生成", 
     "3. コンセプト立案＆バイヤーロジック構築", 
     "4. FGI調査設計", 
     "5. 提案資料構成案"]
)

# セッションステートの初期化（入力内容を保持するため）
if 'material_info' not in st.session_state:
    st.session_state.material_info = {}
if 'trend_search_result' not in st.session_state:
    st.session_state.trend_search_result = ""
if 'concept_draft' not in st.session_state:
    st.session_state.concept_draft = ""
if 'fgi_insights' not in st.session_state:
    st.session_state.fgi_insights = ""

# --- Phase 1: 原材料の因数分解 ---
if phase == "1. 原材料の因数分解":
    st.header("1. 原材料の「機能」と「情緒」を言語化する")
    st.info("素材が持つポテンシャルを「機能性」だけでなく「体験価値」として定義します。")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("原材料名", placeholder="例：BarleyMAX、Kernza")
        func_feat = st.text_area("機能的特徴（スペック）", placeholder="例：レタスの○倍の食物繊維、低GI、グルテンフリー...")
        sensory_feat = st.text_area("感覚的特徴（五感・体験）重要！", placeholder="例：プチプチした食感、香ばしいナッツのような香り、茶色の見た目、噛みごたえ...")
    with col2:
        origin_story = st.text_area("開発背景・ストーリー", placeholder="例：オーストラリアの研究機関が開発、環境再生型農業（リジェネラティブ）由来...")
        target_category = st.text_input("想定している商品カテゴリ（仮）", placeholder="例：おにぎり、ベーカリー、サラダトッピング")

    if st.button("情報を保存"):
        st.session_state.material_info = {
            "name": name,
            "func": func_feat,
            "sensory": sensory_feat,
            "story": origin_story,
            "category": target_category
        }
        st.success("原材料情報を保存しました。次のフェーズへ進んでください。")

# --- Phase 2: 「受容の器」探索プロンプト生成 ---
elif phase == "2. 「受容の器」探索プロンプト生成":
    st.header("2. 素材が輝く「トレンドの波」を探す")
    st.markdown("この素材が入り込める市場の**「空席（受容の器）」**を探すためのプロンプトを発行します。")
    
    if not st.session_state.material_info:
        st.warning("先にフェーズ1で原材料情報を入力してください。")
    else:
        m = st.session_state.material_info
        
        st.subheader("Gemini / Deep Research用 調査プロンプト")
        st.markdown("以下のプロンプトをコピーして、Gemini Advanced (Deep Research推奨) に入力してください。")
        
        # プロンプトの生成ロジック
        search_prompt = f"""
あなたは優秀なフードマーケター兼トレンドアナリストです。
以下の「新しい原材料」を日本のコンビニ市場（または量販店）に導入するための、市場の「受容の器（トレンドの波）」を調査・特定してください。

【対象原材料】
- 名前: {m['name']}
- 感覚的特徴（重要）: {m['sensory']}
- 機能的特徴: {m['func']}
- 背景: {m['story']}
- 想定カテゴリ: {m['category']}

【調査・分析してほしいこと】
単に「{m['name']}」の検索数を見るのではなく、この素材の特徴がフィットする「現在〜未来のトレンド」を探ってください。

1. **イノベーター・アーリーアダプター層の動向**:
   - 現在、SNS（Instagram, TikTok）や専門誌で、上記「感覚的特徴（例：食感、香り）」や「背景（例：サステナブル）」に関連するキーワードで盛り上がっている食品トレンドは何か？
   - 具体的なメニュー名やハッシュタグは？

2. **「過去のヒット」からの類推**:
   - 過去に「似たような特徴（食感やヘルシーさ）」でヒットした事例はあるか？（例：もち麦、オートミール、ピスタチオなど）
   - それらはなぜマジョリティに受け入れられたのか？

3. **コンビニ市場の「空席」**:
   - 現在のコンビニの棚（{m['category']}周辺）で、消費者が飽きを感じているポイントはどこか？
   - そこにこの原材料が入ることで解決できる「新しい体験」は何か？

出力は、具体的なトレンドキーワード、事例、そして「なぜ今、この素材がいけるのか」の仮説を含めてレポートしてください。
"""
        st.code(search_prompt, language="text")
        
        st.markdown("---")
        st.subheader("調査結果の入力")
        result_input = st.text_area("Geminiから得られた調査レポートをここに貼り付けてください", height=300)
        if st.button("調査結果を保存"):
            st.session_state.trend_search_result = result_input
            st.success("調査結果を保存しました。")

# --- Phase 3: コンセプト立案＆バイヤーロジック構築 ---
elif phase == "3. コンセプト立案＆バイヤーロジック構築":
    st.header("3. コンセプト開発と「バイヤー説得ロジック」の生成")
    
    if not st.session_state.trend_search_result:
        st.warning("フェーズ2で調査結果を入力してください。")
    else:
        st.markdown("調査結果に基づき、**「コンビニ担当者が上司に説明できる」**レベルの企画ロジックを作成するためのプロンプトです。")
        
        m = st.session_state.material_info
        
        analysis_prompt = f"""
あなたは大手コンビニの商品開発コンサルタントです。
以下の「原材料情報」と「市場調査結果」を掛け合わせ、最もヒット確率が高い商品企画と、バイヤー向けの説得ロジックを作成してください。

【原材料情報】
- {m['name']} ({m['sensory']} / {m['func']})

【市場調査・トレンド情報】
{st.session_state.trend_search_result}

【作成してほしいアウトプット】
以下の3つの要素で構成された企画案を3パターン提案してください。

1. **商品コンセプト（What）**:
   - 商品名案、ターゲット（アーリーアダプター〜アーリーマジョリティ）
   - 「食べる理由」（機能ではなく、気分の描写。例：罪悪感のない夜食、作業中のリフレッシュなど）

2. **「過去のヒット」を用いた説得ロジック（Why Now）**:
   - **「これは、次の◯◯（過去のヒット商品）である」**という類推ロジックを作ってください。
   - 例：「かつて『もち麦おにぎり』が食感と腸活でヒットしましたが、この商品はその食感をさらに香ばしくし、パン派の層を取り込む『次世代のもち麦』です」
   - コンビニ担当者が社内会議でそのまま使える言葉を選んでください。

3. **採用のしやすさ（How）**:
   - オペレーション負荷が低く、既存の製造ラインで作りやすいメニュー提案。

出力形式は、バイヤーへのプレゼンメモ形式でお願いします。
"""
        st.code(analysis_prompt, language="text")
        
        st.markdown("---")
        st.subheader("コンセプト案の入力")
        concept_input = st.text_area("Geminiが生成した企画案・ロジックをここに貼り付けてください", height=300)
        if st.button("コンセプトを保存"):
            st.session_state.concept_draft = concept_input
            st.success("コンセプトを保存しました。")

# --- Phase 4: FGI調査設計 ---
elif phase == "4. FGI調査設計":
    st.header("4. 消費者受容性調査 (FGI) の設計")
    
    if not st.session_state.concept_draft:
        st.warning("フェーズ3でコンセプト案を入力してください。")
    else:
        st.markdown("企画の「独りよがり」を防ぐため、消費者の「生の声」を確認するFGI（グループインタビュー）の設計書を作成します。")
        
        fgi_prompt = f"""
考案された以下の「新商品コンセプト」について、定性調査（FGI）を行うための設計書を作成してください。

【検証したい商品コンセプト】
{st.session_state.concept_draft}

【作成依頼内容】
1. **対象者プロファイル（スクリーニング条件）**:
   - イノベーター理論に基づき、この商品を最初に手に取るであろう層（アーリーアダプター寄り）の条件。
   - 年代、職業だけでなく、「普段の食生活」や「価値観」の条件。

2. **モデレーターへの指示書（質問フロー）**:
   - 参加者から引き出したい「本音」を探るための質問リスト。
   - 特に確認したい点：
     - 「機能（健康）」と「情緒（食感・味）」のどちらに反応したか？
     - 提示された「過去のヒット商品の類推（これは次の◯◯です）」は、消費者にとって納得感があるか？
     - どの売り場に置いてあれば手に取るか？価格感は？

3. **評価のKPI（定性）**:
   - 「売れそう」ではなく「納得した（確かにそうだよね）」という反応が得られたかを判断するシグナルとなる発言例。
"""
        st.code(fgi_prompt, language="text")
        
        st.markdown("---")
        st.subheader("FGI結果（議事録要約）の入力")
        fgi_input = st.text_area("実施したFGIの重要な気付き・議事録をここに貼り付けてください", height=300)
        if st.button("FGI結果を保存"):
            st.session_state.fgi_insights = fgi_input
            st.success("FGI結果を保存しました。")

# --- Phase 5: 提案資料構成案 ---
elif phase == "5. 提案資料構成案":
    st.header("5. 最終提案資料プロンプトの生成")
    
    if not st.session_state.fgi_insights:
        st.warning("フェーズ4でFGI結果を入力してください。")
    else:
        st.markdown("Gensparkなどのスライド生成AI、またはPowerPoint作成のために、これまでの全情報を統合した指示書を作成します。")
        
        final_prompt = f"""
あなたはプロのプレゼンテーションクリエイターです。
原材料商社として、大手コンビニチェーンのバイヤーに対し、新しい原材料を使った商品を提案するための資料構成案を作成してください。

【前提情報】
1. **原材料**: {st.session_state.material_info}
2. **市場の機会（トレンド）**: {st.session_state.trend_search_result}
3. **提案コンセプト＆ロジック**: {st.session_state.concept_draft}
4. **消費者検証の結果（FGI）**: {st.session_state.fgi_insights}

【資料構成要件】
スライド枚数：10枚程度
ストーリーライン：
1. **Introduction**: 市場の変化と新たな消費者のニーズ（「売れるもの」ではなく「納得するもの」へのシフト）。
2. **The Gap**: 現在のコンビニ棚に足りない要素と、そこに対する機会。
3. **The Solution**: 原材料「{st.session_state.material_info.get('name')}」の紹介。ただしスペック列挙ではなく、体験価値を中心に。
4. **The Analogy**: バイヤーが社内で説明しやすい「魔法の言葉」（過去のヒット商品との対比）。
5. **Consumer Voice**: FGIでのリアルな反応（エビデンス）。
6. **Product Proposal**: 具体的な商品イメージと展開案。
7. **Impact**: これを採用することでコンビニ側が得られる未来（新しい客層の獲得など）。

出力は、各スライドの「タイトル」「メインメッセージ」「掲載すべき要素（グラフや写真のイメージ）」を表形式でまとめてください。
"""
        st.code(final_prompt, language="text")
        st.success("このプロンプトをGensparkやChatGPTに入力して、スライド構成を作成してください。")