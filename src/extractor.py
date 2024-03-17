from requests import get

class Extractor:

    def __init__(self) -> None:
        self.base_url = "https://stockanalysis.com/stocks/{ticker}"
        self.responses = []

    # extracts data from the source endpoint 
    # returns unprocessed data for further processing
    def extract(self, tickers: list[str]) -> list[str]:
        for ticker in tickers:
            response = get(self.base_url.format(ticker=ticker)).text
            self.responses.append(response)
        return self.responses

class ExtractorAsync:
    pass