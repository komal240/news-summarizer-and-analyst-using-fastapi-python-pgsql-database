from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import query
from openai import OpenAI
import logging
import traceback

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class newsRequest(BaseModel):
    news:str

@app.get("/")
async def home():
    return JSONResponse(content={"message": "Working Fine"})


@app.post("/analyze")
async def get_ingredients(data:newsRequest):
    news = data.news
    updnews = query("SELECT * FROM sa WHERE news = %s", (news,))
    logger.info(f"Query result: {updnews}")
    if len(updnews) > 0: 
        steps_from_db = updnews[0][2].split("\n")
        return JSONResponse(content={"message": "Data from DB", "summary": steps_from_db})
    else:
        try:
            gemini_key = "AIzaSyAdfD6yDtOF6vbmoxVvtHcuG4SVPTMx_fg"
            client = OpenAI(
                api_key=gemini_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )

            response = client.chat.completions.create(
                model="gemini-2.5-flash",
               messages = [
                 {"role": "system", "content": "You are an expert news summarizer and analyst. Focus on Maharashtra local news."},
                 {"role": "user", "content": f"Summarize and analyze the following news article:\n\n{news}"}
                   ] 

            )

            result_text = response.choices[0].message.content
            summery_analysis = result_text.split("\n")

            if not summery_analysis:
                return JSONResponse(content={"message": "No news found for this recipe"})


            summery_analysis = "\n".join(summery_analysis)
            query("INSERT INTO sa (news, summery_analysis) VALUES (%s, %s)", (news,summery_analysis))
        
            return {"message": "Data fetched from Gemini API", "summary":summery_analysis}

        except Exception as e:
         logger.error(traceback.format_exc())
         return JSONResponse(content={"message": "Error fetching data", "error": str(e)})