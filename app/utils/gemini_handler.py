import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class CallGemini:
    def __init__(self,model_name='gemini-2.0-flash'):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self,prompt):
        response = self.model.generate_content(prompt)
        generated_text = response.candidates[0].content.parts[0].text
        return generated_text