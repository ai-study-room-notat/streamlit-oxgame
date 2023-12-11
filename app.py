import cv2
import numpy as np
from PIL import Image
import pprint

import streamlit as st
from streamlit_drawable_canvas import st_canvas


st.title('Streamlit OX game!!')

st.write("あなたは○です。○を書いて「Submit」ボタンを押してください")


if 'background_image' not in st.session_state:
  DEFAULT_BACKGROUND_IMAGE = np.full((600, 600, 3), 255, dtype=np.uint8)
  cv2.line(DEFAULT_BACKGROUND_IMAGE, (200, 0), (200, 600), (0, 0, 0), thickness=16)
  cv2.line(DEFAULT_BACKGROUND_IMAGE, (400, 0), (400, 600), (0, 0, 0), thickness=16)
  cv2.line(DEFAULT_BACKGROUND_IMAGE, (0, 200), (600, 200), (0, 0, 0), thickness=16)
  cv2.line(DEFAULT_BACKGROUND_IMAGE, (0, 400), (600, 400), (0, 0, 0), thickness=16)
  DEFAULT_BACKGROUND_IMAGE = Image.fromarray(DEFAULT_BACKGROUND_IMAGE)
  
  st.session_state.default_background_image = DEFAULT_BACKGROUND_IMAGE
  st.session_state.background_image = DEFAULT_BACKGROUND_IMAGE

canvas_result = st_canvas(
  background_image=st.session_state.background_image
)

if canvas_result is not None and canvas_result.json_data is not None:
  if len(canvas_result.json_data['objects']) > 0:
    start_point = canvas_result.json_data['objects'][-1]['path'][0][1:]
    end_point = canvas_result.json_data['objects'][-1]['path'][-1][1:]
    print(start_point, end_point)    
  
if st.button("Submit"):
  st.write("あなたは、次をサブミットしました。", end_point)
  background_image = st.session_state.default_background_image
  background_image = cv2.ellipse(np.array(background_image), [int(_) for _ in end_point], (60, 60), 0, 0, 360, color=(255, 0, 0), thickness=8)
  st.session_state.background_image = Image.fromarray(background_image)
