import streamlit as st
import pandas as pd
import json
import os
import time
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Import backend modules
try:
    from src.prediction import predict_url, get_model_metrics, validate_url
    from src.feature_extraction import FEATURE_NAMES
    BACKEND_AVAILABLE = True
except ImportError as e:
    BACKEND_AVAILABLE = False
    IMPORT_ERROR = str(e)

# --- CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="Phishing URL Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #0a0a0a;
        color: #e6edf3;
    }
    
    /* Headers & Text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    p {
        color: #c9d1d9;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #233554;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        color: #64ffda !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }
    
    /* Cards */
    .st-emotion-cache-1r6slb0 {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
    }
    
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #64ffda;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #8b949e;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #238636;
        color: white;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 6px;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        border-color: #8b949e;
    }
    
    /* Status Badges */
    .badge-legitimate {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #2ea043;
        display: inline-block;
        margin-bottom: 15px;
        font-size: 1.5rem;
    }
    .badge-suspicious {
        background-color: rgba(210, 153, 34, 0.15);
        color: #d29922;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #d29922;
        display: inline-block;
        margin-bottom: 15px;
        font-size: 1.5rem;
    }
    .badge-phishing {
        background-color: rgba(248, 81, 73, 0.15);
        color: #ff7b72;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #f85149;
        display: inline-block;
        margin-bottom: 15px;
        font-size: 1.5rem;
    }
    
    /* Alert Boxes */
    .alert-redflag {
        background-color: rgba(248, 81, 73, 0.1);
        border-left: 4px solid #f85149;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
        color: #ff7b72;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
@st.cache_data
def get_metrics():
    if not BACKEND_AVAILABLE:
        return None
    try:
        return get_model_metrics()
    except Exception:
        return None

def main():
    apply_custom_css()
    
    # --- 1. HERO HEADER ---
    st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">🛡️ Phishing URL Detection System</h1>
            <p style="font-size: 1.2rem; margin-top: 10px;">Advanced Machine Learning for Cyber Threat Intelligence</p>
        </div>
    """, unsafe_allow_html=True)

    # Check backend
    if not BACKEND_AVAILABLE:
        st.error(f"Backend modules not found. Error: {IMPORT_ERROR}")
        st.info("Make sure src.prediction and src.feature_extraction are properly structured.")
        st.stop()

    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/shield.png", width=80)
        st.title("About Project")
        st.info(
            "This dashboard uses a trained Machine Learning model to detect whether a URL "
            "is Legitimate, Suspicious, or Phishing based on lexical and structural features."
        )
        
        st.markdown("### Dataset Info")
        st.markdown("- **Source**: Synthetic (self-generated)")
        st.markdown("- **Features**: 16 Lexical features")
        
        st.markdown("### Sample URLs")
        st.markdown("Click to copy and test:")
        st.code("https://www.github.com/login", language="text")
        st.code("http://secure-update-paypal.com-verification.info/login", language="text")
        st.code("http://bit.ly/2v9aK8c", language="text")
        
        st.markdown("---")
        st.caption("Developed for Cybersecurity Analysis")

    # --- 2. URL ANALYSIS SECTION ---
    st.header("🔍 URL Analysis Engine")
    
    url_input = st.text_input("Enter URL to analyze:", placeholder="https://example.com", key="url_input")
    
    if st.button("Analyze URL", use_container_width=True):
        if not url_input:
            st.warning("Please enter a URL to analyze.")
        else:
            is_valid, cleaned_url, error_msg = validate_url(url_input)
            
            if not is_valid:
                st.error(f"Invalid URL: {error_msg}")
            else:
                with st.spinner("Analyzing threat signatures..."):
                    time.sleep(0.5)  # Slight delay for effect
                    try:
                        result = predict_url(cleaned_url)
                        
                        # Display Results
                        st.markdown("---")
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.subheader("Classification Result")
                            cls_lower = result['classification'].lower()
                            
                            if cls_lower == 'legitimate':
                                st.markdown(f'<div class="badge-legitimate">✅ {result["classification"]}</div>', unsafe_allow_html=True)
                            elif cls_lower == 'suspicious':
                                st.markdown(f'<div class="badge-suspicious">⚠️ {result["classification"]}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="badge-phishing">🚨 {result["classification"]}</div>', unsafe_allow_html=True)
                            
                            st.markdown(f"**Confidence Score:** {result['confidence']:.1f}%")
                            st.progress(result['confidence'] / 100.0)
                            
                        with col2:
                            st.subheader("Threat Explanation")
                            st.write(result['explanation'])
                            
                            if result.get('red_flags'):
                                st.markdown("**Detected Red Flags:**")
                                for flag in result['red_flags']:
                                    st.markdown(f'<div class="alert-redflag">🚩 {flag}</div>', unsafe_allow_html=True)
                        
                        # --- 3. FEATURE ANALYSIS ---
                        st.markdown("### 📊 Feature Analysis")
                        f_col1, f_col2 = st.columns([2, 1])
                        
                        with f_col1:
                            with st.expander("View All Extracted Features", expanded=False):
                                features_df = pd.DataFrame(
                                    [{"Feature": k, "Value": v} for k, v in result['features'].items()]
                                )
                                st.dataframe(features_df, use_container_width=True, hide_index=True)
                                
                        with f_col2:
                            st.markdown("**Top Influential Features:**")
                            for imp_f in result.get('important_features', []):
                                st.markdown(f"- **{imp_f['name']}**: {imp_f['value']} *(Impact: {imp_f['importance']:.2f})*")
                                
                    except Exception as e:
                        st.error(f"Error during prediction: {str(e)}")

    st.markdown("---")

    # --- 5. MODEL PERFORMANCE SECTION ---
    st.header("📈 Model Performance Metrics")
    metrics = get_metrics()
    
    if metrics:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Accuracy", f"{metrics.get('accuracy', 0)*100:.1f}%", help="Overall correctness of the model")
        with m2:
            st.metric("Precision", f"{metrics.get('precision', 0)*100:.1f}%", help="Accuracy of positive (phishing) predictions")
        with m3:
            st.metric("Recall", f"{metrics.get('recall', 0)*100:.1f}%", help="Ability to find all phishing URLs")
        with m4:
            st.metric("F1 Score", f"{metrics.get('f1_score', 0)*100:.1f}%", help="Harmonic mean of Precision and Recall")
            
        # --- 6. VISUALIZATIONS ---
        v1, v2 = st.columns(2)
        
        with v1:
            st.subheader("Confusion Matrix")
            try:
                base = os.path.dirname(os.path.abspath(__file__))
                cm_path = os.path.join(base, "reports", "confusion_matrix.png")
                if os.path.exists(cm_path):
                    img = Image.open(cm_path)
                    st.image(img, use_container_width=True)
                else:
                    # Generate plotly matrix if image not found
                    cm = metrics.get('confusion_matrix', [[0,0,0],[0,0,0],[0,0,0]])
                    fig = px.imshow(cm, 
                                   labels=dict(x="Predicted", y="Actual", color="Count"),
                                   x=['Legitimate', 'Suspicious', 'Phishing'],
                                   y=['Legitimate', 'Suspicious', 'Phishing'],
                                   text_auto=True,
                                   color_continuous_scale="Blues")
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning("Could not load confusion matrix.")
                
        with v2:
            st.subheader("Feature Importance")
            try:
                fi_path = os.path.join(base, "reports", "feature_importance.png")
                if os.path.exists(fi_path):
                    img = Image.open(fi_path)
                    st.image(img, use_container_width=True)
                else:
                    fi = metrics.get('feature_importances', {})
                    if fi:
                        df_fi = pd.DataFrame([{"Feature": k, "Importance": v} for k, v in fi.items()])
                        df_fi = df_fi.sort_values(by="Importance", ascending=True).tail(10)
                        fig2 = px.bar(df_fi, x="Importance", y="Feature", orientation='h', color="Importance", color_continuous_scale="Viridis")
                        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("Feature importance data not available.")
            except Exception as e:
                st.warning("Could not load feature importance chart.")
    else:
        st.warning("Model metrics could not be loaded. Ensure the model has been trained and models/metrics.json exists.")

    # --- 8. METRIC EXPLANATIONS ---
    with st.expander("📚 Model Evaluation Terms Explained (Viva Reference)"):
        st.markdown("""
        * **Accuracy**: The ratio of correctly predicted observations to the total observations. It answers: *"How many URLs did we classify correctly overall?"*
        * **Precision**: The ratio of correctly predicted positive observations to the total predicted positive observations. It answers: *"Of all URLs labeled as phishing, how many were actually phishing?"* High precision means few false alarms (false positives).
        * **Recall (Sensitivity)**: The ratio of correctly predicted positive observations to all actual positives. It answers: *"Of all actual phishing URLs, how many did we catch?"* High recall means few missed threats (false negatives).
        * **F1 Score**: The weighted average of Precision and Recall. Useful when dealing with uneven class distribution, balancing false positives and false negatives.
        * **Confusion Matrix**: A table showing True Positives, True Negatives, False Positives, and False Negatives, providing a detailed breakdown of model performance across all classes.
        """)

    st.markdown("---")
    
    # --- 7. TEST RESULTS SECTION ---
    st.header("🧪 Batch Test Results")
    base = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(base, "tests", "test_urls.csv")
    
    if os.path.exists(test_file_path):
        if st.button("Run Batch Tests", key="run_tests"):
            try:
                test_df = pd.read_csv(test_file_path)
                results = []
                correct = 0
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, row in test_df.iterrows():
                    url = row.get('url', '')
                    expected = row.get('expected_result', '')
                    
                    if pd.isna(url) or not url:
                        continue
                        
                    is_val, clean_u, err = validate_url(url)
                    if is_val:
                        try:
                            pred = predict_url(clean_u)
                            actual = pred['classification']
                            is_correct = actual.lower() == expected.lower()
                            if is_correct:
                                correct += 1
                                
                            results.append({
                                'URL': url,
                                'Expected': expected,
                                'Actual': actual,
                                'Status': '✅ Pass' if is_correct else '❌ Fail'
                            })
                        except Exception:
                            results.append({
                                'URL': url,
                                'Expected': expected,
                                'Actual': 'Error',
                                'Status': '❌ Error'
                            })
                    else:
                        results.append({
                            'URL': url,
                            'Expected': expected,
                            'Actual': 'Invalid URL',
                            'Status': '❌ Error'
                        })
                        
                    progress_bar.progress((i + 1) / len(test_df))
                    status_text.text(f"Processed {i + 1}/{len(test_df)} URLs")
                
                # Show results
                if results:
                    res_df = pd.DataFrame(results)
                    st.success(f"Batch Test Complete: {correct}/{len(results)} correct predictions.")
                    
                    def color_status(val):
                        color = '#3fb950' if 'Pass' in str(val) else '#f85149'
                        return f'color: {color}'
                    
                    st.dataframe(res_df.style.map(color_status, subset=['Status']), use_container_width=True)
            except Exception as e:
                st.error(f"Error running batch tests: {str(e)}")
    else:
        st.info("Test dataset (tests/test_urls.csv) not found.")

    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; color: #8b949e;">
            <hr>
            <p>Phishing URL Detection System © 2024 | Secure Threat Intelligence</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
