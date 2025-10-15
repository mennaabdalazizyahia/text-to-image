import streamlit as st
import requests
import os
from PIL import Image
import io
from datetime import datetime

st.set_page_config(
    page_title="Text to Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title('🎨 Text to Image Generator')
st.write('Transform your text into amazing images using AI!')

with st.sidebar:
    st.header("ℹ️ Instructions")
    st.write("""
    1. Enter your image description
    2. Click Generate Image
    3. Wait for the magic! ✨
    
    **Note:** First generation may take 20-30 seconds as the model loads.
    """)
    
    st.header("⚙️ Settings")
    model_option = st.selectbox(
        "Choose Model",
        [
            "stabilityai/stable-diffusion-xl-base-1.0",
            "runwayml/stable-diffusion-v1-5"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.header("🔑 API Configuration")

api_source = st.sidebar.radio(
    "API Token Source",
    ["Use Streamlit Secrets", "Enter Manually"]
)

if api_source == "Use Streamlit Secrets":
    if 'HUGGINGFACEHUB_API_TOKEN' in st.secrets:
        api_token = st.secrets['HUGGINGFACEHUB_API_TOKEN']
        st.sidebar.success("✅ API Token loaded from secrets")
    else:
        st.sidebar.error("❌ No API token found in secrets")
        st.sidebar.info("""
        Add to your Streamlit Cloud secrets:
        ```
        HUGGINGFACEHUB_API_TOKEN=your_token_here
        ```
        """)
        api_token = None
else:
    api_token = st.sidebar.text_input("Enter HuggingFace Token", type="password")

prompt = st.text_area(
    '**Describe your image:**',
    'a cute cat playing with a red ball in the garden, cartoon style',
    height=120,
    placeholder="Be creative! Describe the image you want to generate..."
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button('🚀 Generate Image', type='primary', use_container_width=True)

if generate_btn:
    if not prompt.strip():
        st.warning('⚠️ Please enter a prompt description')
        st.stop()
    
    if not api_token:
        st.error("🔐 Please configure your HuggingFace API Token in the sidebar")
        st.stop()
    
    with st.spinner('🎨 Creating your masterpiece... This may take 20-30 seconds for the first time.'):
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model_option}"
            headers = {'Authorization': f"Bearer {api_token}"}
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f"Generating... {i+1}%")
            
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                
                st.subheader("🎉 Your Generated Image")
                st.image(image, caption=f"**{prompt}**", use_column_width=True)
                
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                
                download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
                with download_col2:
                    st.download_button(
                        label="📥 Download PNG Image",
                        data=img_bytes.getvalue(),
                        file_name=f"ai_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                st.success('✅ Image generated successfully!')
                
            elif response.status_code == 503:
                st.warning("⏳ Model is loading, please try again in 30 seconds...")
                st.info("This usually happens when the model hasn't been used recently.")
            elif response.status_code == 401:
                st.error("🔐 Invalid API Token. Please check your HuggingFace token.")
            else:
                st.error(f'❌ API Error {response.status_code}')
                st.code(response.text[:200] + "..." if len(response.text) > 200 else response.text)
                
        except requests.exceptions.RequestException as e:
            st.error(f'🌐 Network error: Please check your internet connection')
            st.debug(f"Error details: {str(e)}")
        except Exception as e:
            st.error(f'❌ Unexpected error occurred')
            st.debug(f"Error details: {str(e)}")
    
    status_text.empty()
    progress_bar.empty()

with st.expander("💡 Tips for better results"):
    st.write("""
    - **Be specific**: "a red car" vs "a shiny red sports car on a mountain road at sunset"
    - **Include style**: "watercolor painting", "digital art", "photorealistic"
    - **Add details**: lighting, colors, background, emotions
    - **Example prompts**:
        - "a majestic dragon flying over a medieval castle, fantasy art"
        - "a cozy coffee shop in paris, watercolor style"
        - "an astronaut riding a horse on mars, photorealistic"
    """)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Powered by 🤗 Hugging Face | Built with 🎈 Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)

