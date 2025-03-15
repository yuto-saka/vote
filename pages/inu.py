import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 日本語フォントを設定するための準備
font_path = "C:/Windows/Fonts/msgothic.ttc"  # パスは環境に合わせて変更してください
jp_font = FontProperties(fname=font_path)
rcParams['font.family'] = jp_font.get_name()

# コメントを保存するCSVファイルのパス
comments_file_path = "comments.csv"

# コメントデータの初期化
if "comments" not in st.session_state:
    if os.path.exists(comments_file_path):  # CSVファイルが存在する場合は読み込む
        st.session_state.comments = pd.read_csv(comments_file_path)["comment"].tolist()
    else:
        st.session_state.comments = []  # 存在しない場合は空のリストを作成

# 投票結果保存用CSVファイルのパス
data_file_path = "animal_votes.csv"

# 投票結果を保存・初期化するためのデータフレーム
if "votes_df" not in st.session_state:
    if os.path.exists(data_file_path):  # CSVファイルが存在する場合は読み込む
        st.session_state.votes_df = pd.read_csv(data_file_path)
    else:
        st.session_state.votes_df = pd.DataFrame(columns=["vote"])  # 新しいデータフレームを作成

# 投票のセッション状態を初期化
if "votes" not in st.session_state:
    st.session_state.votes = None  # 初期値を None に設定

# 投票ボタンと画像を左右に分割して表示
col1, col2 = st.columns(2)  # 2列に分割

with col1:
    # 左側に犬の画像を表示
    st.image("inu.jpg", caption="犬", use_column_width=True)

with col2:
    # 右側に猫の画像を表示
    st.image("neko.jpg", caption="猫", use_column_width=True)

# 投票済みかどうかのセッション状態を初期化
if "vote" not in st.session_state:
    st.session_state.vote = False

# 投票ボタンの動作設定
dog = st.button("犬")  # 犬ボタン
cat = st.button("猫")  # 猫ボタン

if dog or cat:
    if st.session_state.vote:  # 投票済みの場合は警告を表示
        st.warning("すでに投票済みです！")
    else:
        if dog:  # 犬に投票した場合
            st.session_state.votes = "犬"
        else:  # 猫に投票した場合
            st.session_state.votes = "猫"
        # 新しい投票データをデータフレームに追加
        new_row = pd.DataFrame({"vote": [st.session_state.votes]})
        st.session_state.votes_df = pd.concat([st.session_state.votes_df, new_row], ignore_index=True)
        st.session_state.votes_df.to_csv(data_file_path, index=False)  # データをCSVファイルに保存
        st.session_state.vote = True  # 投票済みとして設定
        st.success(f"{st.session_state.votes}に投票しました！")

# コメント欄の設定
st.subheader("コメント欄")
user_comment = st.text_area("コメントを入力してください", "")
if st.button("コメントを送信"):
    if user_comment.strip():  # 空白コメントを除外
        if st.session_state.votes == "犬" or st.session_state.votes == "猫":
            # 投票した派閥にコメントを追加
            st.session_state.comments.append(st.session_state.votes + "派" + user_comment)
        else:
            # どちらでもない場合のコメントを追加
            st.session_state.comments.append("どちらでもない" + user_comment)
        # コメントをCSVに保存
        comments_df = pd.DataFrame({"comment": st.session_state.comments})
        comments_df.to_csv(comments_file_path, index=False)
        st.success("コメントが送信されました！")
    else:
        st.warning("コメントが空白です。内容を入力してください！")

# 既存コメントの表示
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
    fig, ax = plt.subplots(figsize=(6, 3))  # グラフサイズを設定
    labels = results.index  # ラベル（犬、猫）
    sizes = results.values  # 値（票数）
    colors = ['#ff9999', '#66b3ff']  # カスタマイズした色

    # 棒グラフを作成
    ax.barh(['投票結果'], [sizes[0]], color=colors[0], label=labels[0])  # 最初の棒
    if len(sizes) > 1:
        ax.barh(['投票結果'], [sizes[1]], left=[sizes[0]], color=colors[1], label=labels[1])  # 次の棒

    ax.set_xlim(0, sum(sizes))  # X軸範囲を全体の合計に設定
    ax.legend(loc='best', prop={'family': jp_font.get_name()})  # 凡例を追加（日本語フォント対応）
    st.pyplot(fig)  # Streamlit上でグラフを描画