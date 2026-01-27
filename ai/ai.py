from google import genai
import os

# Create Gemini client (NEW SDK)
client = genai.Client(
    api_key=os.getenv("AIzaSyCg0m2d_Y2Nql8d5FkHti_Rc7cupFRw1bs")  # NEVER hardcode
)

# Generate response
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="How does AI work in simple words?"
)

print(response.text)


'''client = genai.Client(api_key="AIzaSyCg0m2d_Y2Nql8d5FkHti_Rc7cupFRw1bs")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="How does AI work?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig()
    ),
)
print(response.text)'''