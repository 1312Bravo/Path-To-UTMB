import pandas as pd
import requests
import warnings

from helper_functions.common import time_to_hours

# -------------------------------------------------
# Get UTMB LIVE API access token
# -------------------------------------------------

def get_utmb_live_access_token(
        utmb_username: str, 
        utmb_password: str
    ) -> str:

    login_data = {
        "grant_type": "password",
        "client_id": "utmb-world",
        "username": utmb_username,
        "password": utmb_password,
        "scope": "openid profile email"
    }

    res = requests.post("https://accounts.utmb.world/auth/realms/utmb-world/protocol/openid-connect/token", data=login_data)
    token_data = res.json()
    access_token = token_data["access_token"]

    return access_token

# -------------------------------------------------
# Get UTMB API access token
# -------------------------------------------------

def get_utmb_access_token(
        utmb_username: str, 
        utmb_password: str
    ) -> str:

    url = "https://accounts.utmb.world/auth/realms/utmb-world/protocol/openid-connect/token"

    payload = {
        "grant_type": "password",
        "client_id": "utmb-world",
        "username": utmb_username,
        "password": utmb_password
    }

    res = requests.post(url, data=payload)
    data = res.json()
    access_token = data.get("access_token")
    
    return access_token

# -------------------------------------------------
# Get race results
# -------------------------------------------------

def get_race_results(
        race_id: str, 
        race_year: int, 
        course_id: str, 
        access_token: str, 
        printouts: bool = False
    ) -> pd.DataFrame:
    print(f"Retrieving data for: {race_id} ~ {course_id} ~ {race_year}")
    if printouts:
        print("-----------------------------------------")


    # The UTMB API returns results page by page
    max_pages = 100 # Maximum number of pages to try
    results_per_page = 100 # How many runners the API returns per page

    # Set up HTTP headers for UTMB API
    headers = {
        "Accept": "*/*", # Accepts any type of response
        "User-Agent": "Mozilla/5.0", # Pretend to be a normal browser
        "Origin": "https://live.utmb.world", # Tell the server request came from UTMB live site
        "Referer": "https://live.utmb.world/", # Tell server what page "linked" us here
        "X-Tenant": f"{race_id}_{race_year}", # UTMB API key
        "content-type": "application/json", # Expecting JSON data
        "Authorization": f"Bearer {access_token}", # Login to UTMB page
    }


    # The UTMB API returns a page of results at a time
    # Run through all pages

    # Store results in a list - single page at once (faster & better if certain page fails)
    race_results_list = []
    for i in range(max_pages + 1):
            
        # GET request to the UTMB API
        res = requests.get(
            f"https://utmblive-api.utmb.world/races/{course_id}/progressive",
            params={"type": "PROGRESSIVE_RANKING", "page": i, "limit": results_per_page},
            headers=headers,
        )

        # Fail early if API breaks
        res.raise_for_status()  

        # Convert JSON content into python dict
        data = res.json()
        
        # Get runners information
        runners = data.get("runners", [])

        # Stop when no runners left
        if not runners:
            if printouts:
                print(f"No more results at page {i} ~> {sum(len(x) for x in race_results_list)} results. Stopping.")
            break

        # flatten JSON to DataFrame
        df = pd.json_normalize(runners) 
        race_results_list.append(df)

        if printouts:
            print(f"Page {i} done ~> {sum(len(x) for x in race_results_list)} runners so far.")

    # Combine all pages into one DataFrame
    if not race_results_list:
        race_results = pd.DataFrame()

    else:
        warnings.filterwarnings(
            "ignore",
            message=".*DataFrame concatenation with empty or all-NA entries is deprecated.*",
            category=FutureWarning
            )
        
        columns_to_select = [
            "raceId", "raceName", "raceCategory", "start",
            "info.fullname", "info.url", "info.index",
            "info.sex", "info.age", "info.countryCode", "info.category", "info.club",
            "ranking.scratch", "ranking.sex", "ranking.category",
            "raceTime", "diffToFirst", "status", "isFinisher"
        ]
        
        race_results = (
            pd.concat(race_results_list, ignore_index=True)
            .reindex(columns=columns_to_select)
            .rename(columns={
                "raceId": "race_id", 
                "raceName": "race_name", 
                "raceCategory": "race_category",
                "start": "race_start_time",
                "info.fullname": "runner_name", 
                "info.url": "runner_url", 
                "info.index": "runner_overall_index",
                "info.sex": "runner_gender", 
                "info.age": "runner_age", 
                "info.countryCode": "runner_country_code", 
                "info.category": "runner_category", 
                "info.club": "runner_club",
                "ranking.scratch": "runner_rank", 
                "ranking.sex": "runner_rank_gender", 
                "ranking.category": "runner_rank_category",
                "raceTime": "runner_race_time", 
                "diffToFirst": "runner_diff_to_first_time", 
                "status": "runner_final_status", 
                "isFinisher": "runner_is_finisher"
            })
            .assign(
                age = lambda x: pd.to_numeric(x["runner_age"], errors="coerce"),
                runner_race_time_hours = lambda x: x["runner_race_time"].apply(time_to_hours),
                runner_diff_to_first_time_hours = lambda x: x["runner_diff_to_first_time"].apply(time_to_hours),
                race_start_time_hours = lambda x: x["race_start_time"].apply(time_to_hours),
                runner_final_status_map = lambda x: x["runner_final_status"].map({"f": "finisher", "a": "dnf", "hd": "broomed"})
            )
        )

    # Format data ...
    # race_results.loc[race_results["runner_is_finisher"] == False, "runner_race_time_hours"] = np.nan
    # race_results.loc[race_results["runner_is_finisher"] == False, "runner_race_time"] = np.nan
    
    race_results["runner_age"] = race_results["runner_age"].astype(float)

    return race_results

# -------------------------------------------------
# Get runner results
# -------------------------------------------------

def get_runner_results(
        runner_id: str, 
        access_token: str
    ) -> pd.DataFrame:

    # Set up HTTP headers for UTMB API
    headers = {
        "Accept": "*/*", # Accepts any type of response
        "User-Agent": "Mozilla/5.0", # Pretend to be a normal browser
        "Origin": "https://utmb.world", # Tell the server request came from UTMB site
        "Referer": "https://utmb.world/", # Tell server what page "linked" us here
        "x-tenant-id": "worldseries", # UTMB API key
        "content-type": "application/json", # Expecting JSON data
        "Authorization": f"Bearer {access_token}" # Login to UTMB page
    }

                
    # GET request to the UTMB API
    res = requests.get(
        url=f"https://api.utmb.world/runners/{runner_id}/results",
        params={"page": 1, "limit": 100},
        headers=headers,
    )

    data = res.json()
    results = data.get("results", [])
    df = pd.DataFrame(results)
    runner_results_df = (
        df
        [[
            "dateIso", "race",  "uri", "piCategory", "utmbEventStatus", "country", "countryCode",
            "distance", "elevationGain", 
            "time", "isDnf", "rank", "rankGender", 
            "totalRanked", "totalRankedGender", "index",
        ]]
        .rename(columns = {
            "dateIso": "date",
            "race": "race_name",
            "uri": "race_uri",
            "utmbEventStatus": "utmb_event_status",
            "country": "country",
            "countryCode": "country_code",
            "distance": "distance",
            "elevationGain": "elevation_gain",
            "time": "race_time",
            "isDnf": "is_dnf",
            "rank": "rank",
            "rankGender": "rank_gender",
            "totalRanked": "total_finished",
            "totalRankedGender": "total_finished_gender",
            "index": "race_utmb_index",
        })
        .assign(
                distance = lambda x: x["distance"].apply(lambda x: pd.to_numeric(x, errors="coerce")),
                race_time_hours = lambda x: x["race_time"].apply(time_to_hours),
                date = lambda x: pd.to_datetime(x["date"]) 
        )
    )

    return runner_results_df