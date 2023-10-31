from datetime import datetime
from .WikiImgs import WikiImgs
from .FormulaOne import FormulaOne
from cache import cache

class Races(FormulaOne):
    def __init__(self):
        # initialize cache
        cache.set("race_results", {})
    
    def get_season_races(self):
        #get the season races based on the date of the day         
        next_races = []
        next_races_wiki_urls = []
        prev_races = {}
        todays_date = datetime.now().date()
        # fetch data
        races = FormulaOne.make_request(self, "2023")["MRData"]["RaceTable"]["Races"]
        # organize data 
        for race in races:
            if datetime.strptime(race["date"], "%Y-%m-%d").date() > todays_date:
                next_races.append({
                    "race_name": race["raceName"],
                    "circuit_name": race["Circuit"]["circuitName"],
                    "race_locality": race["Circuit"]["Location"]["locality"],
                    "race_country": race["Circuit"]["Location"]["country"],
                    "race_date": race["date"],
                    "race_time": race["time"]
                })
                next_races_wiki_urls.append(race["Circuit"]["url"])
            else:
                prev_races[race["round"]] = {race["round"]: race["raceName"]}

        # get races images
        wikiImgsRaces = WikiImgs(next_races_wiki_urls, 350)
        next_races_imgs_urls = wikiImgsRaces.get_images()
        
        for next_race in range(len(next_races)):
            next_races[next_race]["url"] = next_races_imgs_urls[next_race]
        
        # calculating how long to cache races 
        next_race_date = datetime.strptime(next_races[0].get("race_date"), "%Y-%m-%d").date()
        days_left_for_race = (next_race_date-todays_date)
        second_left_for_race = days_left_for_race.days*86400
        
        print(next_races)
        # cache data   
        cache.set("next_races", next_races, second_left_for_race)
        cache.set("prev_races", prev_races, second_left_for_race)
    
    def get_race_result_by_round(self, race_round):
        # get the race results by round
        race_results_cache = cache.get("race_results")
        try:
            results = FormulaOne.make_request(self, f"2023/{race_round}/results")["MRData"]["RaceTable"]["Races"][0]["Results"]
            race_results = [
                {
                    "position": result["position"], 
                    "driver_name": result["Driver"]["givenName"],     
                    "driver_surname": result["Driver"]["familyName"],     
                    "points": result["points"],       
                    "grid": result["grid"],       
                    "laps": result["laps"],       
                    "status": result["status"],       
                    "a_speed": result.get("FastestLap", {}).get("AverageSpeed", {}).get("speed")        
                }
                for result in results
            ]
            race_results_cache[race_round] = race_results
            cache.set("race_results", race_results_cache)
            return True
        except:
            return False
        
           