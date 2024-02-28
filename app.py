import cv2
import numpy as np
from PIL import Image

import streamlit as st
from streamlit_drawable_canvas import st_canvas


def result_check(board):
    row_sum = np.sum(board, axis=0).astype(int)
    col_sum = np.sum(board, axis=1).astype(int)
    diagonal_sum = np.diag(board).sum().astype(int)
    transpose_diagonal_sum = np.diag(board.T).sum().astype(int)

    if (3 in row_sum) or (3 in col_sum) or (3 == diagonal_sum) or (3 == transpose_diagonal_sum):
        return 1
    elif (-3 in row_sum) or (-3 in col_sum) or (-3 == diagonal_sum) or (-3 == transpose_diagonal_sum):
        return -1
    else:
        return 0


def get_default_background():
    default_background = np.full((600, 600, 3), 255, dtype=np.uint8)
    cv2.line(default_background, (200, 0), (200, 600), (0, 0, 0), thickness=16)
    cv2.line(default_background, (400, 0), (400, 600), (0, 0, 0), thickness=16)
    cv2.line(default_background, (0, 200), (600, 200), (0, 0, 0), thickness=16)
    cv2.line(default_background, (0, 400), (600, 400), (0, 0, 0), thickness=16)
    default_background = Image.fromarray(default_background)
    return default_background


def dlow_circles(background_image, _xs, _ys):
    for _x, _y in zip(list(_xs), list(_ys)):
        background_image = cv2.ellipse(
            np.array(background_image), [200 * _x + 100, 200 * _y + 100],
            (60, 60), 0, 0, 360, color=(255, 0, 0), thickness=8)
    return background_image


def get_canvas_start_end(canvas_result):
    start_point = None
    end_point = None
    if canvas_result is not None and canvas_result.json_data is not None:
        if len(canvas_result.json_data['objects']) > 0:
            start_point = canvas_result.json_data['objects'][-1]['path'][0][1:]
            end_point = canvas_result.json_data['objects'][-1]['path'][-1][1:]
    return start_point, end_point


def update_board(board, start_point, end_point, value=1):
    _s_x, _s_y = start_point
    _e_x, _e_y = end_point

    for _id_x in range(3):
        for _jd_y in range(3):
            if ((200 * _id_x) < _s_x < (200 * (_id_x + 1))) \
                    and ((200 * _id_x) < _e_x < (200 * (_id_x + 1))) \
                    and ((200 * _jd_y) < _s_y < (200 * (_jd_y + 1))) \
                    and ((200 * _jd_y) < _e_y < (200 * (_jd_y + 1))):
                board[_id_x, _jd_y] = value
    return board


def main():
    st.title('Streamlit OX game!!')

    state_holder = st.empty()

    if 'board' not in st.session_state:
        st.session_state.board = np.zeros((3, 3))

    if 'background_image' not in st.session_state:
        st.session_state.background_image = get_default_background()

    canvas_result = st_canvas(
        background_image=st.session_state.background_image,
        height=600,
        width=600,
    )

    start_point, end_point = get_canvas_start_end(canvas_result)
    print(start_point, end_point)

    if st.button("Submit") and start_point is not None and end_point is not None:
        st.write("あなたは、次をサブミットしました。", start_point, end_point)

        board = st.session_state.board
        st.session_state.board = update_board(board, start_point, end_point)
        print(st.session_state.board)

        print(np.where(st.session_state.board == 1))

        _xs, _ys = np.where(st.session_state.board == 1)

        background_image = get_default_background()
        background_image = dlow_circles(background_image, _xs, _ys)
        st.session_state.background_image = Image.fromarray(background_image)

        st_canvas(
            background_image=st.session_state.background_image,
            height=600, width=600,
        )

    result = result_check(st.session_state.board)

    if result == 0:
        state_holder.write("あなたは○です。○を書いて「Submit」ボタンを押してください")
    elif result == 1:
        state_holder.write("あなたの勝ちです")
    elif result == -1:
        state_holder.write("あなたの負けです")


if __name__ == '__main__':
    main()