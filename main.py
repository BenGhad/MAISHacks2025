

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
    "http://localhost:3000"
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