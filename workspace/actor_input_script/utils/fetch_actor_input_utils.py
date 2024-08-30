import configparser
import json
import os

def write_params(folder,input_params):
  for social_media,params in input_params.items():
    print(f'[+] writting {social_media} params into {folder}...')
    with open(os.path.join(folder,f"{social_media}Input.json"),'w',encoding='utf-8') as f:
      json.dump(params,f,indent=4)
    f.close()

def get_config_parser(config_filepath):
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_filepath)
    return config

def fetch_input_path(config_parser):
    assert config_parser['GENERAL']["input_folder"] != "" ,f"[-] The configuration file does not contain an input folder in which to generate the actor inputs."
    return config_parser['GENERAL']["input_folder"]


def fetch_query_limits(config_parser):
    assert config_parser['GENERAL']["comments_query_limit"] != "" ,f"[-] The configuration file does not contain a comments query limit"
    assert config_parser['GENERAL']["posts_query_limit"] != "" ,f"[-] The configuration file does not contain a post query limit"
    return config_parser.getint('GENERAL',"comments_query_limit"),config_parser.getint('GENERAL',"posts_query_limit")

def get_date_limit(config_parser):
    assert config_parser['GENERAL']["date_limit"] != "" ,f"[-] The configuration file does not contain a search cutoff date for the actors that support it."
    return config_parser['GENERAL']["date_limit"]