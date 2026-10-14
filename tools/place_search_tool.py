
import os
import json
import re
import urllib.parse
import urllib.request
from typing import List

from langchain.tools import tool
from dotenv import load_dotenv


# Optional Tavily fallback
try:
    from utils.place_info_search import TavilyPlaceSearchTool
except ImportError:
    TavilyPlaceSearchTool = None


class PlaceSearchTool:
    def __init__(self):
        load_dotenv()

        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.tavily_search = None

        self.place_search_tool_list = self._setup_tools()

    def _get_tavily_client(self):
        if self.tavily_api_key and self.tavily_search is None:
            if TavilyPlaceSearchTool is not None:
                self.tavily_search = TavilyPlaceSearchTool()
        return self.tavily_search

    def _search_openstreetmap(self, place: str, category: str) -> str:
        """Search OpenStreetMap data through the Overpass API."""

        category_filters = {
            "attractions": [
                '["tourism"="attraction"]',
                '["tourism"="museum"]',
                '["tourism"="viewpoint"]',
                '["historic"]',
                '["tourism"="artwork"]',
            ],
            "restaurants": [
                '["amenity"="restaurant"]',
                '["amenity"="cafe"]',
                '["amenity"="fast_food"]',
                '["amenity"="food_court"]',
            ],
            "activities": [
                '["leisure"="park"]',
                '["sport"]',
                '["tourism"="theme_park"]',
                '["tourism"="zoo"]',
                '["natural"="beach"]',
                '["tourism"="museum"]',
            ],
            "transportation": [
                '["amenity"="bus_station"]',
                '["public_transport"="station"]',
                '["railway"="station"]',
                '["amenity"="taxi"]',
                '["aeroway"="aerodrome"]',
            ],
        }

        filters = category_filters[category]

        # Escape the place name before inserting it into the query.
        safe_place = re.escape(place.strip())

        # Find the administrative area matching the destination.
        query_parts = [
            f'area["name"~"^{safe_place}$",i]["boundary"="administrative"]->.searchArea;'
        ]

        for item_filter in filters:
            query_parts.append(
                f"(node{item_filter}(area.searchArea);"
                f"way{item_filter}(area.searchArea);"
                f"relation{item_filter}(area.searchArea););"
            )

        query = "\n".join(query_parts) + "\nout center tags 15;"

        url = "https://overpass-api.de/api/interpreter"
        data = urllib.parse.urlencode({"data": query}).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "AITripPlanner/1.0",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))

        elements = result.get("elements", [])
        places = []
        seen = set()

        for element in elements:
            tags = element.get("tags", {})
            name = tags.get("name")

            if not name or name.lower() in seen:
                continue

            seen.add(name.lower())

            details = [
                f"Name: {name}",
                f"Category: {category}",
            ]

            address = tags.get("addr:full")
            if address:
                details.append(f"Address: {address}")

            for key in ("tourism", "amenity", "historic", "leisure", "sport"):
                if tags.get(key):
                    details.append(f"{key}: {tags[key]}")
                    break

            places.append(" | ".join(details))

        if not places:
            return (
                f"No matching mapped places were found for {category} "
                f"in {place}. Try checking the destination name or "
                "using another data source."
            )

        return "\n".join(f"{i}. {item}" for i, item in enumerate(places, 1))

    def _static_fallback(self, place: str, category: str) -> str:
        examples = {
            "attractions": "local landmarks, historical sites, markets, cultural spots",
            "restaurants": "local restaurants, street food areas, cafes",
            "activities": "sightseeing, cultural walks, outdoor activities",
            "transportation": "local buses, taxis, auto-rickshaws, railway stations",
        }

        return (
            f"No live place data is available for {place}. "
            f"Possible {category} to research include "
            f"{examples.get(category, 'local places')}."
        )

    def _search(self, place: str, category: str, tavily_method: str) -> str:
        try:
            results = self._search_openstreetmap(place, category)
            if not results.startswith("No matching mapped places"):
                return f"{category.title()} in {place} (OpenStreetMap):\n{results}"
        except Exception as exc:
            osm_error = str(exc)
        else:
            osm_error = ""

        # Optional fallback if Tavily is configured.
        try:
            tavily = self._get_tavily_client()
            if tavily is not None:
                method = getattr(tavily, tavily_method, None)
                if method:
                    return f"{category.title()} in {place} (Tavily): {method(place)}"
        except Exception:
            pass

        fallback = self._static_fallback(place, category)

        if osm_error:
            return f"{fallback}\nOpenStreetMap search failed: {osm_error}"

        return fallback

    def _setup_tools(self) -> List:

        @tool
        def search_attractions(place: str) -> str:
            """Search tourist attractions in a destination using OpenStreetMap."""
            return self._search(
                place, "attractions", "tavily_search_attractions"
            )

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants and cafes using OpenStreetMap."""
            return self._search(
                place, "restaurants", "tavily_search_restaurants"
            )

        @tool
        def search_activities(place: str) -> str:
            """Search parks and activities using OpenStreetMap."""
            return self._search(
                place, "activities", "tavily_search_activity"
            )

        @tool
        def search_transportation(place: str) -> str:
            """Search public transportation locations using OpenStreetMap."""
            return self._search(
                place, "transportation", "tavily_search_transportation"
            )

        return [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation,
        ]










# import os
# from typing import List
# from langchain.tools import tool
# from dotenv import load_dotenv

# # optional imports (won't crash if unused)
# try:
#     from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
# except ImportError:
#     GooglePlaceSearchTool = None
#     TavilyPlaceSearchTool = None


# class PlaceSearchTool:
#     def __init__(self):
#         load_dotenv()

#         self.google_api_key = os.getenv("GPLACES_API_KEY")
#         self.tavily_api_key = os.getenv("TAVILY_API_KEY")

#         self.google_places_search = None
#         self.tavily_search = None

#         self.place_search_tool_list = self._setup_tools()

#     def _get_google_client(self):
#         if self.google_api_key and self.google_places_search is None:
#             self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
#         return self.google_places_search

#     def _get_tavily_client(self):
#         if self.tavily_api_key and self.tavily_search is None:
#             self.tavily_search = TavilyPlaceSearchTool()
#         return self.tavily_search

#     def _static_fallback(self, place: str, category: str) -> str:
#         """Final fallback when no APIs are available"""
#         examples = {
#             "attractions": "local landmarks, historical sites, markets, cultural spots",
#             "restaurants": "popular local restaurants, street food areas, cafes",
#             "activities": "sightseeing, local food exploration, cultural walks",
#             "transportation": "local buses, taxis, auto-rickshaws, rental vehicles",
#         }
#         return (
#             f"(Demo Mode) Since external APIs are not configured, here are common "
#             f"{category} to explore in {place}: {examples.get(category)}."
#         )

#     def _setup_tools(self) -> List:

#         @tool
#         def search_attractions(place: str) -> str:
#             """Search attractions of a place"""

#             if self.google_api_key:
#                 try:
#                     google = self._get_google_client()
#                     return f"Attractions in {place}: {google.google_search_attractions(place)}"
#                 except Exception:
#                     pass

#             if self.tavily_api_key:
#                 try:
#                     tavily = self._get_tavily_client()
#                     return f"Attractions in {place}: {tavily.tavily_search_attractions(place)}"
#                 except Exception:
#                     pass

#             return self._static_fallback(place, "attractions")

#         @tool
#         def search_restaurants(place: str) -> str:
#             """Search restaurants of a place"""

#             if self.google_api_key:
#                 try:
#                     google = self._get_google_client()
#                     return f"Restaurants in {place}: {google.google_search_restaurants(place)}"
#                 except Exception:
#                     pass

#             if self.tavily_api_key:
#                 try:
#                     tavily = self._get_tavily_client()
#                     return f"Restaurants in {place}: {tavily.tavily_search_restaurants(place)}"
#                 except Exception:
#                     pass

#             return self._static_fallback(place, "restaurants")

#         @tool
#         def search_activities(place: str) -> str:
#             """Search activities of a place"""

#             if self.google_api_key:
#                 try:
#                     google = self._get_google_client()
#                     return f"Activities in {place}: {google.google_search_activity(place)}"
#                 except Exception:
#                     pass

#             if self.tavily_api_key:
#                 try:
#                     tavily = self._get_tavily_client()
#                     return f"Activities in {place}: {tavily.tavily_search_activity(place)}"
#                 except Exception:
#                     pass

#             return self._static_fallback(place, "activities")

#         @tool
#         def search_transportation(place: str) -> str:
#             """Search transportation of a place"""

#             if self.google_api_key:
#                 try:
#                     google = self._get_google_client()
#                     return f"Transportation in {place}: {google.google_search_transportation(place)}"
#                 except Exception:
#                     pass

#             if self.tavily_api_key:
#                 try:
#                     tavily = self._get_tavily_client()
#                     return f"Transportation in {place}: {tavily.tavily_search_transportation(place)}"
#                 except Exception:
#                     pass

#             return self._static_fallback(place, "transportation")

#         return [
#             search_attractions,
#             search_restaurants,
#             search_activities,
#             search_transportation,
#         ]

# import os
# from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
# from typing import List
# from langchain.tools import tool
# from dotenv import load_dotenv

# class PlaceSearchTool:
#     def __init__(self):
#         load_dotenv()
#         self.google_api_key = os.environ.get("GPLACES_API_KEY")
#         self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
#         self.tavily_search = TavilyPlaceSearchTool()
#         self.place_search_tool_list = self._setup_tools()

#     def _setup_tools(self) -> List:
#         """Setup all tools for the place search tool"""
#         @tool
#         def search_attractions(place:str) -> str:
#             """Search attractions of a place"""
#             try:
#                 attraction_result = self.google_places_search.google_search_attractions(place)
#                 if attraction_result:
#                     return f"Following are the attractions of {place} as suggested by google: {attraction_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_attractions(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         @tool
#         def search_restaurants(place:str) -> str:
#             """Search restaurants of a place"""
#             try:
#                 restaurants_result = self.google_places_search.google_search_restaurants(place)
#                 if restaurants_result:
#                     return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_restaurants(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         @tool
#         def search_activities(place:str) -> str:
#             """Search activities of a place"""
#             try:
#                 restaurants_result = self.google_places_search.google_search_activity(place)
#                 if restaurants_result:
#                     return f"Following are the activities in and around {place} as suggested by google: {restaurants_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_activity(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         @tool
#         def search_transportation(place:str) -> str:
#             """Search transportation of a place"""
#             try:
#                 restaurants_result = self.google_places_search.google_search_transportation(place)
#                 if restaurants_result:
#                     return f"Following are the modes of transportation available in {place} as suggested by google: {restaurants_result}"
#             except Exception as e:
#                 tavily_result = self.tavily_search.tavily_search_transportation(place)
#                 return f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
#         return [search_attractions, search_restaurants, search_activities, search_transportation]