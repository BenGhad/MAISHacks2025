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
    result = ""
    for ticker in tickers:
        result += skibidi.predictNext(ticker) + " "
    return result


# ----------------------------
# Frontend Content(nice particles)
# ----------------------------
HTML_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Skibidi Scikit Stock Bot</title>
  <style>
    /* Global Reset */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    html, body {
      height: 100%;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      color: #333;
    }

    /* Particle background container */
    #particles-js {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      background-color: #3D3D3D; /* Dark gray background */
    }

    /* Header Styling */
    header {
      background-color: #1C1C1C;
      padding: 20px;
      text-align: center;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }
    header h1 {
      color: #fff;
      font-size: 2rem;
    }
    main {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 40px 20px;
      min-height: calc(100% - 80px); 
    }

    .content-box {
      background: #fff;
      max-width: 900px;
      width: 100%;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }

    .input-section {
      flex: 1;
      min-width: 280px;
    }
    .input-section label {
      display: block;
      margin: 15px 0 5px;
      font-size: 0.9rem;
      font-weight: bold;
      color: #555;
    }
    .input-section input[type="text"],
    .input-section input[type="date"] {
      width: 100%;
      padding: 12px;
      font-size: 1rem;
      border: 1px solid #ddd;
      border-radius: 5px;
      margin-bottom: 15px;
    }

    .action-section {
      flex: 1;
      min-width: 280px;
      display: flex;
      flex-direction: column;
      gap: 30px;
    }
    .action-block {
      background: #F8F8F8;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .action-block button {
      background-color: #1C1C1C;
      color: #fff;
      border: none;
      border-radius: 5px;
      padding: 12px 20px;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.3s ease;
      width: 100%;
    }
    .action-block button:hover {
      background-color: #333;
    }
    .action-desc {
      margin-top: 10px;
      font-size: 0.9rem;
      line-height: 1.4;
      color: #555;
    }
    .result-box {
      margin-top: 15px;
      padding: 12px;
      background: #F2F2F2;
      border: 1px solid #ddd;
      border-radius: 5px;
      min-height: 40px;
      font-size: 0.95rem;
      text-align: left;
    }
  </style>
</head>
<body>
  <!-- Particle Background -->
  <div id="particles-js"></div>
  <header>
    <h1>Stock Predictor</h1>
  </header>

  <main>
    <div class="content-box">
      <!-- Left Column: Inputs --> 
      <div class="input-section">
        <label for="tickersInput">Enter Stocks (space-separated):</label>
        <input type="text" id="tickersInput" placeholder="e.g. AAPL MSFT GOOG" />

        <label for="startDateInput">Start Date:</label>
        <input type="date" id="startDateInput" />

        <label for="endDateInput">End Date:</label>
        <input type="date" id="endDateInput" />
      </div>

      <div class="action-section">
        <!-- Action Block 1: Daily Prediction -->
        <div class="action-block">
          <button onclick="handleDailyPrediction()">Daily Prediction</button>
          <p class="action-desc">
            For each ticker and for each day within the selected range, this action sends ticker data to our model. The model predicts whether to buy, sell, or hold, and returns an estimated profit for these tickers.
          </p>
          <div id="outputBox" class="result-box">Output goes here...</div>
        </div>
        <!-- Action Block 2: Tomorrow Hold Prediction -->
        <div class="action-block">
          <button onclick="handleTomorrowPrediction()">Hold Until Tomorrow</button>
          <p class="action-desc">
            For each ticker, our model determines if it is advisable to hold until tomorrow. The response is:
            <br>• 1: Yes
            <br>• -1: No
            <br>• 0: Yes if you have a high risk tolerance.
          </p>
          <div id="answerBox" class="result-box">Answer goes here...</div>
        </div>
        <!-- Action Block 3: 1-Year Price Plot -->
        <div class="action-block">
            <button onclick="handlePlot()">Plot 1-Year History</button>
            <p class="action-desc">
            This action retrieves and plots the past year's closing prices for the first ticker you entered.
            </p>
         <div class="result-box">
        <img id="plotBox" style="max-width:100%;" alt="Plot will appear here" />
        </div>
        </div>

      </div>
    </div>
  </main>

  <!-- Extra JS -->
  <script>
  async function handleDailyPrediction() {
    const tickers = document.getElementById("tickersInput").value;
    const startDate = document.getElementById("startDateInput").value;
    const endDate = document.getElementById("endDateInput").value;

    try {
      const response = await fetch("/start", {  // Changed from "/daily" to "/start"
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tickers, startDate, endDate })
      });
      const data = await response.json();
      document.getElementById("outputBox").innerText = data.result;
    } catch (error) {
      document.getElementById("outputBox").innerText = "Error: " + error;
    }
  }

  async function handleTomorrowPrediction() {
    const tickers = document.getElementById("tickersInput").value;

    try {
      const response = await fetch("/next", {  // Changed from "/tomorrow" to "/next"
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tickers })
      });
      const data = await response.json();
      if (Array.isArray(data.result)) {
        document.getElementById("answerBox").innerText = data.result.join(", ");
      } else {
        document.getElementById("answerBox").innerText = data.result;
      }
    } catch (error) {
      document.getElementById("answerBox").innerText = "Error: " + error;
    }
  }
  
   async function handlePlot() {
    const tickerString = document.getElementById("tickersInput").value.trim();

    // Validate input
    if (!tickerString) {
      alert("No Ticker Specified");
      return;
    }

    // Just take the first ticker if multiple are provided
    const ticker = tickerString.split(/\s+/)[0];

    try {
      const response = await fetch("/plot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker: ticker })
      });

      // Parse the response
      const data = await response.json();
      if (data.image) {
        document.getElementById("plotBox").src = 'data:image/png;base64,' + data.image;
      }
      else if (data.error) {
        alert("Error: " + data.error);
        document.getElementById("plotBox").src = "";
      }
    } catch (error) {
      alert("Error: " + error);
      document.getElementById("plotBox").src = "";
    }
  }
</script>
  <!-- Load particles.js library from CDN -->
  <script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
  
  <!-- Initialize particles.js -->
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 60,
          "density": { "enable": true, "value_area": 800 }
        },
        "color": { "value": "#ffffff" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5, "random": true },
        "size": { "value": 3, "random": true },
        "line_linked": {
          "enable": true,
          "distance": 150,
          "color": "#ffffff",
          "opacity": 0.5,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 2,
          "direction": "none",
          "random": true,
          "straight": false,
          "out_mode": "out"
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": { "enable": true, "mode": "grab" },
          "onclick": { "enable": true, "mode": "repulse" },
          "resize": true
        },
        "modes": {
          "grab": { "distance": 200, "line_linked": { "opacity": 1 } },
          "repulse": { "distance": 100, "duration": 0.4 }
        }
      },
      "retina_detect": true
    });
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


@app.post("/plot")
async def plot_endpoint(request: Request):
    body = await request.json()
    ticker = body.get("ticker", "").strip()
    if not ticker:
        return JSONResponse(content={"error": "No ticker specified"}, status_code=400)
    return JSONResponse(content={"image": skibidi.plotGraph(ticker)})


# ----------------------------
# Run the server
# ----------------------------
if __name__ == "__main__":
    uvicorn.run("newMain:app", host="127.0.0.1", port=8000, reload=True)
