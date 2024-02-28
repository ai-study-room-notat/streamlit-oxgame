import cv2
import numpy as np
from PIL import Image
import pprint

import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title('Streamlit OX game!!')

state_holder = st.empty()


def result_chack(board):
    row_sum = np.sum(board, axis=0).astype(int)
    col_sum = np.sum(board, axis=1).astype(int)
    diag_sum = np.diag(board).sum().astype(int)
    rediag_sum = np.diag(board.T).sum().astype(int)

    print(row_sum)
    print(col_sum)
    print(diag_sum)
    print(rediag_sum)

    if 3 in row_sum:
        return 1
    elif 3 in col_sum:
        return 1
    elif 3 == diag_sum:
        return 1
    elif 3 == rediag_sum:
        return 1
    else:
        return 0


if 'board' not in st.session_state:
    st.session_state.board = np.zeros((3, 3))

if 'background_image' not in st.session_state:
    default_background_image = np.full((600, 600, 3), 255, dtype=np.uint8)
    cv2.line(default_background_image, (200, 0), (200, 600), (0, 0, 0), thickness=16)
    cv2.line(default_background_image, (400, 0), (400, 600), (0, 0, 0), thickness=16)
    cv2.line(default_background_image, (0, 200), (600, 200), (0, 0, 0), thickness=16)
    cv2.line(default_background_image, (0, 400), (600, 400), (0, 0, 0), thickness=16)
    default_background_image = Image.fromarray(default_background_image)

    st.session_state.default_background_image = default_background_image
    st.session_state.background_image = default_background_image

    print(st.session_state.default_background_image)

canvas_result = st_canvas(
    background_image=st.session_state.background_image,
    height=600,
    width=600,
)

if canvas_result is not None and canvas_result.json_data is not None:
    if len(canvas_result.json_data['objects']) > 0:
        start_point = canvas_result.json_data['objects'][-1]['path'][0][1:]
        end_point = canvas_result.json_data['objects'][-1]['path'][-1][1:]
        print(start_point, end_point)

if st.button("Submit"):
    st.write("あなたは、次をサブミットしました。", start_point, end_point)

    _s_x, _s_y = start_point
    _e_x, _e_y = end_point

    for _id_x in range(3):
        for _jd_y in range(3):
            if ((200 * _id_x) < _s_x < (200 * (_id_x + 1))) \
                    and ((200 * _id_x) < _e_x < (200 * (_id_x + 1))) \
                    and ((200 * _jd_y) < _s_y < (200 * (_jd_y + 1))) \
                    and ((200 * _jd_y) < _e_y < (200 * (_jd_y + 1))):
                st.session_state.board[_id_x, _jd_y] = 1
    print(st.session_state.board)

    # background_image = st.session_state.default_background_image
    # background_image = cv2.ellipse(
    #   np.array(background_image), [int(_) for _ in end_point],
    #   (60, 60), 0, 0, 360, color=(255, 0, 0), thickness=8)
    # st.session_state.background_image = Image.fromarray(background_image)

    print(np.where(st.session_state.board == 1))

    _xs, _ys = np.where(st.session_state.board == 1)

    background_image = st.session_state.default_background_image
    for _x, _y in zip(list(_xs), list(_ys)):
        background_image = cv2.ellipse(
            np.array(background_image), [200 * _x + 100, 200 * _y + 100],
            (60, 60), 0, 0, 360, color=(255, 0, 0), thickness=8)
    st.session_state.background_image = Image.fromarray(background_image)

    st_canvas(
        background_image=st.session_state.background_image,
        height=600,
        width=600,
    )

result = result_chack(st.session_state.board)
print('result :', result)

if result == 0:
    state_holder.write("あなたは○です。○を書いて「Submit」ボタンを押してください")
elif result == 1:
    state_holder.write("あなたの勝ちです")
