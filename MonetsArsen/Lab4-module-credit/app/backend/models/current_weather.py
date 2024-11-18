"""Current weather report model"""

from typing import Tuple, Optional
from datetime import datetime
from beanie import Document, Indexed
from pydantic import BaseModel, Field


class WeatherSchema(BaseModel):
    """
    Schema for representing the weather report data.

    This class defines the structure of the weather report, including fields
    for city, coordinates, weather description, temperature, humidity, wind
    speed, sunrise, and sunset times.

    Attributes:
        city (str): The name of the city where the weather report is generated.
        coordinates (Tuple[float, float]): Latitude and longitude of the city.
        description (str): Description of the current weather (e.g., "Clear sky").
        temperature (float): The current temperature in degrees Celsius.
        humidity (float): The current humidity percentage.
        wind_speed (float): The current wind speed in meters per second.
        time (datetime): The timestamp of when the weather report was generated.
        sunrise (Optional[datetime]): The time of sunrise, if available.
        sunset (Optional[datetime]): The time of sunset, if available.
    """
    city: Indexed(str, unique=True)
    coordinates: Tuple[float, float]
    description: str = Field(...)
    temperature: float = Field(...)
    humidity: float
    wind_speed: float
    time: datetime
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None


class WeatherReport(Document, WeatherSchema):
    """
    MongoDB Document model representing a weather report.

    This class extends both the Beanie `Document` class and `WeatherSchema` class.
    It represents the weather report document that will be stored in MongoDB,
    and includes custom methods for comparison, hashing, and retrieving data.

    Inherits from:
        Document: Beanie's MongoDB document model.
        WeatherSchema: Pydantic model that defines the structure of the weather report.

    Methods:
        __repr__(): Custom representation for the weather report object.
        __str__(): String representation for the weather report object.
        __hash__(): Generates a hash value based on the city name.
        __eq__(): Compares two weather report objects for equality based on the city.
        created: Property that returns the creation timestamp from the report's ID.
        by_city(): Class method to find a weather report by city name.
    """

    def __repr__(self) -> str:
        """
        Custom representation for the WeatherReport object.

        Returns:
            str: A string representing the WeatherReport object in the format:
                 <WeatherReport {city}>.
        """
        return f"<WeatherReport {self.city}>"

    def __str__(self) -> str:
        """
        String representation for the WeatherReport object.

        Returns:
            str: The name of the city associated with the weather report.
        """
        return self.city

    def __hash__(self) -> int:
        """
        Generates a hash value for the WeatherReport object based on the city name.

        Returns:
            int: The hash value of the city name.
        """
        return hash(self.city)

    def __eq__(self, other: object) -> bool:
        """
        Compares two WeatherReport objects for equality based on the city name.

        Args:
            other (object): The other object to compare with.

        Returns:
            bool: True if the city names of both weather reports are the same, False otherwise.
        """
        if isinstance(other, WeatherReport):
            return self.city == other.city
        return False

    @property
    def created(self) -> datetime:
        """
        Property that returns the creation time of the weather report based on its MongoDB document ID.

        The document ID's generation time is used as the creation timestamp.

        Returns:
            datetime: The datetime when the weather report document was created.
        """
        return self.id.generation_time

    @classmethod
    async def by_city(cls, city: str) -> "WeatherReport":
        """
        Class method to retrieve a weather report by the name of the city.

        Args:
            city (str): The name of the city for which the weather report is to be fetched.

        Returns:
            WeatherReport: The weather report document for the specified city.
        """
        return await cls.find_one({"city": city})