import streamlit as st
from PIL import Image
import time
import random

# Page config
st.set_page_config(page_title="Cassava Disease Predictor", layout="centered")

# Custom CSS for the interface
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
        }
        .disease-name {
            font-size: 1.5rem;
            font-weight: bold;
            color: #6a0dad;
            margin-bottom: 5px;
        }
        .causative-agent {
            font-size: 1rem;
            color: #666;
            margin-bottom: 15px;
            font-style: italic;
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
        .progress-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }
        .progress-circle {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: conic-gradient(#6a0dad 0% var(--progress), #f0f0f0 var(--progress) 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .progress-circle::before {
            content: '';
            position: absolute;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: white;
        }
        .progress-text {
            position: relative;
            font-weight: bold;
            color: #6a0dad;
        }
        .symptom-item {
            margin-bottom: 8px;
            padding-left: 15px;
            position: relative;
        }
        .symptom-item:before {
            content: "•";
            position: absolute;
            left: 0;
            color: #6a0dad;
        }
    </style>
""", unsafe_allow_html=True)

# Disease information database
disease_info = {
    "Cassava Bacterial Blight (CBB)": {
        "causative_agent": "Xanthomonas spp.",
        "symptoms": [
            "Water-soaked, angular leaf lesions that later turn brown/black",
            "Rapid wilting of shoots and young plants (especially after rain)",
            "Stem cankers, oozing of bacterial exudate from stems/cut surfaces",
            "Stunted growth and dieback in infected plants"
        ],
        "prevention": [
            "Use clean, disease-free planting cuttings from certified seed systems",
            "Remove and destroy severely infected plants",
            "Improve field sanitation (prune/wipe tools, disinfect cutting tools)",
            "Avoid planting in waterlogged or poorly drained sites",
            "Plant tolerant/resistant varieties and rotate with non-host crops"
        ],
        "confidence": 0.92
    },
    "Cassava Brown Streak Disease (CBSD)": {
        "causative_agent": "Virus",
        "symptoms": [
            "Yellowing or chlorotic patches on leaves",
            "Subtle leaf vein chlorosis",
            "Brownish streaks or necrosis on stems",
            "Necrotic brown streaks or corky rot inside storage roots"
        ],
        "prevention": [
            "Use certified virus-free planting material",
            "Remove and destroy infected plants",
            "Control whitefly vectors (Bemisia tabaci)",
            "Plant CBSD-resistant or tolerant varieties"
        ],
        "confidence": 0.88
    },
    "Cassava Green Mottle (CGM)": {
        "causative_agent": "Cassava green mottle virus",
        "symptoms": [
            "Yellow or pale green spots/patches (mottling) on young leaves",
            "Irregular chlorotic patches and leaf distortion/stunting",
            "Slow growth and weak, stunted plants from infected cuttings"
        ],
        "prevention": [
            "Use virus-free planting material",
            "Remove infected plants and burn or bury removed material",
            "Practice crop sanitation and rotation",
            "Favor healthy seed systems and surveillance"
        ],
        "confidence": 0.85
    },
    "Cassava Mosaic Disease (CMD)": {
        "causative_agent": "Cassava Mosaic Geminiviruses (CMGs)",
        "symptoms": [
            "Irregular yellow or yellow-green mosaics or mottling on leaves",
            "Leaf distortion (narrow, misshapen leaves)",
            "Stunted growth and reduced root yield",
            "Severe yield losses in young plants or when using infected cuttings"
        ],
        "prevention": [
            "Start with virus-free/clean planting material",
            "Plant CMD-resistant or tolerant cassava varieties",
            "Manage whitefly vectors through IPM",
            "Rapidly remove and destroy heavily infected plants"
        ],
        "confidence": 0.95
    },
    "Healthy": {
        "causative_agent": "N/A",
        "symptoms": [
            "Uniform green color appropriate to the cultivar",
            "Leaves fully expanded and symmetrical with normal lobing",
            "No necrotic lesions, stem cankers or exudates",
            "Roots firm, without internal necrosis"
        ],
        "prevention": [
            "Use certified disease-free cuttings from trusted suppliers",
            "Practice good field sanitation",
            "Maintain balanced soil fertility and proper spacing",
            "Routine scouting for early symptoms"
        ],
        "confidence": 0.97
    }
}

# Title
st.title("🌿 Cassava Disease Predictor")

# Create a permanent layout with columns
col1, col2 = st.columns([1, 1])

with col1:
    # Upload section with custom container
    st.markdown('<div class="custom-header">Upload Cassava Leaf Image</div>', unsafe_allow_html=True)
    
    # File uploader inside styled container
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        help="Limit 200MB per file - JPG, JPEG, PNG",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Image display section
    st.markdown('<div class="custom-header">Cassava Leaf Image</div>', unsafe_allow_html=True)
    
    # Keep everything inside this box
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Cassava Leaf", use_container_width=True)
    else:
        st.markdown('<p style="color: grey;">Image will appear here after upload</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close properly

with col2:
    # Prediction section
    st.markdown('<div class="custom-header">Prediction Result</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
    
    if uploaded_file:
        if st.button("Predict", type="primary", use_container_width=True):
            # Simulate analysis with variable time (5-15 seconds)
            analysis_time = random.randint(5, 15)
            
            # Create a progress container
            progress_placeholder = st.empty()
            
            # Simulate analysis progress
            for i in range(analysis_time):
                progress_percent = (i + 1) / analysis_time * 100
                
                # Display circular progress
                progress_placeholder.markdown(f"""
                <div class="progress-container">
                    <div class="progress-circle" style="--progress: {progress_percent}%">
                        <div class="progress-text">{int(progress_percent)}%</div>
                    </div>
                </div>
                <p style="text-align: center;">Analyzing... {i+1}/{analysis_time} seconds</p>
                """, unsafe_allow_html=True)
                
                time.sleep(1)
            
            # Clear progress indicator
            progress_placeholder.empty()
            
            # Select a random disease for demonstration
            # In a real app, this would be the actual prediction from your model
            predicted_disease = random.choice(list(disease_info.keys()))
            disease_data = disease_info[predicted_disease]
            
            # Display prediction results
            st.markdown(f'<div class="disease-name">{predicted_disease}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="causative-agent">Causative Agent: {disease_data["causative_agent"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="confidence">Confidence: {disease_data["confidence"]*100:.0f}%</div>', unsafe_allow_html=True)
            
            # Display symptoms
            st.markdown("**Typical Symptoms:**")
            for symptom in disease_data["symptoms"]:
                st.markdown(f'<div class="symptom-item">{symptom}</div>', unsafe_allow_html=True)
            
            # Display prevention measures
            st.markdown("**Prevention/Management:**")
            for measure in disease_data["prevention"]:
                st.markdown(f'<div class="symptom-item">{measure}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color: grey;">Prediction results will appear here after image upload and analysis</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close properly
