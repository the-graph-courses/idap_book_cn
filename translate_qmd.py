import os
import requests
from pathlib import Path
import local_settings

# API Configuration
OPENROUTER_API_KEY = local_settings.OPENROUTER_API_KEY
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Get all QMD files in the current directory that start with "p_"
current_dir = Path.cwd()
qmd_files = list(current_dir.glob("p_*.qmd"))

# Loop over each file with an index so you can inspect 'n'
for n in range(0,len(qmd_files)):
    file_path = qmd_files[n]
    print(f"\nProcessing file {n}: {file_path.name}")
    
    # Read original content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Prepare the prompt and request parameters
    prompt = (
        "Please translate the following QMD document to Chinese. \n"
        "Preserve all code blocks, YAML headers, and markdown formatting exactly as they are. \n"
        "Only translate the English text content. \n"
        "Return only the updated QMD without any prelude or commentary."
    )
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    
    data = {
        "model": "openai/o1-mini",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\n{content}"
            }
        ]
    }
    
    # Send request to the API for translation
    response = requests.post(API_URL, headers=headers, json=data)
    translated_content = response.json()["choices"][0]["message"]["content"]
    
    # Save the translated content to a new file
    new_filename = file_path.stem + "_cn" + file_path.suffix
    new_path = file_path.parent / new_filename
    
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(translated_content)
    
    print(f"Translated file saved as: {new_filename}")
