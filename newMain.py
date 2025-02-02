from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

# ----------------------------
# Import trainer/predictor
# ----------------------------
import backend.model.model_trainer as model_trainer
import backend.model.preidctor as skibidi

app = FastAPI(Title="Skibidi Scikit Stock Bot")

# ----------------------------
# Functions
# ----------------------------
def start(startDate: str, endDate: str, tickers: list) -> int:
    return skibidi.start(startDate, endDate, tickers)

def next_prediction(tickers: list) -> list:
    return [skibidi.predictNext(ticker) for ticker in tickers]

# ----------------------------
# HTML content (pure HTML/CSS/JS)
# ----------------------------
HTML_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Predictor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 30px;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
        }
        label, input, button {
            display: block;
            margin: 10px 0px;
        }
        #outputBox, #answerBox {
            margin: 20px 0;
            border: 1px solid #ccc;
            min-height: 40px;
            padding: 10px;
        }
        button {
            cursor: pointer;
            padding: 8px 16px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Stock Predictor</h1>

    <label for="tickersInput">Enter Stocks (space-separated):</label>
    <input type="text" id="tickersInput" placeholder="e.g. AAPL MSFT GOOG" />

    <label for="startDateInput">Start Date:</label>
    <input type="date" id="startDateInput" />

    <label for="endDateInput">End Date:</label>
    <input type="date" id="endDateInput" />

    <button onclick="handleStart()">Start</button>
    <div id="outputBox">Output goes here...</div>

    <button onclick="handleNext()">Next</button>
    <div id="answerBox">Answer goes here...</div>
</div>

<script>
    async function handleStart() {
        const tickers = document.getElementById("tickersInput").value;
        const startDate = document.getElementById("startDateInput").value;
        const endDate = document.getElementById("endDateInput").value;

        try {
            const response = await fetch("/start", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    tickers: tickers,
                    startDate: startDate,
                    endDate: endDate
                })
            });
            const data = await response.json();
            document.getElementById("outputBox").innerText = data.result;
        } catch (error) {
            document.getElementById("outputBox").innerText = "Error: " + error;
        }
    }

    async function handleNext() {
        const tickers = document.getElementById("tickersInput").value;

        try {
            const response = await fetch("/next", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({tickers: tickers})
            });
            const data = await response.json();
            // If it's a list, join the results in some display-friendly way
            if (Array.isArray(data.result)) {
                document.getElementById("answerBox").innerText = data.result.join(", ");
            } else {
                document.getElementById("answerBox").innerText = data.result;
            }
        } catch (error) {
            document.getElementById("answerBox").innerText = "Error: " + error;
        }
    }
</script>
</body>
</html>
"""

# ----------------------------
# Routes
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def read_home():
    return HTMLResponse(content=HTML_content, status_code=200)


@app.post("/start")
async def start_endpoint(request: Request):
    body = await request.json()
    # Split space-separated tickers
    tickers = body["tickers"].split() if "tickers" in body else []
    start_date = body.get("startDate", "")
    end_date = body.get("endDate", "")
    try:
        result = start(start_date, end_date, tickers)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/next")
async def next_endpoint(request: Request):
    body = await request.json()
    # Split space-separated tickers
    tickers = body["tickers"].split() if "tickers" in body else []
    try:
        result = next_prediction(tickers)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# ----------------------------
# Run the server
# ----------------------------
if __name__ == "__main__":
    uvicorn.run("newMain:app", host="127.0.0.1", port=8000, reload=True)
