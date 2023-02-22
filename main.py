import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title('Streamlit 超入門')

st.write('プログレスバーの表示')
'Start!!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteratiom {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'Done!!!'

# if st.checkbox('Show Image'):
#     img = Image.open('DSC_2466.jpg')
#     st.image(img,caption='Tomoya Hirano',use_column_width=True)

left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を入力')
if button:
    right_column.write('ここは右カラム')

expander1 = st.expander('問題１ ウサギとカメ、早かったのはどっち？')
expander1.write('カメ')
expander2 = st.expander('鹿島アントラーズと横浜Ｆマリノス、Ｊリーグで優勝が多いのはどっち？')
expander2.write('鹿島アントラーズ')
expander3 = st.expander('ネコとイヌ、漢字で書くと画数が多いのはどっち？')
expander3.write('ネコ')

# text = st.text_input('あなたの趣味を教えて下さい。')
# condition = st.sidebar.slider('あなたの今の調子は？',0, 100, 50)

# 'あなたの趣味：', text
# 'コンディション:', condition

# option = st.selectbox(
#     'あなたが好きな数字を教えて下さい。',
#     list(range(1,11))
# )



# df = pd.DataFrame(
#     np.random.rand(100, 2)/[50, 50] +[35.69,139.70],
#     columns=['lat', 'lon']
# )
# # st.table(df.style.highlight_max(axis=0))
# st.map(df)
