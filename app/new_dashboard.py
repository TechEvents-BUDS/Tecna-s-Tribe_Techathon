import os
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import streamlit.components.v1 as components
import PyPDF2
import time

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
st.title("Towards Inclusive Hiring Practices")
st.write("Analyze biases in hiring decisions to promote fairness and equity. Your journey to better insights starts here.")

# Sidebar Navigation
st.sidebar.header(" ")
col1, col2 = st.sidebar.columns([1, 4])
with col1:
    st.image("static/circle.png", width=50)
with col2:
    st.text("Neutral")
options = ["Overview", "Data Visualization", "Comparitive Analysis", "Final Analysis"]
choice = st.sidebar.radio("", options)

# Data for Gender Bias in Hiring over 10 years
bias_data = {
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Bias_Level": [75, 70, 68, 65, 62, 60, 58, 55, 52, 50],  # Example data, represent bias percentage
}

# Data for Gender Bias in Hiring over 10 years
bias_data = {
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Bias_Level": [75, 70, 68, 65, 62, 60, 58, 55, 52, 50],  # Example data, represent bias percentage
}

# Data for Ageism in Hiring over 10 years
ageism_data = {
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Bias_Level": [60, 58, 55, 53, 50, 48, 47, 45, 43, 40],  # Example data for ageism bias percentage
}
# Data for Racism in Hiring over 10 years
racism_data = {
    "Year": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Bias_Level": [80, 75, 72, 70, 68, 65, 63, 60, 58, 55],  # Example data for racism bias percentage
}
# Data for Gender Comparison in Software Company
gender_data = {
    "Gender": ["Male", "Female"],
    "Count": [140, 50]  # Example data: 120 males and 80 females
} 
# Data for Gender Comparison in Software Company
age_data = {
    "Age": ["Below 40", "Above 40"],
    "Count": [160, 60]  
} 
# Data for Gender Comparison in Software Company
race_data = {
    "Race": ["White", "Black", "Hispanic", "East Asians", "South Asians"],
    "Count": [160, 60, 30, 120, 140]  
}
# Convert to DataFrame
df_bias = pd.DataFrame(bias_data)
df_ageism = pd.DataFrame(ageism_data)
df_racism = pd.DataFrame(racism_data)

# Convert to DataFrame
df_bias = pd.DataFrame(bias_data)

# Function for the file upload and first analysis (this is your first_page logic)
def first_page():
    """
    Creates the first page with file upload functionality.
    Returns two placeholder strings for demonstration.
    """

    # File upload for CV
    cv_file = st.file_uploader("Upload CV", type=['pdf', 'docx', 'txt'])
    
    # File upload for decision document
    decision_file = st.file_uploader("Upload Decision Document", type=['pdf', 'docx', 'txt'])
    

    # Analyze button
    if st.button("Analyze Documents"):
        # Store files in session state
        st.session_state.cv_file = cv_file
        st.session_state.decision_file = decision_file
        
        if cv_file and decision_file:
            st.success("Files uploaded and saved successfully! Starting analysis...", icon="📊")
            cv = pdf_to_text(cv_file)
            decision = pdf_to_text(decision_file)
            analysis_result = send_to_ai(cv, decision)
            return analysis_result
        else:
            st.error("Upload both files")
        # Switch to analysis page
        st.session_state.page = 'analysis'
        
        # Use st.rerun() instead of experimental_rerun()
        st.rerun()
    


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


def pdf_to_text(uploaded_file):
    """
    Converts an uploaded file (PDF, DOCX, or TXT) to text.
    
    Args:
        uploaded_file (UploadedFile): Streamlit uploaded file object
    
    Returns:
        str: The extracted text from the file
    
    Raises:
        ValueError: If an unsupported file type is uploaded
    """
    if uploaded_file is None:
        return ""
    
    # Determine file type based on file name
    filename = uploaded_file.name.lower()
    
    try:
        # PDF file handling
        if filename.endswith('.pdf'):
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            # Initialize an empty string to store the text
            full_text = ''
            
            # Extract text from each page
            for page in pdf_reader.pages:
                # Extract text from the current page and append to full_text
                full_text += page.extract_text() + '\n'
            
            return full_text.strip()
        
        # DOCX file handling
        elif filename.endswith('.docx'):
            # Read the docx file
            doc = docx.Document(uploaded_file)
            
            # Extract text from all paragraphs
            full_text = '\n'.join([para.text for para in doc.paragraphs])
            
            return full_text.strip()
        
        # TXT file handling
        elif filename.endswith('.txt'):
            # Read text files directly
            return uploaded_file.getvalue().decode('utf-8').strip()
        
        else:
            # Unsupported file type
            raise ValueError(f"Unsupported file type: {filename}")
    
    except Exception as e:
        st.error(f"Error processing file {filename}: {str(e)}")
        return ""



def send_to_ai(cv, decision):

    user_req = f'''Turn the text delimited by triple backticks into the following columns:
    S.No,Age,Accessibility,EdLevel,Employment,Gender,MentalHealth,MainBranch,YearsCode,YearsCodePro,Country,PreviousSalary,HaveWorkedWith,ComputerSkills,Employed,Age_Category,Is_Employed,Skills_List,Skills_Count,Education_Level,Gender_Category,Previous_Salary,Years_Coding,Years_Professional_Coding
    ```{cv}```
    RESPOND IN ONLY CSV VALUE - NO ADDITIONAL TEXT, ONLY THE VALUES IN COMMA SEPARATED FORMAT, DO NOT INCLUDE THE COLUMN NAMES EITHER 
    '''

    ai = AI(SYSTEM_PROMPT)
    new_columns = ai.generate_response(user_req)
    # ml_decision = get_ml_decision(new_columns)
    ml_decision = 'BIASED'
    new_prompt = f""" 
    You know the following things
    CV (delimited by triple backticks) : ```{cv}```,
    Decision (delimited by double backticks): ``{decision}``,
    You also have a prediction from an expert machine learning system that determined the following decision as {ml_decision}
    
    Now write 500 words explaining why the following decision for the following candidate (the one whose cv is given) might be biased or might be a justfied decision.
    Remember to always trust the machine learning's decision - it's been trained for this purpose and is more accurate
"""
    document = ai.generate_response(new_prompt)

    return document


# Main application flow
if choice == "Overview":
    analysis_result = first_page()  # This is your first page logic for file upload and analysis
    if analysis_result:
        st.session_state.analysis_result = analysis_result  # Store the result in session state

elif choice == "Data Visualization":
    st.subheader("Data Visualization")

    # Gender Bias in Hiring Bar Chart
    st.write("### Gender Bias in Hiring over 10 Years")
    chart_data = {
        "chart": {
            "type": "bar"
        },
        "series": [{
            "name": "Bias Level (%)",
            "data": df_bias["Bias_Level"].tolist()
        }],
        "xaxis": {
            "categories": df_bias["Year"].tolist()
        },
        "title": {
            "text": "Gender Bias in Hiring Over 10 Years"
        },
        "colors": ['#7f7fdb', '#33FF57', '#3357FF', '#FF33A6', '#FF9633', '#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FF9633']
    }
    components.html(f"""
    <div id="chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {chart_data};
    var chart = new ApexCharts(document.querySelector('#chart'), options);
    chart.render();
    </script>
    """, height=500)

        # Ageism Bias in Hiring Bar Chart (updated to bar chart)
    st.write("### Ageism Bias in Hiring over 10 Years")
    ageism_chart_data = {
        "chart": {
            "type": "bar"  # Change the chart type to bar
           
        },
        "series": [{
            "name": "Bias Level (%)",
            "data": df_ageism["Bias_Level"].tolist()
        }],
        "xaxis": {
            "categories": df_ageism["Year"].tolist()
        },
        "title": {
            "text": "Ageism Bias in Hiring Over 10 Years"
        },
        "colors": ['#f49230', '#33FF57', '#3357FF', '#FF33A6', '#FF9633', '#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FF9633']
    }

    components.html(f"""
    <div id="ageism-chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {ageism_chart_data};
    var chart = new ApexCharts(document.querySelector('#ageism-chart'), options);
    chart.render();
    </script>
    """, height=500)


    # Detailed table of the bias data
    st.write("### Detailed Table of Bias Data")
    st.dataframe(df_bias)

    # Racism Bias in Hiring Bar Chart (new chart)
    st.write("### Racism Bias in Hiring over 10 Years")
    racism_chart_data = {
        "chart": {
            "type": "bar"
        },
        "series": [{
            "name": "Bias Level (%)",
            "data": df_racism["Bias_Level"].tolist()
        }],
        "xaxis": {
            "categories": df_racism["Year"].tolist()
        },
        "title": {
            "text": "Racism Bias in Hiring Over 10 Years"
        },
        "colors": ['#c472ff', '#FF33A6', '#33FF57', '#3357FF', '#FF9633', '#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FF9633']
    }
    components.html(f"""
    <div id="racism-chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {racism_chart_data};
    var chart = new ApexCharts(document.querySelector('#racism-chart'), options);
    chart.render();
    </script>
    """, height=500)

    # Detailed table of the bias data
    st.write("### Detailed Table of Bias Data")
    st.dataframe(df_bias)


elif choice == "Comparitive Analysis":

    # Pie chart configuration for Gender Comparison
    gender_chart_data = {
        "chart": {
            "type": "pie",  # Set chart type to pie
             "width": "400",  # Adjust the width of the pie chart
             "height": "400"  # Adjust the height of the pie chart
        },
        "series": gender_data["Count"],  # The values to plot
        "labels": gender_data["Gender"],  # Labels for each segment
        "title": {
            "text": "Gender Comparison in a Software Company"
        },
        "colors": ['#7f7fdb', '#0d0d70']  # Custom colors for male and female
    }

    # Render the pie chart in Streamlit
    components.html(f"""
    <div id="gender-chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {gender_chart_data};
    var chart = new ApexCharts(document.querySelector('#gender-chart'), options);
    chart.render();
    </script>
    """, height=500)

    # Pie chart configuration for AGE Comparison
    age_chart_data = {
        "chart": {
            "type": "pie",  # Set chart type to pie
             "width": "400",  # Adjust the width of the pie chart
             "height": "400"  # Adjust the height of the pie chart
        },
        "series": age_data["Count"],  # The values to plot
        "labels": age_data["Age"],  # Labels for each segment
        "title": {
            "text": "age Comparison in a Software Company"
        },
        "colors": ['#c472ff', '#6616a3']  # Custom colors for male and female
    }

    # Render the pie chart in Streamlit
    components.html(f"""
    <div id="age-chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {age_chart_data};
    var chart = new ApexCharts(document.querySelector('#age-chart'), options);
    chart.render();
    </script>
    """, height=500)

    # Pie chart for race
    # Pie chart configuration for Gender Comparison
    race_chart_data = {
        "chart": {
            "type": "pie",  # Set chart type to pie
             "width": "400",  # Adjust the width of the pie chart
             "height": "400"  # Adjust the height of the pie chart
        },
        "series": race_data["Count"],  # The values to plot
        "labels": race_data["Race"],  # Labels for each segment
        "title": {
            "text": "race Comparison in a Software Company"
        },
        "colors": ['#6a040f', '#9d0208', '#d00000', '#dc2f02', '#e85d04' ]  # Custom colors for male and female
    }

    # Render the pie chart in Streamlit
    components.html(f"""
    <div id="race-chart"></div>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
    var options = {race_chart_data};
    var chart = new ApexCharts(document.querySelector('#race-chart'), options);
    chart.render();
    </script>
    """, height=500)
# Automatically move to Final Analysis after Overview


elif choice == "Final Analysis":
    if 'analysis_result' in st.session_state:
        # Theme-aware colorful content styling
        st.markdown(
            f"""
            <div style="
                border: 2px solid #a855f7;
                padding: 20px;
                border-radius: 15px;
                background: linear-gradient(135deg, #f9f7ff, #e9d5ff, #fce7f3);
                color: #3b0764;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            ">
                <h3 style="margin-bottom: 10px; color: #7e22ce;">🌟 Final Analysis Result</h3>
                <p style="margin: 0; font-size: 1.1em;">{st.session_state.analysis_result}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("No analysis result available yet. Upload your files in earlier steps!")
# Footer
st.write("---")
st.write("Built by Tecna's Tribe ❤️")
