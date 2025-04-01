from utils.llm_client import LLMClient

class KarateScriptGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def generate_karate_script(self, test_cases):
        prompt = f'''
        Given these test cases in json format:
        {test_cases}

        Generate Karate automation scripts for testing the APIs.
        Do not give the steps but core Karate scripts based on the test cases given.
        '''
        return self.llm.query_llm(prompt)

