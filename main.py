from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# LangChain v1.2+ imports
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS (optional for testing/dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve .well-known folder for ai-plugin.json
app.mount(
    "/.well-known",
    StaticFiles(directory=os.path.join(os.getcwd(), "static", "well-known")),
    name="well-known",
)

# Serve openapi.json at root
@app.get("/openapi.json")
async def get_openapi():
    return FileResponse("openapi.json")

# Optional health check
@app.get("/ping")
def ping():
    return {"message": "pong"}

# ----------------------
# ✅ /ask Endpoint Setup
# ----------------------

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
    api_key=openai_api_key,
    temperature=0.7,
)

template = """
You are a helpful assistant helping someone reduce overwhelm and gain emotional clarity.

User question: {prompt}

Give a thoughtful, supportive, and actionable response.
"""

prompt_template = PromptTemplate(
    input_variables=["prompt"],
    template=template
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

# Request/response models
class AskRequest(BaseModel):
    user_id: str
    prompt: str

class AskResponse(BaseModel):
    response: str

# POST /ask endpoint
@app.post("/ask", response_model=AskResponse)
async def ask_route(payload: AskRequest):
    try:
        print(f"Prompt from {payload.user_id}: {payload.prompt}")
        llm_response = llm_chain.run(payload.prompt)
        return AskResponse(response=llm_response or "Sorry, no response was generated.")
    except Exception as e:
        print(f"Error in /ask: {e}")
        return AskResponse(response="Sorry, something went wrong processing your request.")
