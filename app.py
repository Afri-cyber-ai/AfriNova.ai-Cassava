import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import gdown
import os
import time

# -------------------------------
# Custom CSS for Professional Styling
# -------------------------------
st.markdown("""
<style>
    /* Main purple theme */
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
    .disease-info {
        background-color: #f0e6ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #9370db;
        margin-top: 1rem;
    }
    .confidence-bar {
        background-color: #e6e6fa;
        height: 1.5rem;
        border-radius: 0.3rem;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .confidence-fill {
        background-color: #6a0dad;
        height: 100%;
        border-radius: 0.3rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 0.5rem;
        color: white;
        font-weight: 500;
        font-size: 0.8rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #6a0dad;
        font-size: 0.9rem;
    }
    .consult-button {
        background-color: #6a0dad;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
        font-weight: 600;
    }
    /* Hide unnecessary Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 1. Load Model from Google Drive with Verification
# -------------------------------

MODEL_PATH = "cassava_model.keras"
FILE_ID = "1Z_ALef3S-hYkyzqicsoRCYrv765d_tqq"  # Your Google Drive file ID

@st.cache_resource
def load_model():
    # Check if file exists and is valid
    if os.path.exists(MODEL_PATH):
        try:
            # Try loading to verify it's a valid model file
            model = tf.keras.models.load_model(MODEL_PATH)
            return model
        except:
            st.warning("Local model file is corrupted. Downloading a fresh copy...")
            os.remove(MODEL_PATH)
    
    # Download the file with progress indicator
    try:
        with st.spinner("Downloading model from Google Drive..."):
            url = f"https://drive.google.com/uc?id={FILE_ID}"
            gdown.download(url, MODEL_PATH, quiet=False)
            
        # Verify the file was downloaded
        if not os.path.exists(MODEL_PATH):
            st.error("Download failed - file not found after download attempt")
            return None
            
        # Verify file size (basic check)
        file_size = os.path.getsize(MODEL_PATH)
        if file_size < 1024:  # Less than 1KB is probably not a valid model
            st.error(f"Downloaded file is too small ({file_size} bytes). Probably an error page.")
            os.remove(MODEL_PATH)
            return None
            
        # Try loading the model
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
        
    except Exception as e:
        st.error(f"Error downloading or loading model: {str(e)}")
        # Clean up potentially corrupted file
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return None

# Load the model
model = load_model()

# -------------------------------
# 2. Class Names and Disease Information
# -------------------------------

CLASS_NAMES = [
    "Cassava Bacterial Blight",
    "Cassava Brown Streak Disease",
    "Cassava Green Mottle",
    "Cassava Mosaic Virus",
    "Healthy"
]

# Disease information database
DISEASE_INFO = {
    "Cassava Bacterial Blight": {
        "symptoms": "Water-soaked angular leaf spots, blight, wilting, stem cankers, and dieback. Leaves may show yellowing and necrosis.",
        "prevention": "Use disease-free planting materials, practice crop rotation, avoid waterlogged conditions, and remove infected plants.",
        "consult_link": "tel:+1234567890"
    },
    "Cassava Brown Streak Disease": {
        "symptoms": "Yellow chlorotic patterns along veins, brown necrotic streaks on stems, root constriction, and rot.",
        "prevention": "Plant resistant varieties, control whitefly vectors, use clean planting materials, and rogue infected plants.",
        "consult_link": "tel:+1234567890"
    },
    "Cassava Green Mottle": {
        "symptoms": "Light and dark green mosaic patterns on leaves, leaf distortion, stunting, and reduced root yield.",
        "prevention": "Use virus-free planting materials, control insect vectors, practice field sanitation, and remove weeds.",
        "consult_link": "tel:+1234567890"
    },
    "Cassava Mosaic Virus": {
        "symptoms": "Leaf mosaic patterns, leaf distortion, reduced leaf size, stunted growth, and tuber yield reduction.",
        "prevention": "Plant resistant varieties, use virus-free cuttings, control whitefly populations, and practice rogueing.",
        "consult_link": "tel:+1234567890"
    },
    "Healthy": {
        "symptoms": "No visible signs of disease. Leaves are uniformly green with normal shape and size.",
        "prevention": "Maintain good agricultural practices, monitor regularly for early signs of disease, and ensure proper nutrition.",
        "consult_link": "tel:+1234567890"
    }
}

# -------------------------------
# 3. Enhanced Streamlit Interface
# -------------------------------

st.set_page_config(
    page_title="AgriNova.ai - Cassava Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">AgriNova.ai</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Intelligent Crop Disease Detection</h2>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="agrinova-badge">Cassava Disease Classifier</div>', unsafe_allow_html=True)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Main content
if model is None:
    st.error("Model loading failed. Please check the connection and try again.")
    st.info("""
    **Troubleshooting steps:**
    - Check your internet connection
    - Verify the model file is accessible
    - Refresh the page to try again
    """)
else:
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Cassava Leaf Image")
        st.markdown("Upload a clear image of a cassava leaf for disease analysis")
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            # Show uploaded image with a border
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Cassava Leaf", use_container_width=True)
            
            if st.button("🔍 Analyze Image", use_container_width=True, type="primary"):
                # Create a progress bar for the 15-second analysis
                progress_text = "Analysis in progress. Please wait..."
                progress_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.15)  # 15 seconds total for the progress bar
                    progress_bar.progress(percent_complete + 1, text=progress_text)
                
                # Actual prediction (this happens quickly but we've already shown the progress)
                with st.spinner("Finalizing analysis..."):
                    # Preprocess image
                    img = image.resize((224, 224))
                    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

                    # Run prediction
                    try:
                        preds = model.predict(img_array)
                        confidence = np.max(preds) * 100
                        predicted_class = CLASS_NAMES[np.argmax(preds)]
                        
                        # Store results in session state
                        st.session_state.prediction = {
                            "class": predicted_class,
                            "confidence": confidence,
                            "all_predictions": preds[0]
                        }
                    except Exception as e:
                        st.error(f"Error during prediction: {str(e)}")
                
                progress_bar.empty()
                st.success("Analysis complete!")
    
    # Show results in the left column if available
    if uploaded_file and "prediction" in st.session_state:
        with col1:
            pred = st.session_state.prediction
            
            st.markdown("### 📊 Analysis Results")
            
            # Results card
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            
            if pred["class"] == "Healthy":
                st.success(f"**Status:** {pred['class']} 🟢")
            else:
                st.error(f"**Status:** {pred['class']} 🔴")
                
            st.metric("Confidence Level", f"{pred['confidence']:.2f}%")
            
            st.markdown("**Detailed Confidence Scores:**")
            
            # Show confidence bars for all classes
            for i, class_name in enumerate(CLASS_NAMES):
                conf_percent = pred["all_predictions"][i] * 100
                st.markdown(f"**{class_name}**")
                st.markdown(
                    f'<div class="confidence-bar">'
                    f'<div class="confidence-fill" style="width: {conf_percent}%">'
                    f'{conf_percent:.2f}%</div></div>',
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Show disease information in the right column if prediction is available
    if uploaded_file and "prediction" in st.session_state:
        with col2:
            pred = st.session_state.prediction
            disease_name = pred["class"]
            disease_data = DISEASE_INFO[disease_name]
            
            st.markdown("### 🌱 Disease Information")
            st.markdown(f'#### {disease_name}')
            
            # Disease info card
            st.markdown('<div class="disease-info">', unsafe_allow_html=True)
            
            st.markdown("**Symptoms:**")
            st.info(disease_data["symptoms"])
            
            st.markdown("**Prevention Measures:**")
            st.success(disease_data["prevention"])
            
            st.markdown("**Recommendation:**")
            if disease_name == "Healthy":
                st.markdown("Your plant appears healthy. Continue monitoring and maintain good agricultural practices.")
            else:
                st.markdown("We recommend consulting with an agricultural expert for specific treatment options.")
            
            # Consult button
            st.markdown(
                f'<a href="{disease_data["consult_link"]}" class="consult-button">📞 Consult an Expert</a>',
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
    elif uploaded_file:
        with col2:
            st.info("👈 Click 'Analyze Image' to get detailed disease information")
            
    # Add some information about the system
    st.markdown("---")
    st.markdown("### ℹ️ About This System")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown("**Technology**")
        st.markdown("- Deep Learning AI")
        st.markdown("- Computer Vision")
        st.markdown("- TensorFlow Backend")
        
    with info_col2:
        st.markdown("**Capabilities**")
        st.markdown("- 5 Disease Classifications")
        st.markdown("- Real-time Analysis")
        st.markdown("- Confidence Scoring")
        
    with info_col3:
        st.markdown("**Benefits**")
        st.markdown("- Early Disease Detection")
        st.markdown("- Reduced Crop Loss")
        st.markdown("- Increased Yield")

# Footer
st.markdown("---")
st.markdown('<div class="footer">AgriNova.ai • AI-Powered Agricultural Solutions • © 2023</div>', unsafe_allow_html=True)
