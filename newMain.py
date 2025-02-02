# main.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn
import backend.model.model_trainer as model_trainer
import backend.model.preidctor as skibidi


app = FastAPI()



def start(startDate: str, endDate: str, tickers: list) -> int:
    return skibidi.start(startDate, endDate, list)

def next(tickers: list) -> list:
    buys = []
    for ticker in tickers:
        buys.append(skibidi.predictNext(ticker))
    return buys




@app.get("/", response_class=HTMLResponse)
async def index():
    # Initial page with an empty output box.
    html_content = html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Stock Predictor</title>
</head>
<body>
    <h1>Stock Predictor</h1>
    
    <div>
        <label for="tickersInput">Tickers (space-separated):</label><br>
        <input type="text" id="tickersInput" placeholder="AAPL TSLA MSFT" style="width:300px;">
    </div>
    <br>
    
    <div>
        <label for="startDate">Start Date:</label><br>
        <input type="date" id="startDate" />
    </div>
    <br>

    <div>
        <label for="endDate">End Date:</label><br>
        <input type="date" id="endDate" />
    </div>
    <br>

    <button onclick="callStart()">Call Start</button>
    <button onclick="callNext()">Call Next</button>

    <hr>

    <!-- Output box -->
    <div id="outputBox" style="border:1px solid #ccc; padding:10px; min-height:50px;">
        <!-- Results will appear here -->
    </div>

    <!-- JavaScript to handle button clicks and fetch calls -->
    <script>
        async function callStart() {
            const tickers = document.getElementById("tickersInput").value;
            const startDate = document.getElementById("startDate").value;
            const endDate = document.getElementById("endDate").value;

            try {
                const response = await fetch("/start", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ 
                        tickers: tickers,
                        startDate: startDate,
                        endDate: endDate
                    })
                });

                if (!response.ok) {
                    throw new Error(`Server error: ${response.statusText}`);
                }

                const data = await response.json();
                document.getElementById("outputBox").innerText = JSON.stringify(data, null, 2);
            } catch (error) {
                console.error(error);
                document.getElementById("outputBox").innerText = "Error: " + error.message;
            }
        }

        async function callNext() {
            const tickers = document.getElementById("tickersInput").value;

            try {
                const response = await fetch("/next", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        tickers: tickers
                    })
                });

                if (!response.ok) {
                    throw new Error(`Server error: ${response.statusText}`);
                }

                const data = await response.json();
                document.getElementById("outputBox").innerText = JSON.stringify(data, null, 2);
            } catch (error) {
                console.error(error);
                document.getElementById("outputBox").innerText = "Error: " + error.message;
            }
        }
    </script>
</body>
</html>

"""


if __name__ == "__main__":
    # Run the app with: python main.py
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
