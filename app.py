from flask import Flask, request, flash, render_template, abort
from classes.Drivers import Drivers
from classes.Races import Races
from classes.Rankings import Rankings
from cache import cache
import time, math

app = Flask(__name__)
cache.init_app(app, config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 0,
    "CACHE_THRESHOLD" : math.inf
})

app.secret_key = b'secret'

drivers_inst = Drivers()
races_inst = Races()
rankings_inst = Rankings()

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")

@app.get("/")
def index():
    next_races = cache.get("next_races")
    try:
        if next_races is None:
            races_inst.get_season_races()
        next_races = cache.get("next_races") 

        return render_template("index.html", next_races=next_races)
    except:
        abort(404)

@app.get("/drivers")
def drivers():
    try:    
        year = request.args.get("year", "2023")
        if int(year) < 1950 or int(year) > 2023:
            flash("INVALID YEAR")
        elif cache.get("drivers_year").get(year) is None:
            drivers_inst.get_drivers_by_year(year)
                
        drivers = cache.get("drivers_year").get(year)
        return render_template("drivers.html", drivers=drivers, year=year)
    except:
        abort(404)

@app.get("/drivers/<driver_id>/")
def driver(driver_id):
    driver_info = cache.get("drivers").get(driver_id)
    driver_exist = True
    try:
        if driver_info is None:
            driver_exist = drivers_inst.get_driver_by_driver_id(driver_id)

        if driver_exist:
            if cache.get("drivers_ranking").get(driver_id) == None:
                time.sleep(2)
                rankings_inst.get_driver_ranking_by_driver_id(driver_id)

            driver_info = cache.get("drivers").get(driver_id)
            driver_ranking = cache.get("drivers_ranking").get(driver_id)
        else:
            driver_info, driver_ranking = {}, {}
            flash("THE DRIVER DOESN'T EXIST")    

        return render_template("driver.html", driver_info=driver_info, driver_ranking=driver_ranking)
    except:
        abort(404)
    
@app.get("/rankings")
def rankings():
    year = request.args.get("year", "2023")
    try:
        if int(year) < 1950 or int(year) > 2023:
            flash("INVALID YEAR")
        elif cache.get("drivers_ranking_year").get(year) is None:
            rankings_inst.get_drivers_ranking_by_year(year)

        ranking = cache.get("drivers_ranking_year").get(year, {})
        return render_template("rankings.html", ranking=ranking, year=year)
    except:
        abort(404)   
    
@app.get("/races")
def races():    
    race_result_exist = True
    race_round = request.args.get("round", "1")
    try:
        if cache.get("prev_races") is None:
            races_inst.get_season_races()
            
        if cache.get("race_results").get(race_round) is None:
            race_result_exist = races_inst.get_race_result_by_round(race_round)
        
        if race_result_exist == False:
            flash("THE RACE HAS NOT BEEN UPLOADED YET")
        
        prev_races = cache.get("prev_races")
        race_results = cache.get("race_results").get(race_round, {})
        return render_template("races.html", prev_races=prev_races, race_results=race_results)
    except:
       abort(404) 
       
