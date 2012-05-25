#!/usr/bin/env python

'''
Created on May 15, 2012

@author: jsmith
'''
import argparse
import xml.etree.ElementTree
import urllib
import sys

API_URL = "http://www.google.com/ig/api?"

class CurrentConditions(object):
    def __init__(self, temp, condition, wind_condition, humidity):
        self.temp = temp
        self.condition = condition
        self.wind_condition = wind_condition
        self.humidity = humidity
    
    def dump(self, out = sys.stdout):
        out.write("""    Current Conditions:
      {0}
      {1}
      {2}
      {3}
""".format(self.temp, self.condition, self.humidity, self.wind_condition))
    
    
class ForecastConditions(object):
    def __init__(self, day_of_week, low, high, condition):
        self.day_of_week = day_of_week
        self.low = low
        self.high = high
        self.condition = condition
        
    def dump(self, out = sys.stdout):
        out.write("""   {0}:
      Low: {1}
      High: {2}
      {3}
""".format(self.day_of_week, self.low, self.high, self.condition))
    
        

def get_weather(location):
    url = API_URL + urllib.urlencode({"weather": location})
    return urllib.urlopen(url).read()

def print_weather(weather_xml, out=sys.stdout):
    root = xml.etree.ElementTree.XML(weather_xml)
    weather = root.find("weather")
    forecast_information = weather.find("forecast_information")
    city = forecast_information.find("city").get("data")
    current_conditions_element = weather.find('current_conditions')
    current_conditions = CurrentConditions(*[current_conditions_element.find(x).get("data") for x in ['temp_f', 'condition', 'wind_condition', 'humidity']])
    

    out.write("City: %s\n" % city)
    current_conditions.dump(out)
    
    for forecast_conditions_element in weather.findall('forecast_conditions'):
        forecast_conditions = ForecastConditions(*[forecast_conditions_element.find(x).get("data") for x in ['day_of_week', 'low', 'high', 'condition']])
        forecast_conditions.dump(out)
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get weather for cities.")
    parser.add_argument("cities", metavar="Cities", nargs='*', help='Cities', default=["Orono, ME"])
    args = parser.parse_args()
    for city in args.cities:
        weather = get_weather(city)
        print_weather(weather)