import uvicorn
import sys
import io

# Force UTF-8 encoding for console logs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

if __name__ == "__main__":
    print("Starting FastAPI Scribe backend...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="info")
