import streamlit as st
from PIL import Image
import base64
import time
import random

# Page config
st.set_page_config(page_title="Cassava Disease Predictor", layout="centered")

# Custom CSS for permanent layout with better image containment
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
            min-height: 350px;
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
            margin-bottom: 5px;
        }
        .causative {
            font-size: 1rem;
            font-style: italic;
            color: #444;
            margin-bottom: 10px;
        }
        .confidence {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c662d;
        }
        .custom-header {
            color: #6a0dad;
            border-bottom: 2px solid #6a0dad;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .analyzing {
            text-align: center;
            font-size: 1.1rem;
            color: #6a0dad;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Disease info dictionary
disease_info = {
    "Cassava Mosaic Disease": {
        "agent": "Cassava Mosaic Geminiviruses (CMGs)",
        "about": "Distinct yellow mosaics and leaf distortion caused by CMGs. "
                 "Major yield reducer in cassava, transmitted by whiteflies.",
        "prevention": [
            "Use virus-free planting material",
            "Plant resistant varieties",
            "Remove infected plants quickly",
            "Manage whitefly vectors via IPM"
        ]
    },
    "Cassava Brown Streak Disease": {
        "agent": "Viruses (transmitted by Bemisia tabaci)",
        "about": "Causes root necrosis and economic loss. Streaks on stems and chlorotic patches on leaves.",
        "prevention": [
            "Use certified clean planting material",
            "Destroy infected plants",
            "Control whitefly populations",
            "Grow resistant varieties"
        ]
    },
    "Cassava Bacterial Blight": {
        "agent": "Xanthomonas spp.",
        "about": "Angular water-soaked lesions, stem cankers, wilting and dieback after rains.",
        "prevention": [
            "Use clean planting cuttings",
            "Remove and destroy infected plants",
            "Disinfect tools",
            "Plant tolerant varieties"
        ]
    },
    "Cassava Green Mottle": {
        "agent": "Cassava Green Mottle Virus",
        "about": "Mottled yellow-green patches and leaf distortion. Plants become stunted with poor roots.",
        "prevention": [
            "Plant virus-free cuttings",
            "Rogue and burn infected plants",
            "Practice crop rotation and sanitation"
        ]
    },
    "Healthy": {
        "agent": "None",
        "about": "Uniform green, symmetrical leaves without necrosis, streaks or distortion.",
        "prevention": [
            "Use disease-free cuttings",
            "Maintain good field sanitation",
            "Ensure balanced soil fertility",
            "Scout fields regularly"
        ]
    }
}

# Title
st.title("🌿 Cassava Disease Predictor")

# Create layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="custom-header">Upload Cassava Leaf Image</div>', unsafe_allow_html=True)
    
    upload_container = st.container()
    with upload_container:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag and drop file here",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=False,
            help="Limit 200MB per file - JPG, JPEG, PNG",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-header">Cassava Leaf Image</div>', unsafe_allow_html=True)
    
    image_container = st.container()
    with image_container:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        if uploaded_file:
            image = Image.open(uploaded_file)
            import io
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'<img src="data:image/png;base64,{img_str}" style="max-width:100%; height:auto;">', 
                       unsafe_allow_html=True)
            st.markdown('<p style="margin-top:10px; color:#666;">Uploaded Cassava Leaf</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: grey; margin: 40px 0;">Image will appear here after upload</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-header">Prediction Result</div>', unsafe_allow_html=True)
    prediction_container = st.container()
    with prediction_container:
        st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
        
        if uploaded_file:
            if st.button("Predict", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing..."):
                    duration = random.randint(5, 15)  # vary between 5–15 sec
                    progress_text = st.empty()
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(duration / 100)
                        progress_bar.progress(i + 1)
                        progress_text.markdown('<div class="analyzing">Analyzing cassava leaf image...</div>', unsafe_allow_html=True)
                
                # Example fixed output (replace with model prediction)
                predicted = "Cassava Mosaic Disease"
                confidence = "92%"
                data = disease_info[predicted]
                
                st.markdown(f'<div class="disease-name">{predicted}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="causative">Causative agent: {data["agent"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="confidence">Confidence: {confidence}</div>', unsafe_allow_html=True)
                
                st.markdown("**About this disease**")
                st.write(data["about"])
                
                st.markdown("**Prevention / Management**")
                for tip in data["prevention"]:
                    st.write(f"- {tip}")
        else:
            st.markdown('<p style="color: grey; margin: 40px 0;">Results will appear here after prediction</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
