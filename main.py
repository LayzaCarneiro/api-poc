from fastapi import FastAPI

app = FastAPI(
    title="Minha API POC",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "API online com sucesso"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"Usuario {user_id}"
    }