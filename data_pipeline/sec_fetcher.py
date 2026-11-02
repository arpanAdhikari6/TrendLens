import os
import requests
from dotenv import load_dotenv
import pandas as pd 
def sec_headers():
    load_dotenv()
    user_agent_value=os.getenv("SEC_USER_AGENT")
    if not user_agent_value:
        raise ValueError("SEC_USER_AGENT value missing or is empty")
    return {"User-Agent": user_agent_value}
def get_cik(ticker: str)-> str:
    ticker=ticker.upper()
    url="https://www.sec.gov/files/company_tickers.json"
    response=requests.get(url, headers=sec_headers(), timeout=10)
    response.raise_for_status()
    tickers_data=response.json()
    found_ticker=None
    for item in tickers_data.values():
        if item.get("ticker")== ticker:
            found_ticker=item.get("ticker")
            found_cik=item.get("cik_str")
            break
    if found_ticker:
        return f"{found_cik:010d}"
    else:
        raise ValueError(f"{ticker} not found in SEC data")
def get_company_Facts(cik:str)->dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response=requests.get(url, headers=sec_headers(), timeout=10)
    response.raise_for_status()
    company_facts_data=response.json()
    return company_facts_data
if __name__ == "__main__":
    cik = get_cik("AAPL")
    facts = get_company_Facts(cik)
    print(facts["entityName"])
    revenue = facts["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
    print(revenue[-1])