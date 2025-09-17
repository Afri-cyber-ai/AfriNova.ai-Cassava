import streamlit as st
from PIL import Image
import base64
import time
import random
import io

# Page config
st.set_page_config(page_title="Cassava Disease Predictor", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #fafafa;
        }
        .stButton>button {
            background-color: #6a0dad;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #580a9e;
        }
        .prediction-container {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            min-height: 300px;
            overflow: hidden;
        }
        .upload-container {
            background-color: #f8f8f8;
            padding: 20px;
            border-radius: 10px;
            border: 2px dashed #6a0dad;
            margin-bottom: 20px;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .image-container {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin: 20px 0;
            text-align: center;
            min-height: 250px;
            overflow: hidden;
        }
        .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }
        .disease-name {
            font-size: 1.5rem;
            font-weight: bold;
            color: #6a0dad;
            margin-bottom: 10px;
        }
        .confidence {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c662d;
        }
        .causative-agent {
            font-size: 1rem;
            font-style: italic;
            margin-bottom: 15px;
            color: #444;
        }
        .custom-header {
            color: #6a0dad;
            border-bottom: 2px solid #6a0dad;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Disease information dictionary
disease_info = {
    "Cassava Bacterial Blight (CBB)": {
        "agent": "Xanthomonas spp.",
        "about": """Water-soaked, angular leaf lesions that later turn brown/black and may merge into large blighted areas.
        Rapid wilting of shoots and young plants (especially after rain). Stem cankers, oozing of bacterial exudate, stunted growth and dieback.
        **Prevention:** Use clean cuttings, destroy infected plants, disinfect tools, avoid waterlogged soils, plant resistant varieties."""
    },
    "Cassava Brown Streak Disease (CBSD)": {
        "agent": "Virus (transmitted by Bemisia tabaci whiteflies)",
        "about": """Yellowing or chlorotic patches on leaves, brown streaks on stems, and necrotic corky rot in storage roots (major yield loss).
        **Prevention:** Use certified clean cuttings, remove infected plants, control whiteflies, plant tolerant varieties."""
    },
    "Cassava Green Mottle (CGM)": {
        "agent": "Cassava green mottle virus",
        "about": """Young leaves show yellow or pale green mottling, irregular chlorotic patches, and leaf distortion/stunting.
        Plants grow slowly with poor-quality roots. **Prevention:** Use virus-free cuttings, rogue infected plants, practice sanitation and crop rotation."""
    },
    "Cassava Mosaic Disease (CMD)": {
        "agent": "Cassava Mosaic Geminiviruses (CMGs)",
        "about": """Irregular yellow-green mosaics on leaves, distortion, stunted growth, and heavy yield loss if severe.
        **Prevention:** Start with virus-free cuttings, plant resistant varieties, manage whiteflies, and destroy heavily infected plants quickly."""
    },
    "Healthy": {
        "agent": "None",
        "about": """Uniform green leaves with no spots, streaks, distortion, or necrosis. Roots are firm and healthy.
        **Practice:** Use clean cuttings, good field sanitation, balanced soil fertility, proper spacing, and routine scouting."""
    }
}

# Title
st.title("🌿 Cassava Disease Predictor")

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="custom-header">Upload Cassava Leaf Image</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drag and drop file here",
                                         type=["jpg", "jpeg", "png"],
                                         accept_multiple_files=False,
                                         label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-header">Cassava Leaf Image</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        if uploaded_file:
            image = Image.open(uploaded_file)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'<img src="data:image/png;base64,{img_str}" style="max-width:100%; height:auto;">',
                        unsafe_allow_html=True)
            st.markdown('<p style="margin-top:10px; color:#666;">Uploaded Cassava Leaf</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: grey; margin: 40px 0;">Image will appear here after upload</p>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-header">Prediction Result</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="prediction-container">', unsafe_allow_html=True)

        if uploaded_file:
            if st.button("Predict", use_container_width=True):
                # Simulate analysis
                with st.spinner("🔄 Analyzing leaf image..."):
                    analysis_time = random.randint(5, 15)
                    time.sleep(analysis_time)

                # Fake prediction (for demo)
                predicted = "Cassava Mosaic Disease (CMD)"
                confidence = random.randint(80, 97)

                st.markdown(f'<div class="disease-name">{predicted}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="confidence">Confidence: {confidence}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="causative-agent">Causative agent: {disease_info[predicted]["agent"]}</div>',
                            unsafe_allow_html=True)

                st.markdown("**About the disease**")
                st.write(disease_info[predicted]["about"])

        else:
            st.markdown('<p style="color: grey; margin: 40px 0;">Prediction results will appear here after upload and analysis</p>',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
