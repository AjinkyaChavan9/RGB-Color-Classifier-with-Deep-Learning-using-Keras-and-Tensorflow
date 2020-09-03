# -*- coding: utf-8 -*-
import streamlit as st
import PIL
from PIL import Image, ImageOps
from color_classifier import predict_color #importing predicting color function

# display image with the size and rgb color
def display_image():
    img = Image.new("RGB", (200, 200), color=(Red,Green,Blue))
    img = ImageOps.expand(img, border=1, fill='black')  # border to the img
    st.image(img, caption='RGB Color')

if __name__ == "__main__":
    hide_st_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.sidebar.title("About")
    st.sidebar.info(
            "**RGB Color Classifier** can Predict upto 11 Distinct Color Classes based on the RGB input by User from the sliders\n\n"
            "The 11 Classes are *Red, Green, Blue, Yellow, Orange, Pink, Purple, Brown, Grey, Black and White*\n\n"
            "This app is created and maintained by [Ajinkya Chavan](https://github.com/AjinkyaChavan9)\n\n"
            "Check the [Source Code] (https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow)"
        )
    st.sidebar.title("Contribute")
    st.sidebar.info(
        "You are very **Welcome** to contribute your awesome comments, questions or suggestions as [issues](https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow/issues) "
        "or [pull requests](https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow/pulls) to the [source code](https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow)"
    )
    #st.title("RGB Color Classifier")
    Title_html = """
    <style>
        .title h1{
          user-select: none;
          font-size: 43px;
          color: white;
          background: repeating-linear-gradient(-45deg, red 0%, yellow 7.14%, rgb(0,255,0) 14.28%, rgb(0,255,255) 21.4%, cyan 28.56%, blue 35.7%, magenta 42.84%, red 50%);
          background-size: 600vw 600vw;
          -webkit-text-fill-color: transparent;
          -webkit-background-clip: text;
          animation: slide 10s linear infinite forwards;
        }
        @keyframes slide {
          0%{
            background-position-x: 0%;
          }
          100%{
            background-position-x: 600vw;
          }
        }
    </style> 
    
    <div class="title">
        <h1>RGB Color Classifier</h1>
    </div>
    """
    st.markdown(Title_html, unsafe_allow_html=True) #Title rendering
    #st.header("Select RGB values")

    Red = st.slider( label="RED value: ", min_value=0, max_value=255, value=0, key="red")
    Green = st.slider(label="GREEN value: ", min_value=0, max_value=255, value=0, key="green")
    Blue = st.slider(label="BLUE value: ", min_value=0, max_value=255, value=0, key="blue")

    st.write('Red: {}, Green: {}, Blue: {}'.format(Red, Green, Blue))
    display_image()
    result = ""
    if st.button("Predict"):
        result = predict_color(Red, Green, Blue)
        st.success('The Color is {}!'.format(result))


