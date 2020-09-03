FROM continuumio/miniconda3:4.8.2

WORKDIR /usr/RGBapp

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /RGB_Color_Classifier_app /usr/RGBapp

CMD streamlit run /usr/RGBapp/RGB_web_app.py



