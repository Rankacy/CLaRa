from enum import Enum


class Language(str, Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"


class UnitTypes(str, Enum):
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


class Stores(str, Enum):
    WALMART = "Walmart"
    TARGET = "Target"
    ZABKA = "Zabka"


class AudioStreamServices(str, Enum):
    APPLEMUSIC = "Apple music"
    SPOTIFY = "Spotify"
    YOUTUBE = "YOUTUBE"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
