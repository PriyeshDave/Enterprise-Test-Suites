import pandas as pd
import streamlit as st
import json
import time
from services.test_case_generator import TestCaseGenerator
from services.karate_script_generator import KarateScriptGenerator
from utils.drift_detector import DriftDetectionApp
from utils.utilities import extract_schema

real_data = pd.read_csv('./Datasets/real_data.csv')
synthetic_data = pd.read_csv('./Datasets/synthetic_data.csv')
test_case_generator = TestCaseGenerator()
karate_script_generator = KarateScriptGenerator()
drift_detector = DriftDetectionApp()


st.set_page_config(page_title="AI Test Automation", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'> DataScriptAI </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'> AI-Powered Test Automation: Data, Test Cases & Scripts Generation </h3>", unsafe_allow_html=True)

test_cases = None
table_name = "transaction_details"
business_justification = st.text_area("Enter Business Justification")

uploaded_swagger = st.file_uploader("Upload Swagger JSON File", type=["json"])
if uploaded_swagger is not None:
    try:
        swagger_json = json.load(uploaded_swagger)
        st.subheader("Swagger Information")
        st.code(json.dumps(swagger_json, indent=4), language='json', line_numbers=True)
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid Swagger JSON.")

    with st.spinner("Connecting with stored procedures to identify relevant tables..."):
        time.sleep(6)
        st.subheader("Identified Table")
        st.success(f"The relevant data is found in table: **{table_name}**")

    with st.spinner("extracting the table schema..."):
        time.sleep(6)
        schema = extract_schema(synthetic_data)
        st.subheader("Extracted Table Schema")
        st.code(json.dumps(schema, indent=4), language='json', line_numbers=True)
            
    if schema:
        with st.spinner("Generating synthetic test data based on schema..."):
            time.sleep(6)
            st.subheader("Data Insights")
            col1, col2 = st.columns(2)
            with col1:
                #st.subheader("Real Data")
                st.markdown("<h5 style='text-align: center; color: black;'> Real Data </h5>", unsafe_allow_html=True)
                st.write(real_data.head())
            with col2:
                #st.subheader("Synthetic Test Data")
                st.markdown("<h5 style='text-align: center; color: black;'> Synthetic Data </h5>", unsafe_allow_html=True)
                st.write(synthetic_data.head())
            
            st.subheader("Drift Reports")
            drift_detector.run(real_data, synthetic_data)



    if st.button("Generate Test Cases"):
        if uploaded_swagger and business_justification:
            st.json(uploaded_swagger)
            test_cases = test_case_generator.generate_test_cases(uploaded_swagger, 
                                                                synthetic_data, 
                                                                business_justification)
            st.session_state["test_cases"] = test_cases
            st.success("Test Cases Generated!")


        if "test_cases" in st.session_state:
            st.subheader("Generated Test Cases")
            st.write(test_cases)
            response_json = {"test_cases": test_cases}



        if st.button("Generate Karate Scripts"):
            if "test_cases" in st.session_state:
                karate_script = karate_script_generator.generate_karate_script(test_cases)
                st.session_state["karate_script"] = karate_script
                st.success("Karate Script Generated!")
                st.code(karate_script, language="java")


        if "test_cases" in st.session_state:
            st.download_button("Download Test Cases", 
                            data=str(test_cases), 
                            file_name="test_cases.txt")

        if "karate_script" in st.session_state:
            st.download_button("Download Karate Script", data=st.session_state["karate_script"], file_name="karate_script.feature")
