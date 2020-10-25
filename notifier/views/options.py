from enum import Enum


class SpaceTypes(str, Enum):
    tracker = "tracker"


class SyncTypeSet(str, Enum):
    test = "test"
    pricetracker = "pricetracker"
    bfy = "bfy"
    d2 = "d2"
    realpython = "realpython"
    dsrcourse = "dsrcourse"
    ng = "ng"
    github_trending = "github_trending"
    weather = "weather"
    news = "news"
    ys = "ys"
    hn = "hn"
    dzone = "dzone"