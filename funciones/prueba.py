from google import genai

client = genai.Client(api_key="AIzaSyDKhuur3D2GcsxVUY9JWHm8hMHEYfhth2U")

print("Modelos disponibles para tu clave:")
for model in client.models.list():
    print(f"- {model.name}")