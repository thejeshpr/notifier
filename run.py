import uvicorn 

from dotenv import load_dotenv

load_dotenv(verbose=True)

if __name__ == "__main__":
    uvicorn.run(
            "notifier:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            debug=True,
            workers=1
        )