import os
import pandas as pd
import streamlit as st
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY not found in environment variables. Please add it to your .env file.")
    st.stop()

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing OpenAI client: {str(e)}")
    st.info("Try: pip install --upgrade openai")
    st.stop()

st.set_page_config(page_title="AutoAnalyst AI", layout="wide")
st.title("AutoAnalyst AI")


# ---------------- DATA ANALYSIS ENGINE ----------------
def analyze_dataset(df):
    """Comprehensive dataset analysis for executive insights"""
    analysis = {
        'shape': df.shape,
        'columns': list(df.columns),
        'numeric_cols': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_cols': df.select_dtypes(include=['object']).columns.tolist(),
        'missing_data': df.isnull().sum().to_dict(),
        'key_stats': {},
        'outliers': {},
        'top_values': {}
    }
    
    # Key statistics for numeric columns
    for col in analysis['numeric_cols']:
        series = df[col].dropna()
        if len(series) > 0:
            q1, q3 = series.quantile([0.25, 0.75])
            iqr = q3 - q1
            outlier_threshold = q3 + 1.5 * iqr
            
            analysis['key_stats'][col] = {
                'min': series.min(),
                'max': series.max(),
                'mean': series.mean(),
                'median': series.median(),
                'std': series.std(),
                'total': series.sum()
            }
            
            # Detect outliers
            outliers = series[series > outlier_threshold]
            if len(outliers) > 0:
                analysis['outliers'][col] = len(outliers)
    
    # Top values for categorical columns
    for col in analysis['categorical_cols']:
        if col in df.columns:
            top_vals = df[col].value_counts().head(3)
            analysis['top_values'][col] = top_vals.to_dict()
    
    return analysis


# ---------------- AI EXECUTIVE INSIGHTS ----------------
def generate_executive_insights(analysis, df):
    """Generate structured executive insights using AI"""
    
    # Prepare comprehensive data summary
    summary_text = f"""
    Dataset Overview:
    - {analysis['shape'][0]:,} rows, {analysis['shape'][1]} columns
    - Numeric columns: {len(analysis['numeric_cols'])}
    - Categorical columns: {len(analysis['categorical_cols'])}
    
    Key Statistics:
    """
    
    for col, stats in analysis['key_stats'].items():
        summary_text += f"\n{col}: Range ${stats['min']:,.0f} - ${stats['max']:,.0f}, Average ${stats['mean']:,.0f}, Total ${stats['total']:,.0f}"
    
    summary_text += "\n\nTop Categories:"
    for col, values in analysis['top_values'].items():
        top_3 = list(values.items())[:3]
        summary_text += f"\n{col}: {', '.join([f'{k}({v})' for k, v in top_3])}"
    
    if analysis['outliers']:
        summary_text += "\n\nOutliers detected in: " + ", ".join(analysis['outliers'].keys())
    
    prompt = f"""
    You are a senior business analyst presenting to executives. Analyze this dataset and provide insights in exactly this format:
    
    {summary_text}
    
    Provide response in this exact structure with HTML formatting:
    
    **Executive Summary**
    
    <div style="color: #2E4A6B;"><em>[4-5 sentences providing a comprehensive summary of what this dataset contains, the business domain it represents, key data characteristics, and overall business story. Focus on describing the table structure, main data categories, and business context.]</em></div>
    
    ---
    
    **Key Highlights**
    
    <div style="color: #2E4A6B;"><em>• [Most important finding with specific numbers]</em></div>
    <div style="color: #2E4A6B;"><em>• [Second most important finding]</em></div>
    <div style="color: #2E4A6B;"><em>• [Third key insight]</em></div>
    
    ---
    
    **Business Recommendations**
    
    <div style="color: #2E4A6B;"><em>• [Specific actionable recommendation]</em></div>
    <div style="color: #2E4A6B;"><em>• [Second recommendation]</em></div>
    <div style="color: #2E4A6B;"><em>• [Third recommendation]</em></div>
    
    ---
    
    **Attention Required**
    
    <div style="color: #2E4A6B;"><em>• [Any outliers, anomalies, or data quality issues]</em></div>
    <div style="color: #2E4A6B;"><em>• [Unusual patterns or concerning trends]</em></div>
    <div style="color: #2E4A6B;"><em>• [Missing data or gaps that need investigation]</em></div>
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {str(e)}"


# ---------------- UI LAYOUT ----------------
uploaded = st.file_uploader("Upload Your Data (Excel/CSV)", type=["xlsx", "csv"])

if uploaded:
    # Read file efficiently
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        
        st.success(f"Loaded {df.shape[0]:,} rows x {df.shape[1]} columns")
        
        # Full Data Preview
        st.subheader("Complete Dataset")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Generate Analysis
        with st.spinner("Analyzing dataset..."):
            analysis = analyze_dataset(df)
        
        # AI Executive Insights
        st.subheader("Executive Intelligence Report")
        if st.button("Generate Executive Insights", type="primary"):
            with st.spinner("Generating executive insights..."):
                insights = generate_executive_insights(analysis, df)
            st.markdown(insights, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

else:
    st.info("Upload your data file to begin executive analysis")
    st.markdown("""
    ### What This Tool Does:
    - **Instant Analysis**: Upload any CSV/Excel file for immediate insights
    - **Executive Focus**: Business-ready summaries, not technical jargon
    - **AI-Powered**: Advanced pattern detection and recommendations
    - **Efficiency Optimized**: Fast processing with smart sampling techniques
    """)