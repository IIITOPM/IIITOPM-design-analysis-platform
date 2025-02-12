import google.generativeai as genai
from duckduckgo_search import DDGS
from typing import List, Dict, Any
import os
from PIL import Image
import io
import streamlit as st
import base64

class DuckDuckGo:
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
        return results

class Agent:
    def __init__(self, model: str, system_prompt: str):
        self.model = model
        self.system_prompt = system_prompt
    
    def initialize_model(self):
        # Configure the model - using appropriate models for vision and text
        if self.model == "gemini-1.5-flash":
            self.genai_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.genai_model = genai.GenerativeModel('gemini-pro')
    
    def run(self, prompt: str, files: List[Any] = None) -> str:
        try:
            # Initialize model if not already initialized
            if not hasattr(self, 'genai_model'):
                self.initialize_model()
            
            if self.model == "gemini-1.5-flash" and files:
                # Convert image to bytes
                image = Image.open(files[0])
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format or 'PNG')
                img_byte_arr = img_byte_arr.getvalue()

                # Create content parts in the correct format
                content = [
                    {
                        "parts": [
                            {"text": f"{self.system_prompt}\n\n{prompt}"},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": img_byte_arr
                                }
                            }
                        ]
                    }
                ]
                
                response = self.genai_model.generate_content(content)
            else:
                full_prompt = f"{self.system_prompt}\n\nUser: {prompt}"
                response = self.genai_model.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.7}
                )
            
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'parts'):
                return response.parts[0].text
            return "No response generated."
        except Exception as e:
            return f"Error generating response: {str(e)}"

def create_vision_agent() -> Agent:
    return Agent("gemini-1.5-flash", "Vision analysis prompt")

def create_ux_agent() -> Agent:
    return Agent("gemini-pro", "UX analysis prompt")

def create_market_agent() -> Agent:
    return Agent("gemini-pro", "Market analysis prompt")

def initialize_agents() -> Dict:
    return {
        "vision": create_vision_agent(),
        "ux": create_ux_agent(),
        "market": create_market_agent()
    } 