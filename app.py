"""
Interactive Demo for AutoPrompt System
Run with: streamlit run app.py
"""
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.autoprompt import AutoPromptEngine
from src.baseline import BaselinePipeline
from src.utils import Review
from src.config_loader import load_secure_config
import json

# Page configuration
st.set_page_config(
    page_title="AutoPrompt Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3b82f6;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .baseline-box {
        background-color: #f1f5f9;
        border-left: 4px solid #94a3b8;
    }
    .autoprompt-box {
        background-color: #dbeafe;
        border-left: 4px solid: #3b82f6;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Load and cache the models"""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return None, None, "API key not found in .env file"
    
    try:
        config = load_secure_config()
        baseline = BaselinePipeline(config)
        autoprompt = AutoPromptEngine(config)
        return baseline, autoprompt, None
    except Exception as e:
        return None, None, str(e)

def format_result(data, title, color_class):
    """Format extraction result in a nice box"""
    st.markdown(f'<div class="result-box {color_class}">', unsafe_allow_html=True)
    st.subheader(title)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Product**")
        st.write(data.product)
    
    with col2:
        st.markdown("**Sentiment**")
        sentiment_emoji = {
            "positive": "😊",
            "negative": "😞",
            "neutral": "😐",
            "mixed": "🤔"
        }
        emoji = sentiment_emoji.get(data.sentiment.lower(), "")
        st.write(f"{emoji} {data.sentiment}")
    
    with col3:
        st.markdown("**Confidence**")
        st.write(f"{data.confidence:.1%}")
    
    st.markdown("**Reason**")
    st.write(data.reason)
    
    with st.expander("Technical Details"):
        st.write(f"**Prompt Used:** {data.prompt_used}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<p class="main-header">🚀 AutoPrompt Interactive Demo</p>', unsafe_allow_html=True)
    
    st.markdown("""
    This demo compares **Baseline** (single prompt) vs **AutoPrompt** (optimized multi-variant) 
    for extracting product information from reviews.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Load models
        baseline, autoprompt, error = load_models()
        
        if error:
            st.error(f"❌ Error loading models: {error}")
            st.info("Make sure you have a `.env` file with `GEMINI_API_KEY=your_key`")
            st.stop()
        else:
            st.success("✅ Models loaded successfully!")
        
        st.markdown("---")
        
        st.header("📊 Sample Reviews")
        sample_reviews = {
            "Coffee Maker (Positive)": "I absolutely love this coffee maker! Makes perfect coffee every morning and looks great on my counter.",
            "Blender (Negative)": "This blender is terrible. It broke after just two weeks of use. Very disappointed.",
            "Headphones (Mixed)": "The sound quality is amazing but they're quite uncomfortable for long listening sessions.",
            "Laptop (Neutral)": "It's a laptop. Does what it's supposed to do. Nothing special.",
        }
        
        selected_sample = st.selectbox("Choose a sample:", list(sample_reviews.keys()))
        
        if st.button("📝 Use Sample"):
            st.session_state.review_text = sample_reviews[selected_sample]
    
    # Main content
    st.header("📝 Enter Review Text")
    
    review_text = st.text_area(
        "Review Text",
        value=st.session_state.get('review_text', ''),
        height=150,
        placeholder="Enter a product review here...",
        help="Type or paste a product review to analyze"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        analyze_button = st.button("🔍 Analyze Review", type="primary", use_container_width=True)
    
    if analyze_button and review_text:
        review = Review(review_id="demo", review_text=review_text)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run Baseline
        status_text.text("Running Baseline...")
        progress_bar.progress(25)
        
        with st.spinner("Processing with Baseline..."):
            baseline_result = baseline.process(review)
        
        progress_bar.progress(50)
        
        # Run AutoPrompt
        status_text.text("Running AutoPrompt (testing multiple prompts)...")
        
        with st.spinner("Processing with AutoPrompt..."):
            autoprompt_result = autoprompt.process(review)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        st.markdown("---")
        st.header("📊 Results Comparison")
        
        # Display results side by side
        col1, col2 = st.columns(2)
        
        with col1:
            format_result(baseline_result, "⚡ Baseline Result", "baseline-box")
        
        with col2:
            format_result(autoprompt_result, "🚀 AutoPrompt Result", "autoprompt-box")
        
        # Comparison metrics
        st.markdown("---")
        st.header("📈 Comparison Metrics")
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                "Confidence Difference",
                f"{(autoprompt_result.confidence - baseline_result.confidence):.1%}",
                delta=f"{(autoprompt_result.confidence - baseline_result.confidence):.1%}"
            )
        
        with metric_col2:
            agreement = "✅ Match" if (
                baseline_result.product.lower() == autoprompt_result.product.lower() and
                baseline_result.sentiment.lower() == autoprompt_result.sentiment.lower()
            ) else "⚠️ Different"
            st.metric("Results Agreement", agreement)
        
        with metric_col3:
            st.metric("AutoPrompt Confidence", f"{autoprompt_result.confidence:.1%}")
        
        # Show JSON
        with st.expander("🔍 View Raw JSON Results"):
            col1, col2 = st.columns(2)
            with col1:
                st.json(baseline_result.dict())
            with col2:
                st.json(autoprompt_result.dict())
    
    elif analyze_button and not review_text:
        st.warning("⚠️ Please enter a review text to analyze!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748b;'>
        Built with ❤️ using Streamlit and Google Gemini AI<br>
        <a href='https://github.com/aayush-1o/auto-Prompt'>View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
