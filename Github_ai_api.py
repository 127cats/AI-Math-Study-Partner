#This Page is for your API
from zhipuai import ZhipuAI
import base64

API_KEY = "" #Insert your API Key Here
client = ZhipuAI(api_key=API_KEY)

def ask_math(question, image_path=None):
    try:
        messages = [
            {"role": "system", "content": "You are an expert math tutor. Look at the image carefully and solve the specific problem mentioned by the user. Show step-by-step calculations. Use plain text like x^2, do NOT use $ or LaTeX. Answer in English."}
            #This code is the command prompt you give the model. Feel free to modify it to your needs!
        ]
        
        if image_path:
            with open(image_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')
            
            content = [
                {"type": "text", "text": question if question else "Please solve the math problem in this image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
            messages.append({"role": "user", "content": content})
            
            model_name = "glm-4v-flash"
        else:
            messages.append({"role": "user", "content": question})
            model_name = "glm-4-flash"
        
        print(f"DEBUG: Using model = {model_name}, has_image = {image_path is not None}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"API Error: {e}"