import os
import requests
from dotenv import load_dotenv
def get_cik(ticker: str)-> str:
    ticker=ticker.upper()
    load_dotenv()
    user_agent_value=os.getenv("SEC_USER_AGENT")
    headers={
        "User-Agent": user_agent_value
    }
    url="https://www.sec.gov/files/company_tickers.json"
    response=requests.get(url, headers=headers)
    if response.status_code==200:
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
            return f"({ticker} does not exist)"
    else:
        return f"Failed to fetch data. Status code: {response.status_code}"

if __name__ == "__main__":
    print(get_cik("AAPL"))