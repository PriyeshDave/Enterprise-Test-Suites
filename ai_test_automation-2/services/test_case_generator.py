from utils.llm_client import LLMClient

class TestCaseGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def generate_test_cases(self, swagger_file, synthetic_data_file, business_justification):
        prompt = f'''
        Generate test cases based on 
        SWAGGER FILE: {swagger_file}, 
        DATA FILE : {synthetic_data_file}, and 
        JUSTIFICATION: {business_justification} 
        
        generate comprehensive test cases covering:
        - Positive cases
        - Negative cases
        - Edge cases 
         
           Provide test cases in JSON format including API endpoint, request body, and expected response.
        '''
        return self.llm.query_llm(prompt)
    

    def generate_test_cases_sre(self, swagger_file, synthetic_data_file, business_justification):
        prompt = f'''
        Generate test cases based on 
        SWAGGER FILE: {swagger_file}, 
        DATA FILE : {synthetic_data_file}, and 
        JUSTIFICATION: {business_justification} 
        
        generate comprehensive test cases covering:
        - Valid Incident Logging: Ensuring that valid incidents are correctly created.
        - Invalid Severity Levels: Testing scenarios where invalid severity values are passed.
        - Missing Required Fields: Ensuring that the system rejects incomplete incident reports.
        - Duplicate Incident IDs: Checking if duplicate incident submissions are handled properly.
        - Incident Escalation: Simulating escalation workflows based on severity.
         
           Provide test cases in JSON format including API endpoint, request body, and expected response.
        '''
        return self.llm.query_llm(prompt)

