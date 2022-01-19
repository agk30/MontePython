import configparser
config = configparser.ConfigParser()

config.read("../inputs.cfg")

experimental = config["Experimental"]["parameter1"]

print (experimental)