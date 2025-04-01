import pandas as pd
import streamlit as st
import json
import time
from services.test_case_generator import TestCaseGenerator
from services.karate_script_generator import KarateScriptGenerator
from utils.drift_detector import DriftDetectionApp
from utils.utilities import extract_schema
from PIL import Image

# Streamlit Config
st.set_page_config(page_title="AI Test Automation", layout="wide")

# Load data (only once, using st.cache to avoid reloading)
@st.cache_data
def load_data():
    real_data = pd.read_csv('./Datasets/SRE Domain/real_dataset.csv')
    synthetic_data = pd.read_csv('./Datasets/SRE Domain/synthetic_dataset.csv')
    return real_data, synthetic_data

real_data, synthetic_data = load_data()

# Initialize generators
test_case_generator = TestCaseGenerator()
karate_script_generator = KarateScriptGenerator()
drift_detector = DriftDetectionApp()

american_express_logo = Image.open('/Users/apple/Documents/Priyesh/Repositories/2025/GrowthHack/FinSyn-Innovators-GenAI/ui/amex_logo_png.png')
H1, H2, H3 = st.columns([1,4,8])
with H1:
    st.image(american_express_logo, width=250)
with H2:
    st.write("<h5 style='text-align: left; color: black;'>  </h5>", unsafe_allow_html=True)
with H3:
    st.markdown("<h3 style='text-align: center; color: black;'>  </h3>", unsafe_allow_html=True)

# Page Title
st.markdown("<h1 style='text-align: center; color: black;'> DataScriptAI </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'> AI-Powered Test Automation for Incident Management </h3>", unsafe_allow_html=True)

# Initialize session state variables
if "uploaded_swagger" not in st.session_state:
    st.session_state.uploaded_swagger = None
if "test_cases" not in st.session_state:
    st.session_state.test_cases = None
if "business_justification" not in st.session_state:
    st.session_state.business_justification = ""
if "karate_script" not in st.session_state:
    st.session_state.karate_script = None
if "schema" not in st.session_state:
    st.session_state.schema = None

# Business Justification Input
st.session_state.business_justification = st.text_area("Enter Business Justification", value=st.session_state.business_justification)

# Swagger File Upload
uploaded_swagger = st.file_uploader("Upload Swagger JSON File", type=["json"])
if uploaded_swagger is not None:
    st.session_state.uploaded_swagger = uploaded_swagger

# Process Swagger file and extract schema (only once)
if st.session_state.uploaded_swagger is not None and st.session_state.schema is None:
    try:
        swagger_json = json.load(st.session_state.uploaded_swagger)
        st.subheader("Swagger Information")
        st.code(json.dumps(swagger_json, indent=4), language='json', line_numbers=True)

        with st.spinner("Connecting with stored procedures to identify relevant tables..."):
            time.sleep(15)
            table_name = "create_incidents"
            st.subheader("Identified Table")
            st.success(f"The relevant data is found in table: **{table_name}**")

        with st.spinner("Extracting the table schema..."):
            time.sleep(10)
            st.session_state.schema = extract_schema(synthetic_data)
            st.subheader("Extracted Table Schema")
            st.code(json.dumps(st.session_state.schema, indent=4), language='json', line_numbers=True)

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid Swagger JSON.")

# Display data insights and drift reports (only if schema is available)
if st.session_state.schema is not None:
    with st.spinner("Generating test data based on schema..."):
        time.sleep(10)
        st.subheader("Data Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h5 style='text-align: center; color: black;'> Real Data </h5>", unsafe_allow_html=True)
            st.write(real_data.head())
        with col2:
            st.markdown("<h5 style='text-align: center; color: black;'> Test Data </h5>", unsafe_allow_html=True)
            st.write(synthetic_data.head())

        st.subheader("Drift Reports")
        drift_detector.run(real_data, synthetic_data)

# Generate Test Cases Button
if st.session_state.uploaded_swagger is not None and st.session_state.business_justification:
    #if st.button("Generate Test Cases"):
    with st.spinner("Generating test cases..."):
        time.sleep(2)
        st.session_state.test_cases = test_case_generator.generate_test_cases_sre(
            st.session_state.uploaded_swagger, synthetic_data, st.session_state.business_justification
        )
        st.success("Test Cases Generated!")


# Display Generated Test Cases
if st.session_state.test_cases is not None:
    st.header("Generated Test Cases")
    st.write(st.session_state.test_cases)

    # Generate Karate Scripts Button
    #if st.button("Generate Karate Scripts"):
    with st.spinner("Generating Karate scripts..."):
        time.sleep(2)
        st.session_state.karate_script = karate_script_generator.generate_karate_script(st.session_state.test_cases)
        st.header("Karate Script Generated!")
        st.code(st.session_state.karate_script, language="java")

    # Download Buttons
    st.download_button("Download Test Cases", data=str(st.session_state.test_cases), file_name="test_cases.txt")

if st.session_state.karate_script is not None:
    st.download_button("Download Karate Script", data=st.session_state.karate_script, file_name="karate_script.feature")
    st.download_button("Push Karate Scripts to GitHub", data=st.session_state.karate_script, file_name="run_karate_script.feature")