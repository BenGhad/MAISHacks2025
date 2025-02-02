from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="Stock Bot")


# The HTML content for the Stock Bot
html_content = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Stock Bot</title>
  <style>
    /* Make sure the page fills the entire browser window */
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: Arial, sans-serif;
    }

    /* The background container for particles */
    #particles-js {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
    }

    body {
      background-color: #3D3D3D;
    }

    header {
      background: #9D00FF;
      color: #fff;
      padding: 20px;
      text-align: center;
    }

    main {
      padding: 40px;
      text-align: center;
    }

    a {
      text-decoration: none;
      color: #4a90e2;
      font-weight: bold;
    }

    .content-box {
      background: #AAA;
      max-width: 600px;
      margin: 20px auto;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }

    .content-box h1 {
      margin-top: 0;
    }

    .location-input {
      width: 60%;
      padding: 10px;
      margin: 10px 0;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 1rem;
    }

    .units-toggle {
      display: flex;
      justify-content: center;
      margin: 10px 0;
      gap: 20px;
    }

    .search-button {
      background: #4a90e2;
      color: #fff;
      border: none;
      border-radius: 5px;
      padding: 12px 20px;
      cursor: pointer;
      font-size: 1rem;
    }

    .search-button:hover {
      background: #3a78b2;
    }
  </style>
</head>
<body>
  <div id="particles-js"></div>

  <header>
    <h1>Weather Dashboard</h1>
  </header>

  <main>
    <div class="content-box">
      <h1>Weather</h1>
      <p>Check the current weather for any city in the world.</p>

      <input
        id="locationInput"
        class="location-input"
        type="text"
        placeholder="Enter a city (e.g., London)"
      />

      <div class="units-toggle">
        <label>
          <input type="radio" name="units" value="metric" checked />
          Metric (C)
        </label>
        <label>
          <input type="radio" name="units" value="imperial" />
          Imperial (F)
        </label>
      </div>

      <button class="search-button" onclick="redirectToWeather()">
        Get Weather
      </button>

      <p>
        Try checking
        <a href="/weather?location=Montreal">the weather in Montreal</a>.
      </p>
    </div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/particles.js"></script>

  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 60,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {"value": "#ffffff"},
        "shape": {"type": "circle"},
        "opacity": {
          "value": 0.5,
          "random": true
        },
        "size": {
          "value": 3,
          "random": true
        },
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
          "onhover": {"enable": true, "mode": "grab"},
          "onclick": {"enable": true, "mode": "repulse"},
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 200,
            "line_linked": {"opacity": 1}
          },
          "repulse": {
            "distance": 100,
            "duration": 0.4
          }
        }
      },
      "retina_detect": true
    });

    function redirectToWeather() {
      const locationInput = document.getElementById('locationInput').value.trim();
      const unitRadios = document.getElementsByName('units');
      let selectedUnit = 'metric';

      for (let i = 0; i < unitRadios.length; i++) {
        if (unitRadios[i].checked) {
          selectedUnit = unitRadios[i].value;
          break;
        }
      }

      if (!locationInput) {
        alert('Please enter a location!');
        return;
      }

      const url = `/weather?location=${encodeURIComponent(locationInput)}&unit=${selectedUnit}`;
      window.location.href = url;
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Returns the Weather Dashboard HTML page as the default route.
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/History",response_class=HTMLResponse)
async def get_value()






"""
##This is a web server to run FastAPI app
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
class Stock(BaseModel):
    name:str
class Wallet(BaseModel):
    wallet: List[Stock]


class PortfolioManager(BaseModel):
    riskTolerance: float
    budget: float
    walletPercentage: List[float]
    stocksHold: List[Stock]
class TradeDuration(BaseModel):
    startDate: str
    endDate: str
class UserChoice(BaseModel):
    tradeDuration: TradeDuration
    portfolioManager: PortfolioManager


app=FastAPI()
##Base origins/pts to call any end points on the server
origins ={
    "http://localhost:5173"
}
##Prevent unauthorized access to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_memory_db ={"stock": []}
@app.get("/wallet",response_model=Wallet)
def get_wallet():
    return Wallet(wallet=temp_memory_db["stock"])
@app.post("/wallet",response_model=Stock)
def add_stock(stock: Stock):
    temp_memory_db["stock"].append(stock)
    return stock


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""