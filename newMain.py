from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# Import the function 'start' from your preidctor.py module
# (Make sure that your PYTHONPATH is set appropriately so that 'backend.model.preidctor' is importable)
import backend.model.preidctor
import backend.model.model_trainer

app = FastAPI()

# Set up Jinja2 templates; ensure the templates folder is in the same directory as newMain.py.
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    # Render the form with no result initially.
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def process_form(
    request: Request,
    start_date: str = Form(...),
    end_date: str = Form(...),
    tickers: str = Form(...)
):
    # Convert the comma-separated tickers string into a list,
    # stripping any extra whitespace.
    tickers_list = [ticker.strip() for ticker in tickers.split(",") if ticker.strip()]

    # Call your 'start' function with the provided dates and tickers.
    result = start(start_date, end_date, tickers_list)

    # Render the form again, now including the result.
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "start_date": start_date,
            "end_date": end_date,
            "tickers": tickers,
        }
    )

# If running this module directly, use Uvicorn to serve the app.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
