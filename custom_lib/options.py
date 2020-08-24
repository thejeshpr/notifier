from enum import Enum

class NGGroup(str, Enum):
    funny = "funny"
    gif = "gif"
    nsfw = "nsfw"
    girl = "girl"
    india = "india"
    random = "random"
    animals = "animals"
    awesome = "awesome"
    car = "car"
    gaming = "gaming"
    girlcelebrity = "girlcelebrity"
    meme = "meme"
    polictics = "polictics"
    relationship = "relationship"
    savage = "savage"
    video = "video"
    wtf = "wtf"


class NGType(str, Enum):
    hot = "hot"
    fresh = "fresh"
    trending = "trending"