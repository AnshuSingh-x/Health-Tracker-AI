import streamlit as st
import google.generativeai as genai 
import os
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Health Tracker AI")
st.header("Health Tracker AI")
uploaded_file=st.file_uploader("Click the photo of your food and upload it here..",
                                type=["jpg","jpeg","png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="uploaded image.",use_container_width=True)

submit= st.button("Track total calories")

input_prompt="""
you are an expert in nutritionist where you need to see the food items from the image
and calulate the total calories, also provide the details of every food items with calorie intake
in below format

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally you can also mention whether the food is healthy or not and also mention the percentage
split of the ratio of carbohydrates,fats,fiber,suger and other important things, also make it short
and easay to read and aslo don"t talk about doctors advisory note, dont give important note

"""
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("Here is the breakdown of you food")
    st.write(response)