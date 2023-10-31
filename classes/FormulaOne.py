import requests

class FormulaOne:
    base_url = "http://ergast.com/api/f1/"
    
    def make_request(self, endpoint):
        url = f"{self.base_url}{endpoint}.json"
        return requests.get(url).json()
        