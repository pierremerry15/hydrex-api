#we need to build a simple restapi using fastapi
#api will allow us to get the info about a user 
#info includes their total baalnce along with list of their accounts 
#each account will include the type of token along w dollar value 
#no real data base bevause it is a 'stub' 

#approach 
#import libraries 
#fast api will be used to created the web abi 
#pydantic basemodel will eb used to define our data and what it should look like
#list will be used to define arrays of items j like a list of accounts 


from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

# Create an instance of the FastAPI application
app = FastAPI()

# Defines the data model for an acc
# Each account stores its type, token symbol, and dollar value

class Account(BaseModel):
    account_type: str     # ie: "Flex" or "Liquid"
    token: str            # Token symbol like USDC, ETH, HYDX
    value: float          # Dollar amount in this account

# Define the data model for a user
# Includes user ID, total balance, and a list of their accounts

class User(BaseModel):
    user_id: str                  # Unique user identifier
    total_balance: float          # Combined balance across all accounts
    accounts: List[Account]       # List of account objects

# Simulated in-memory user database
# This is mock data — no real database is used

fake_user_db = {
    "user123": User(
        user_id="user123",
        total_balance=108126.00,
        accounts=[
            Account(account_type="Flex", token="USDC", value=10126.00),
            Account(account_type="Flex", token="HYDX", value=1032.00),
            Account(account_type="Liquid", token="ETH", value=97000.00)
        ]
    )
}

# Root endpoint that welcomes the user
# Helpful if someone lands on the base URL

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hydrex API"}

# Endpoint to get full user data by user_id
# This returns the total balance and all account details

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = fake_user_db.get(user_id)
    if not user:
        return {"error": "User not found"}
    return user

# Homepage endpoint
# Returns a summary view similar to a dashboard
# Includes total balance, estimated weekly earning, and account/token breakdown

@app.get("/homepage")
def homepage(user_id: str = Query(...)):
    user = fake_user_db.get(user_id)
    if not user:
        return {"error": "User not found"}

    # Estimate weekly earning as 6.5% of total balance (example logic)
    weekly_earning = round(user.total_balance * 0.065, 2)

    # Create a dictionary summarizing token balances
    token_holdings = {acc.token: acc.value for acc in user.accounts}

    # Return structured dashboard-like data
    return {
        "user_id": user.user_id,
        "total_balance": user.total_balance,
        "weekly_earning": weekly_earning,
        "accounts": [
            {
                "account_type": acc.account_type,
                "token": acc.token,
                "value": acc.value
            }
            for acc in user.accounts
        ],
        "token_holdings": token_holdings,
        "back_to_homepage": f"/homepage?user_id={user.user_id}"
    }
