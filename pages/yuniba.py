import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 日本語フォントを設定
font_path = "C:/Windows/Fonts/msgothic.ttc"  # パスは環境に合わせて変更してください
jp_font = FontProperties(fname=font_path)
rcParams['font.family'] = jp_font.get_name()

# コメントを保存するCSVファイルのパス
comments_file_path = "park_comments.csv"

# コメントデータの初期化
if "comments" not in st.session_state:
    if os.path.exists(comments_file_path):
        st.session_state.comments = pd.read_csv(comments_file_path)["comment"].tolist()
    else:
        st.session_state.comments = []

# 投票結果保存用CSVファイル
data_file_path = "park.csv"

# 初期化用のデータフレーム
if "votes_df" not in st.session_state:
    if os.path.exists(data_file_path):
        st.session_state.votes_df = pd.read_csv(data_file_path)
    else:
        st.session_state.votes_df = pd.DataFrame(columns=["vote"])
# セッション状態の初期化
if "votes" not in st.session_state:
    st.session_state.votes = None  # 初期値を None に設定

    

# 投票ボタンと画像の表示
col1, col2 = st.columns(2)  # 2列に分割

with col1:
    st.image("yuniba.jpg", caption="ユニバーシャルスタジオジャパン", use_column_width=True)

with col2:
    st.image("dhizny.jpg", caption="ディズニーランド", use_column_width=True)

# セッション状態の初期化
if "vote" not in st.session_state:
    st.session_state.vote = False

# 投票ボタン
yuniba = st.button("ユニバーシャルスタジオジャパン")
dhizny = st.button("ディズニーランド")

if yuniba or dhizny:
    if st.session_state.vote:
        st.warning("すでに投票済みです！")
    else:
        if yuniba:
            st.session_state.votes = "ユニバーシャルスタジオジャパン"
        else:
            st.session_state.votes = "ディズニーランド"
        # 新しい投票をDataFrameに追加
        new_row = pd.DataFrame({"vote": [st.session_state.votes]})
        st.session_state.votes_df = pd.concat([st.session_state.votes_df, new_row], ignore_index=True)
        st.session_state.votes_df.to_csv(data_file_path, index=False)
        st.session_state.vote = True
        st.success(f"{st.session_state.votes}に投票しました！")

# コメント欄
st.subheader("コメント欄")
user_comment = st.text_area("コメントを入力してください", "")
if st.button("コメントを送信"):
    if user_comment.strip():  # 空白を除いたコメントが存在する場合
        if st.session_state.votes == "ユニバーシャルスタジオジャパン" or st.session_state.votes == "ディズニーランド":
            st.session_state.comments.append(st.session_state.votes+"派"+user_comment)  # コメントをリストに追加
        else:
            st.session_state.comments.append("どちらでもない"+user_comment)
        # コメントをCSVに保存
        comments_df = pd.DataFrame({"comment": st.session_state.comments})
        comments_df.to_csv(comments_file_path, index=False)
        st.success("コメントが送信されました！")
    else:
        st.warning("コメントが空白です。内容を入力してください！")

# コメントの表示
if st.session_state.comments:
    st.subheader("みんなのコメント")
    for comment in st.session_state.comments:
        st.write(f"- {comment}")

# 投票結果の表示
if st.button("投票結果を見る"):
    results = st.session_state.votes_df['vote'].value_counts()

    st.write("投票結果:")
    for index, value in results.items():
        st.write(f"{index}: {value}票")

    # グラフを作成（帯グラフ）
    fig, ax = plt.subplots(figsize=(6, 3))
    labels = results.index
    sizes = results.values
    colors = ['#ff9999', '#66b3ff']  # 色をカスタマイズ

    ax.barh(['投票結果'], [sizes[0]], color=colors[0], label=labels[0])  # 1つ目の棒
    if len(sizes) > 1:
        ax.barh(['投票結果'], [sizes[1]], left=[sizes[0]], color=colors[1], label=labels[1])  # 2つ目の棒

    ax.set_xlim(0, sum(sizes))  # X軸の範囲を調整
    ax.legend(loc='best', prop={'family': jp_font.get_name()})  # 凡例を追加（日本語フォント対応）
    st.pyplot(fig)
