import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from PIL import Image
from google import genai   # ✅ NEW SDK

load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""

    if request.method == 'POST':
        image = request.files['image']

        if image:
            img = Image.open(image)

            prompt = "Describe this image in detail."

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",   # ✅ Latest stable model
                    contents=[prompt, img]
                )

                response_text = response.text

            except Exception as e:
                response_text = "API quota exceeded or service temporarily unavailable. Please try again later."

    return render_template('index.html', response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
