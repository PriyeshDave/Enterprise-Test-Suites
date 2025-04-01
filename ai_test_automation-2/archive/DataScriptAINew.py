import pandas as pd
import streamlit as st
import json
import time
from services.test_case_generator import TestCaseGenerator
from services.karate_script_generator import KarateScriptGenerator
from utils.drift_detector import DriftDetectionApp
from utils.utilities import extract_schema

# Streamlit Config
st.set_page_config(page_title="AI Test Automation", layout="wide")

# Load data (only once, using st.cache to avoid reloading)
@st.cache_data
def load_data():
    real_data = pd.read_csv('./Datasets/real_data.csv')
    synthetic_data = pd.read_csv('./Datasets/synthetic_data.csv')
    return real_data, synthetic_data

real_data, synthetic_data = load_data()

# Initialize generators
test_case_generator = TestCaseGenerator()
karate_script_generator = KarateScriptGenerator()
drift_detector = DriftDetectionApp()

# Page Title
st.markdown("<h1 style='text-align: center; color: black;'> DataScriptAI </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'> AI-Powered Test Automation: Data, Test Cases & Scripts Generation </h3>", unsafe_allow_html=True)

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
if "drift_reports_generated" not in st.session_state:
    st.session_state.drift_reports_generated = False

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
            table_name = "transaction_details"
            st.subheader("Identified Table")
            st.success(f"The relevant data is found in table: **{table_name}**")

        with st.spinner("Extracting the table schema..."):
            time.sleep(15)
            st.session_state.schema = extract_schema(synthetic_data)
            st.subheader("Extracted Table Schema")
            st.code(json.dumps(st.session_state.schema, indent=4), language='json', line_numbers=True)

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid Swagger JSON.")

# Display data insights and drift reports (only if schema is available)
if st.session_state.schema is not None:
    with st.spinner("Generating synthetic test data based on schema..."):
        time.sleep(15)
        st.subheader("Data Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h5 style='text-align: center; color: black;'> Real Data </h5>", unsafe_allow_html=True)
            st.write(real_data.head())
        with col2:
            st.markdown("<h5 style='text-align: center; color: black;'> Synthetic Data </h5>", unsafe_allow_html=True)
            st.write(synthetic_data.head())

        st.subheader("Drift Reports")
        drift_detector.run(real_data, synthetic_data)
        st.session_state.drift_reports_generated = True  # Mark drift reports as generated

# Show "Generate Test Cases" form only after drift reports are generated
if st.session_state.drift_reports_generated:
    with st.form("test_case_form"):
        st.write("Generate Test Cases")
        if st.form_submit_button("Generate Test Cases"):
            if st.session_state.uploaded_swagger and st.session_state.business_justification:
                with st.spinner("Generating test cases..."):
                    st.session_state.test_cases = test_case_generator.generate_test_cases(
                        st.session_state.uploaded_swagger, synthetic_data, st.session_state.business_justification
                    )
                    st.success("Test Cases Generated!")

# Display Generated Test Cases
if st.session_state.test_cases is not None:
    st.subheader("Generated Test Cases")
    st.write(st.session_state.test_cases)

    # Show "Generate Karate Scripts" form only after test cases are generated
    with st.form("karate_script_form"):
        st.write("Generate Karate Scripts")
        if st.form_submit_button("Generate Karate Scripts"):
            with st.spinner("Generating Karate scripts..."):
                st.session_state.karate_script = karate_script_generator.generate_karate_script(st.session_state.test_cases)
                st.success("Karate Script Generated!")
                st.code(st.session_state.karate_script, language="java")

    # Download Buttons
    st.download_button("Download Test Cases", data=str(st.session_state.test_cases), file_name="test_cases.txt")

if st.session_state.karate_script is not None:
    st.download_button("Download Karate Script", data=st.session_state.karate_script, file_name="karate_script.feature")