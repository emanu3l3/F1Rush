from .FormulaOne import FormulaOne
from cache import cache

class Rankings(FormulaOne):
    def __init__(self):
        # initialize cache
        cache.set("drivers_ranking_year", {})
        cache.set("drivers_ranking", {})
        
    def get_drivers_ranking_by_year(self, year):
        # get driver's ranking by year
        ranking_cache = cache.get("drivers_ranking_year")
        drivers_ranking = []
        
        #fetch data
        ranking_list = FormulaOne.make_request(self, f"{year}/driverStandings")["MRData"]["StandingsTable"]["StandingsLists"]

        # organize data
        for rank in ranking_list:
            for driver_rank in rank["DriverStandings"]:
                drivers_ranking.append({
                    "position": driver_rank["position"],
                    "points": driver_rank["points"],
                    "driver_name": driver_rank["Driver"]["givenName"],
                    "driver_surname": driver_rank["Driver"]["familyName"],
                    "team": driver_rank["Constructors"][0]["name"]
                })
        ranking_cache[year] = drivers_ranking  
       
        #cache data      
        cache.set("drivers_ranking_year", ranking_cache)
    
    def get_driver_ranking_by_driver_id(self, driver_id):
        # get driver ranking by driver id
        drivers_ranking_cache = cache.get("drivers_ranking")
        
        # fetch data
        ranking_list = FormulaOne.make_request(self, f"drivers/{driver_id}/driverStandings")["MRData"]["StandingsTable"]["StandingsLists"]
        
        # organize data
        driver_ranking = [
            {
                "season": ranking["season"],   
                "position": ranking["DriverStandings"][0]["position"],     
                "points": ranking["DriverStandings"][0]["points"],  
                "wins": ranking["DriverStandings"][0]["wins"],
                "team": ranking["DriverStandings"][0]["Constructors"][0]["name"]
            }
            for ranking in ranking_list
        ]
        drivers_ranking_cache[driver_id] = driver_ranking
        
        # cache data
        cache.set("drivers_ranking", drivers_ranking_cache)
    