import streamlit as st
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


class DriftDetectionApp:
    def __init__(self):
        self.report = None
        self.table_evaluator_results_path = './outputs/'
    
    def run(self, current_data, reference_data ):
        with st.spinner("Generating drift report..."):
            for i in range(1, 6):
                st.image(f'{self.table_evaluator_results_path}{i}.png')
            self.report = Report(metrics=[DataDriftPreset()])
            self. report.run(reference_data=reference_data, current_data=current_data)
            st.success("Drift report generated successfully!")
            st.components.v1.html(self.report.get_html(), height=800, scrolling=True)
        
