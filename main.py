#we need to build a sim[ple restapi using fastapi
#api will allow us to get the info about a user 
#info includes their total baalnce along with list of their accounts 
#each account will include the type of token along w dollar value 
#no real data base bevause it is a 'stub' 

#approach 
#import libraries 
#fast api will be used to created the web abi 
#pydantic basemodel will eb used to define our data and what it should look like
#list will be used to define arrays of items j like a list of accounts 


from fastapi import FastAPI #importing fastapi to create the web application
from pydantic import BaseModel
from typing import List 

app = FastAPI() #creates an instance of the fastapi class

#we need to define the structure of the account 
class Account(BaseModel):
    account_type: str #this is the type of token
    token: str 
    value: float #amount of money in the account 

#define the structure of the user 
#want to implmemnent the users ID, total balance along w a list of accounts 
class User(BaseModel):
    user_id: str 
    total_balance: float 
    accounts: List[Account] 

#we need to import the baseModel and list for creating the data moeks 

#make the fake data 

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


# we need tro define an API endpoint/"route" to get user data
# When someone visits /users/user123, this function will run
# It looks up the user from the fake database and returns their info
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    # Look up the user in the fake database
    user = fake_user_db.get(user_id)

    # If the user isn't found return an error message
    if not user:
        return {"error": "User not found"}

    # If the user is found, return their data here the fastapi will turn into json
    return user