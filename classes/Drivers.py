from .WikiImgs import WikiImgs
from .FormulaOne import FormulaOne
from cache import cache

class Drivers(FormulaOne):
    def __init__(self):
        # initialize cache
        cache.set("drivers_year", {})
        cache.set("drivers", {})
        
    def get_drivers_by_year(self, year):
        # get the drivers by year
        drivers = FormulaOne.make_request(self, f"{year}/drivers")["MRData"]["DriverTable"]["Drivers"]
        
        drivers_cache = cache.get("drivers")
        drivers_year_cache = cache.get("drivers_year")
        drivers_year = {}
        
        # get drivers images
        wikiImgs = WikiImgs([driver.get("url") for driver in drivers], 250)
        driver_imgs_urls = wikiImgs.get_images()
        
        # organize data
        for driver in range(len(drivers)):
            drivers[driver]["url"] = driver_imgs_urls[driver]
            driver_id = drivers[driver]["driverId"]
            
            drivers_year[driver_id] = {
                "driver_id": drivers[driver]["driverId"],
                "given_name": drivers[driver]["givenName"],
                "family_name": drivers[driver]["familyName"],
                "url": drivers[driver]["url"]
            }
            if driver_id not in drivers_cache:
                drivers_cache[driver_id] = drivers[driver]
        
        # cache data     
        cache.set("drivers", drivers_cache)
        drivers_year_cache[year] = drivers_year
        cache.set("drivers_year", drivers_year_cache)
      
      
    def get_driver_by_driver_id(self, driver_id):
        # get driver info by driver id
        drivers_cache = cache.get("drivers")
        try:
            # fetch data
            driver_info = FormulaOne.make_request(self, f"drivers/{driver_id}")["MRData"]["DriverTable"]["Drivers"]

            # get driver image
            wikiImgs = WikiImgs([driver_info[0].get("url")], 350)
            driver_img_url = wikiImgs.get_images()

            #organize data
            driver_info[0]["url"] = driver_img_url[0]
            driver_id = driver_info[0].get("driverId")
            drivers_cache[driver_id] = driver_info[0]
            
            #cache data
            cache.set("drivers", drivers_cache) 
            return True
        except:
            return False
