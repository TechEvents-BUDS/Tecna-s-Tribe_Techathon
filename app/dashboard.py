import os
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import streamlit.components.v1 as components

# Add the project root to the Python path if necessary
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import necessary functions from the model (assuming these are in the model folder)
from utility import *   # Assuming utility.py exists
from model.genai import *  # Assuming genai.py exists

# Page Config
st.set_page_config(layout="wide", page_title="Neutral AI Dashboard")

# Load external CSS
with open("static/style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Load external HTML template
with open("templates/template.html") as html_file:
    st.markdown(html_file.read(), unsafe_allow_html=True)

# Title and Description
st.title("Neutral AI Project Dashboard")
st.write("A beginner-friendly dashboard for visualizing and interacting with the Neutral AI project.")

# Sidebar Navigation
st.sidebar.header(" ")
col1, col2 = st.sidebar.columns([1, 4])
with col1:
    st.image("C:/Users/HP/Desktop/Neutral/Neutral/app/static/circle.png", width=50)
with col2:
    st.text("Neutral")
options = ["Overview", "Data Visualization", "Comparitive Analysis", "Final Analysis"]
choice = st.sidebar.radio("", options)

# Data for Bias Analysis
bias_data = {
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Gender Bias (%)": [75, 70, 68, 65, 62, 60, 58, 55, 52, 50],
    "Ageism Bias (%)": [60, 58, 55, 53, 50, 48, 47, 45, 43, 40],
    "Racism Bias (%)": [80, 75, 72, 70, 68, 65, 63, 60, 58, 55],
}

# Convert to DataFrame
df_bias = pd.DataFrame(bias_data)

# Function for the file upload and first analysis (this is your first_page logic)
def first_page():
    UPLOAD_DIR = "uploads"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    uploaded_file_1 = st.file_uploader("Step 1: Upload Your CV (PDF format only)", type="pdf")
    uploaded_file_2 = st.file_uploader("Step 2: Upload the Company's Reason for Not Hiring (PDF format only)", type="pdf")

    if uploaded_file_1:
        file_path_1 = os.path.join(UPLOAD_DIR, 'cv.pdf')
        with open(file_path_1, "wb") as f:
            f.write(uploaded_file_1.getbuffer())
        st.write(f"✅ Uploaded CV: **{uploaded_file_1.name}** (saved at {file_path_1})")
    if uploaded_file_2:
        file_path_2 = os.path.join(UPLOAD_DIR, 'decision.pdf')
        with open(file_path_2, "wb") as f:
            f.write(uploaded_file_2.getbuffer())
        st.write(f"✅ Uploaded Reason File: **{uploaded_file_2.name}** (saved at {file_path_2})")

    if st.button("Start Bias Analysis"):
        if uploaded_file_1 and uploaded_file_2:
            st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
            analysis_result = send_to_ai(file_path_1, file_path_2)
            return analysis_result
        else:
            st.error("Please upload both files before proceeding.")
    return None

# Function for displaying the final analysis result (this is your final_analysis logic)
def final_analysis(analysis: str):
    st.title("Detecting Biases in Hiring")
    st.header("Neutral's Analysis Result")
    st.markdown(f"""
        <div style="background-color: #222; color: #ddd; padding: 15px; border-radius: 5px;">
            <p style="font-size: 16px;">{analysis}</p>
        </div>
    """, unsafe_allow_html=True)

    # Combined Biases Chart
    st.write("### Bias Trends Over 10 Years (Gender, Ageism, Racism)")
    combined_chart_data = {
        "chart": {"type": "line"},
        "series": [
            {"name": "Gender Bias (%)", "data": df_bias["Gender Bias (%)"].tolist()},
            {"name": "Ageism Bias (%)", "data": df_bias["Ageism Bias (%)"].tolist()},
            {"name": "Racism Bias (%)", "data": df_bias["Racism Bias (%)"].tolist()},
        ],
        "xaxis": {"categories": df_bias["Year"].tolist()},
        "title": {"text": "Bias Trends Over 10 Years"},
        "colors": ["#ff7f0e", "#1f77b4", "#2ca02c"],
    }

    components.html(f"""
    <div id="combined-bias-chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {combined_chart_data};
    var chart = new ApexCharts(document.querySelector('#combined-bias-chart'), options);
    chart.render();
    </script>
    """, height=500)

    if st.button("Generate PDF"):
        pdf_stream = BytesIO()
        c = canvas.Canvas(pdf_stream, pagesize=letter)
        c.drawString(72, 750, "Neutral's Analysis Result")
        c.drawString(72, 730, "Analysis:")
        y = 710
        line_height = 14
        for line in analysis.splitlines():
            c.drawString(72, y, line)
            y -= line_height
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        pdf_stream.seek(0)
        st.download_button(
            label="Download PDF",
            data=pdf_stream.getvalue(),
            file_name="analysis_result.pdf",
            mime="application/pdf",
        )

# Function to send files to AI for analysis (your send_to_ai function)
def send_to_ai(cv_path, decision_path):
    # Placeholder function for AI processing
    return "This is a placeholder analysis result."

# Main application flow
if choice == "Overview":
    analysis_result = first_page()  # This is your first page logic for file upload and analysis
    if analysis_result:
        st.session_state.analysis_result = analysis_result  # Store the result in session state

elif choice == "Data Visualization":
    st.subheader("Data Visualization")
    st.write("Coming soon!")

elif choice == "Comparitive Analysis":
    st.subheader("Comparitive Analysis")
    st.write("Coming soon!")

elif choice == "Final Analysis":
    if 'analysis_result' in st.session_state:
        final_analysis(st.session_state.analysis_result)  # Display the analysis result

# Footer
st.write("---")
st.write("Built with ❤️ using Streamlit and ApexCharts.")
