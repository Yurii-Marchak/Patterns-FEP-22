from backend.models import SportsEventReport, WeatherReport

__beanie_models__ = [WeatherReport, SportsEventReport]
"""
List of Beanie ODM (Object-Document Mapper) models to be registered.

This list is typically used during application initialization to 
register document models with Beanie for MongoDB interaction. 
Registering models allows for automatic database collection 
mapping and provides async CRUD operations.

Models:
    - WeatherReport: Stores weather-related data
    - SportsEventReport: Stores sports event information
"""