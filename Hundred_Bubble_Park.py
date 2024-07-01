import streamlit as st
import random
from PIL import Image, ImageDraw
import math

# 15色の定義
colors = {
    'あか': 'red', 'あお': 'blue', 'みどり': 'green', 'きいろ': 'yellow', 'むらさき': 'purple',
    'オレンジ': 'orange', 'ピンク': 'pink', 'ちゃいろ': '#8B4513', 'はいいろ': 'gray',
    'みずいろ': 'skyblue', 'こん': 'navy', 'きみどり': '#9ACD32', 'くろ': 'black',
    'ベージュ': 'beige', 'うすむらさき': 'lavender'
}

# 8つの図形の定義（お花を削除し、船を追加）
shapes = ['まる', 'しかく', 'さんかく', 'ごかく', 'ろっかく', 'ほし', 'おうぎ', 'ふね']

def create_shape_image(shape, color, board_size=300, shape_size=100, seed=None):
    if seed is not None:
        random.seed(seed)
    
    image = Image.new('RGB', (board_size, board_size), color='white')
    draw = ImageDraw.Draw(image)
    
    max_x = board_size - shape_size
    max_y = board_size - shape_size
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)
    
    center_x = x + shape_size // 2
    center_y = y + shape_size // 2
    
    if shape == 'まる':
        draw.ellipse([x, y, x+shape_size, y+shape_size], fill=color)
    elif shape == 'しかく':
        draw.rectangle([x, y, x+shape_size, y+shape_size], fill=color)
    elif shape == 'さんかく':
        draw.polygon([
            (center_x, y),
            (x, y+shape_size),
            (x+shape_size, y+shape_size)
        ], fill=color)
    elif shape == 'ごかく':
        points = []
        for i in range(5):
            angle = i * 72 - 90
            point_x = center_x + int((shape_size//2 - 5) * math.cos(math.radians(angle)))
            point_y = center_y + int((shape_size//2 - 5) * math.sin(math.radians(angle)))
            points.append((point_x, point_y))
        draw.polygon(points, fill=color)
    elif shape == 'ろっかく':
        draw.regular_polygon((center_x, center_y, shape_size//2 - 5), 6, fill=color)
    elif shape == 'ほし':
        points = []
        for i in range(10):
            angle = i * 36 - 90
            r = shape_size//2 - 5 if i % 2 == 0 else shape_size//4 - 5
            point_x = center_x + int(r * math.cos(math.radians(angle)))
            point_y = center_y + int(r * math.sin(math.radians(angle)))
            points.append((point_x, point_y))
        draw.polygon(points, fill=color)
    elif shape == 'おうぎ':
        # おうぎの向きを変更（要が下向き）
        draw.pieslice([x, y, x+shape_size, y+shape_size], start=240, end=300, fill=color)
    elif shape == 'ふね':
        # 船の形を描画
        hull_height = shape_size // 3
        sail_height = shape_size * 2 // 3
        
        # 船体
        draw.polygon([
            (x, y + shape_size - hull_height),
            (x + shape_size, y + shape_size - hull_height),
            (x + shape_size * 4 // 5, y + shape_size),
            (x + shape_size // 5, y + shape_size)
        ], fill=color)
        
        # 帆
        draw.polygon([
            (x + shape_size // 3, y + shape_size - hull_height),
            (x + shape_size // 3, y),
            (x + shape_size * 2 // 3, y + shape_size - hull_height - sail_height // 2)
        ], fill=color)
    
    return image

def get_random_shape_and_color():
    return random.choice(shapes), random.choice(list(colors.keys()))

def main():
    st.set_page_config(layout="centered")
    st.title("ハンドレッド・シャボン・パーク")
    
    if 'current_shape' not in st.session_state or 'current_color' not in st.session_state:
        st.session_state.current_shape, st.session_state.current_color = get_random_shape_and_color()
        st.session_state.current_seed = random.randint(0, 1000000)
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    
    st.write("がめんにでてきた「かたち」と「いろ」はなにかな？")
    
    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            image = create_shape_image(st.session_state.current_shape, colors[st.session_state.current_color], seed=st.session_state.current_seed)
            img_placeholder = st.empty()
            img_placeholder.image(image, use_column_width=True)
    
    st.markdown("""
    <style>
    .stButton>button {
        width: 80%;
        height: 60px;
        font-size: 24px;
        font-weight: bold;
        margin: 10px auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("がめんをかえる", key="change_button"):
            st.session_state.show_answer = False
            new_shape, new_color = get_random_shape_and_color()
            while (new_shape, new_color) == (st.session_state.current_shape, st.session_state.current_color):
                new_shape, new_color = get_random_shape_and_color()
            st.session_state.current_shape, st.session_state.current_color = new_shape, new_color
            st.session_state.current_seed = random.randint(0, 1000000)
            new_image = create_shape_image(new_shape, colors[new_color], seed=st.session_state.current_seed)
            img_placeholder.image(new_image, use_column_width=True)
    
    with col2:
        if st.button("こたえをみる", key="answer_button"):
            st.session_state.show_answer = True
    
    if st.session_state.show_answer:
        st.write(f"げんざいのかたち: **{st.session_state.current_shape}**")
        st.write(f"げんざいのいろ: **{st.session_state.current_color}**")
    
    st.markdown("---")
    st.write("### 親の方へ")
    st.write("""
    「ハンドレッド・シャボン・パーク」へようこそ！
    このアプリは、お子様の視覚発達と形状・色彩認識能力を高めるためのものです。
    - 100種類以上の形と色の組み合わせが、シャボンのように次々と現れます。
    - 「がめんをかえる」ボタンをタッチすると、新しい形と色の組み合わせが表示されます。
    - お子様に画面に表示された形と色を答えてもらいましょう。
    - 「こたえをみる」ボタンで正解を確認できます。
    - お子様の反応を観察し、正解を一緒に確認しましょう。
    - 1日の使用時間は10〜15分程度を目安にしてください。
    
    ハンドレッド・シャボン・パークで、楽しみながら学びましょう！
    """)

if __name__ == "__main__":
    main()