import math


def standard_deviation(data=[]):
    mean = sum(data) / len(data)
    return math.sqrt(sum([(p - mean) ** 2 for p in data]) / (len(data) - 1))


def rolling_standard_deviation(data=[]):
    return math.sqrt(sum([p ** 2 for p in data]) / len(data))


def volatility(data=[]):
    return standard_deviation(data=log_return(data=data))


def rolling_volatility(data=[]):
    return rolling_standard_deviation(data=log_return(data=data))


def log_return(data=[]):
    return [math.log(data[i + 1] / data[i]) for i in range(len(data) - 1)]
