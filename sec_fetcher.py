import os
import requests
from dotenv import load_dotenv
def get_cik(ticker: str)-> str:
    ticker=ticker.upper()
    load_dotenv()
    user_agent_value=os.getenv("SEC_USER_AGENT")
    if not user_agent_value:
        raise ValueError("SEC_USER_AGENT value missing or is empty")
    headers={
        "User-Agent": user_agent_value
    }
    url="https://www.sec.gov/files/company_tickers.json"
    response=requests.get(url, headers=headers, timeout=10)
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
if __name__ == "__main__":
    print(get_cik("mib"))