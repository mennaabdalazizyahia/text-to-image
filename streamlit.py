# from dotenv import load_dotenv, find_dotenv
# import requests
# import os
# import io 
# from PIL import Image 
# from datetime import datetime
# import streamlit as st

# load_dotenv(find_dotenv())
# HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
# def text2image(prompt: str) -> str:
#     API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
#     headers = {'Authorization': f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
#     payload = {
#         "inputs": prompt,
#     }
    
#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
#         response.raise_for_status()
        
#         image_bytes = response.content
#         image = Image.open(io.BytesIO(image_bytes))

#         timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#         filename = f"{timestamp}.jpg"
#         image.save(filename)
        
#         return filename
#     except Exception as e:
#         st.error(f"Error generating image: {e}")
#         return None

# def main():
#     st.set_page_config(
#         page_title="Text2Image Generator",
#         page_icon="🎨",
#         layout="centered"
#     )
    
#     st.title('Text-to-Image Generator')
#     st.write("Enter a prompt below to generate an image using AI")

#     with st.form(key='my_form'):
#         query = st.text_area(
#             label='Image Prompt:',
#             help="Enter a descriptive prompt for the image you want to generate",
#             key='query',
#             max_chars=100,
#             height=100
#         )

#         submit_button = st.form_submit_button(label='Generate Image')
        
#         if submit_button:
#             if not query.strip():
#                 st.warning("Please enter a prompt")
#             else:
#                 with st.spinner('Generating image... This may take a few seconds'):
#                     filename = text2image(query)
#                     if filename:
#                         st.success('Image generated successfully!')
#                         st.image(filename, caption=query, use_column_width=True)
                        
#                         with open(filename, "rb") as file:
#                             st.download_button(
#                                 label="Download Image",
#                                 data=file,
#                                 file_name=filename,
#                                 mime="image/jpeg"
#                             )

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import os
from PIL import Image
import io
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.title('Text to Image Generator')
st.write('Simple text to image conversion')

prompt = st.text_input('Enter your prompt:', 'a cat playing with ball')

if st.button('Generate Image'):
    if prompt:
        st.write('Generating image...')
        
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {'Authorization': f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}
        
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            st.image(image, caption=prompt)
            st.success('Done!')
        else:
            st.error(f'Error: {response.status_code}')
    else:
        st.warning('Please enter a prompt')