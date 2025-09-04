import os
import requests
import json
import base64
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class ImageGenerationInput(BaseModel):
    """Input schema for ImageGenerationTool."""
    prompt: str = Field(..., description="Detailed description of the image to generate.")
    filename: str = Field(..., description="Filename to save the generated image (without extension).")
    style: str = Field("digital art", description="Style of the image (e.g., digital art, photo, cartoon).")
    aspect_ratio: str = Field("1:1", description="Aspect ratio of the image (e.g., '1:1', '16:9', '4:3').")

class ImageGenerationTool(BaseTool):
    name: str = "Image Generation Tool"
    description: str = (
        "Generates images using ChatGPT's DALL-E API based on detailed text prompts. "
        "The tool creates images for game elements like backgrounds, characters, and UI components."
    )
    args_schema: Type[BaseModel] = ImageGenerationInput
    api_key: str=None
    
    def __init__(self, api_key="API_KEY"):
        super().__init__()
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key is required for image generation.")
        
        # Create directories if they don't exist
        os.makedirs("game_outputs/images", exist_ok=True)

    def _run(self, prompt: str, filename: str, style: str = "digital art", aspect_ratio: str = "1:1") -> str:
        """Generate an image using the OpenAI API and save it to disk."""
        try:
            # Map aspect ratios to OpenAI's size parameter
            aspect_ratio_map = {
                "1:1": "1024x1024",
                "16:9": "1792x1024",
                "4:3": "1024x768",
                "3:4": "768x1024",
                "9:16": "1024x1792"
            }
            
            size = aspect_ratio_map.get(aspect_ratio, "1024x1024")
            
            # Enhance prompt with style
            enhanced_prompt = f"{prompt}, {style}, high quality, game asset"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "dall-e-3",
                "prompt": enhanced_prompt,
                "n": 1,
                "size": size,
                "response_format": "b64_json"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                response_data = response.json()
                image_data = response_data["data"][0]["b64_json"]
                
                # Save the image to disk
                file_path = f"game_outputs/images/{filename}.png"
                with open(file_path, "wb") as image_file:
                    image_file.write(base64.b64decode(image_data))
                
                return f"Image successfully generated and saved to {file_path}"
            else:
                return f"Error generating image: {response.text}"
                
        except Exception as e:
            return f"Error generating image: {str(e)}"