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
    bkdko = "bkdko"
    crdko = "crdko"
    bkdko_road_test = "bkdko_road_test"
    crdko_road_test = "crdko_road_test"
    autocrind = "autocrind"
    crwle = "crwle"
    twrdsdtsc = "twrdsdtsc"
    deepst = "deepst"
    better_advice = "better_advice"