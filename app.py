import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import gdown
import os
import time
import random

# -------------------------------
# Custom CSS for Professional Styling
# -------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #6a0dad;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #8a2be2;
        font-weight: 400;
        margin-top: 0;
    }
    .agrinova-badge {
        background-color: #6a0dad;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: inline-block;
    }
    .stButton>button {
        background-color: #6a0dad;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #8a2be2;
        color: white;
    }
    .prediction-card {
        background-color: #f8f5ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #6a0dad;
        margin-top: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #6a0dad;
        font-size: 0.9rem;
    }
    .analyzing {
        text-align: center;
        font-size: 1.1rem;
        color: #6a0dad;
        margin-bottom: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 1. Load Model
# -------------------------------
MODEL_PATH = "cassava_model.keras"
FILE_ID = "1BhoZx--RL8A6fgLbLG6uxOf7WR_VOjVq"  

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return tf.keras.models.load_model(MODEL_PATH)
        except:
            os.remove(MODEL_PATH)
    
    try:
        with st.spinner("Downloading model from Google Drive..."):
            url = f"https://drive.google.com/uc?id={FILE_ID}"
            gdown.download(url, MODEL_PATH, quiet=False)
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        st.error(f"Error downloading/loading model: {str(e)}")
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return None

model = load_model()

# -------------------------------
# 2. Class Names + Disease Info
# -------------------------------
CLASS_NAMES = [
    "Cassava Bacterial Blight",
    "Cassava Brown Streak Disease",
    "Cassava Green Mottle",
    "Cassava Mosaic Virus",
    "Healthy"
]

DISEASE_INFO = {
    "Cassava Bacterial Blight": {
        "agent": "Xanthomonas spp.",
        "about": "Water-soaked angular lesions, stem cankers, wilting and dieback after rains.",
        "prevention": [
            "Use clean planting cuttings",
            "Remove and destroy infected plants",
            "Disinfect tools between use",
            "Plant tolerant/resistant varieties"
        ]
    },
    "Cassava Brown Streak Disease": {
        "agent": "Viruses (transmitted by Bemisia tabaci)",
        "about": "Yellow patches, brown streaks on stems, root necrosis causing yield loss.",
        "prevention": [
            "Use certified clean planting material",
            "Destroy infected plants",
            "Control whitefly populations",
            "Grow resistant varieties"
        ]
    },
    "Cassava Green Mottle": {
        "agent": "Cassava green mottle virus",
        "about": "Leaves show mottled yellow-green patches and distortion; plants become stunted.",
        "prevention": [
            "Use virus-free planting material",
            "Rogue and destroy infected plants",
            "Maintain field sanitation and crop rotation"
        ]
    },
    "Cassava Mosaic Virus": {
        "agent": "Cassava Mosaic Geminiviruses (CMGs)",
        "about": "Distinct yellow-green mosaics, leaf distortion, reduced yield. Spread by whiteflies.",
        "prevention": [
            "Use virus-free planting cuttings",
            "Plant resistant/tolerant varieties",
            "Remove infected plants quickly",
            "Manage whitefly vectors (IPM)"
        ]
    },
    "Healthy": {
        "agent": "None",
        "about": "Uniform green, symmetrical leaves without lesions, streaks or distortion.",
        "prevention": [
            "Continue current practices",
            "Scout fields regularly",
            "Maintain soil fertility and sanitation"
        ]
    }
}

# -------------------------------
# 3. Streamlit Interface
# -------------------------------
st.set_page_config(
    page_title="AgriNova.ai - Cassava Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">AgriNova.ai</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Intelligent Crop Disease Detection</h2>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="agrinova-badge">Cassava Disease Classifier</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if model is None:
    st.error("Model loading failed. Please try again.")
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📤 Upload Cassava Leaf Image")
        uploaded_file = st.file_uploader(
            "Choose an image file", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
        )
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Cassava Leaf", use_container_width=True)

            if st.button("🔍 Analyze Image", use_container_width=True, type="primary"):
                with st.spinner("🔄 Analyzing..."):
                    duration = random.randint(5, 15)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    for i in range(100):
                        time.sleep(duration / 100)
                        progress_bar.progress(i + 1)
                        status_text.markdown('<div class="analyzing">Analyzing cassava leaf image...</div>', unsafe_allow_html=True)

                    try:
                        img = image.resize((224, 224))
                        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
                        preds = model.predict(img_array)
                        confidence = np.max(preds) * 100
                        predicted_class = CLASS_NAMES[np.argmax(preds)]
                        st.session_state.prediction = {
                            "class": predicted_class,
                            "confidence": confidence,
                        }
                    except Exception as e:
                        st.error(f"Error during prediction: {str(e)}")

    with col2:
        if uploaded_file and "prediction" in st.session_state:
            pred = st.session_state.prediction
            st.markdown("### 📊 Analysis Results")
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)

            if pred["class"] == "Healthy":
                st.success(f"**Status:** {pred['class']} 🟢")
            else:
                st.error(f"**Status:** {pred['class']} 🔴")

            # ✅ Show only one confidence score
            st.metric("Confidence Level", f"{pred['confidence']:.2f}%")

            # ✅ Show causative agent
            st.markdown(f"**Causative Agent:** {DISEASE_INFO[pred['class']]['agent']}")

            # ✅ Disease description
            st.markdown("**About this disease**")
            st.write(DISEASE_INFO[pred['class']]['about'])

            st.markdown("**Prevention / Management**")
            for tip in DISEASE_INFO[pred['class']]['prevention']:
                st.write(f"- {tip}")

            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👈 Upload an image and click 'Analyze' to get results")

# Footer
st.markdown("---")
st.markdown('<div class="footer">AgriNova.ai • AI-Powered Agricultural Solutions • © 2025</div>', unsafe_allow_html=True)
