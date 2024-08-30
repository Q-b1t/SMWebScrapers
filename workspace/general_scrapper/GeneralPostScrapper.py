from apify_client import ApifyClient
from argparse import ArgumentParser,Namespace
import json
import os
import requests
from tqdm import tqdm
from utils.config_utils import *
from utils.parsing_utils import *
from utils.path_utils import *
from utils.proxy_utils import *




def main():
  # instance command line interface 
  COMMAND_LINE_PARSER = ArgumentParser()
  COMMAND_LINE_PARSER.add_argument("-f","--config_file",help="The command line tool used to the run's parameters (default: scraper.cfg)",type=str,default='scraper.cfg',nargs="?")
  COMMAND_LINE_PARSER.add_argument("-c","--comments_scrap",help="If set to True, it will scrap for comments and posts otherwise (default: False)",type=bool,default=False,nargs="?") 
  COMMAND_LINE_PARSER.add_argument("-s","--social_media",help="Social media to scrap (Supported sm are: Instagram, Facebook, Twitter, X, and Tikok)",type=str,required=True)
  # to be retrieved via the command line interface
  args: Namespace = COMMAND_LINE_PARSER.parse_args()
  SOCIAL_MEDIA = args.social_media
  CONFIG_FILE = args.config_file
  SCRAP_COMMENTS = args.comments_scrap
  
  config = get_config_parser(config_filepath=CONFIG_FILE)

  # apify parameters
  BEARER_TOKEN, APIFY_ACTOR = fetch_apify_params(
    config_parser=config,
    social_media=SOCIAL_MEDIA,
    comments=SCRAP_COMMENTS
    )

  # proxy settings
  PROXY_USERNAME,PROXY_PASSWORD,GEONODE_DNS = fetch_proxy_params(config_parser=config)
  PROXY_URL_TEMPLATE = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{GEONODE_DNS}"

  # folders & paths 
  ACTOR_INPUT_FILE_ = fetch_actor_input_filepath(config_parser=config)
  DATA_FOLDER_ = fetch_data_folder(config_parser=config)
  INPUTS_FOLDER_ = fetch_input_folder(config_parser=config)

  # parse the actor input file based on scrapping type
  ACTOR_INPUT_FILE =parse_actor_input_file(
    path=ACTOR_INPUT_FILE_,
    social_media=SOCIAL_MEDIA,
    comments=SCRAP_COMMENTS
  )

  # parse the data file based on scrapping type 
  DATA_FOLDER = parse_data_folder(
    data_path=DATA_FOLDER_,
    social_media=SOCIAL_MEDIA,
    comments=SCRAP_COMMENTS
  )

  # validate input folder
  check_scrapper_input_paths(INPUTS_FOLDER_)
  INPUTS_FOLDER = parse_scrapper_input_folder(
    scraper_input_path=INPUTS_FOLDER_,
    social_media=SOCIAL_MEDIA,
    comments=SCRAP_COMMENTS
  )

  # parse the path from which the queries will be loaded depending on whether we are scrapong for post or comments
  INPUTS_FILE = f"{SOCIAL_MEDIA}_urls.txt" if SCRAP_COMMENTS else f"{SOCIAL_MEDIA}_queries.txt"
  INPUTS_PATH = os.path.join(INPUTS_FOLDER,INPUTS_FILE)

  # parse data path (the path to which the scraped data will be written to)
  DATA_FILE = f"{SOCIAL_MEDIA}_comments.json" if SCRAP_COMMENTS else f"{SOCIAL_MEDIA}_posts.json"
  DATA_PATH = os.path.join(DATA_FOLDER,DATA_FILE)

  # get the url output file and path (for posts scraping operations only)
  URL_OUTPUT_FOLDER,URL_OUTPUT_FILE = None,None
  if not SCRAP_COMMENTS:
    URL_OUTPUT_FOLDER = get_url_output_path(INPUTS_FOLDER_) # the url's are the comments input so they are on the input folder
    URL_OUTPUT_FILE = f"{SOCIAL_MEDIA}_urls.txt"
    URL_OUTPUT_PATH = os.path.join(URL_OUTPUT_FOLDER,URL_OUTPUT_FILE)
  
  # Prepare the Actor input
  raw_actor_input = load_json(ACTOR_INPUT_FILE)


  # Initialize the ApifyClient with your API token
  client = ApifyClient(BEARER_TOKEN)

  parsing_action_mapper = get_action_mappers(comments=SCRAP_COMMENTS)
  url_action_mapper = None
  if not SCRAP_COMMENTS:
    url_action_mapper = get_url_extraction_action_mapper()

  # session 
  session = requests.Session()

  # get queries
  queries = load_text_file(INPUTS_PATH)
  print(f"[~] reading input file: {INPUTS_PATH}")
  print(f"[+] retrieved {len(queries)} queries for this run")

  items = list()
  
  
  for index,query in tqdm(enumerate(queries,start=1)):
    extracted_queries = list()
    # mapping containing the query that must be added depending on the social network
    parse_input_poats = {
        'instagram':{'search':query},
        'facebook': {"query": query},
        'tiktok':{"searchQueries": [query]}
    }
    parse_input_comments = {
      'instagram':{'directUrls':[query]},
      'facebook': {"startUrls": [{"url": query}]},
      'tiktok':{"postURLs": [query]}
    }

    # create a new actor input 
    actor_input = raw_actor_input.copy()

    # attempt to get a proxy
    proxy_url,proxy_location,success = get_proxy_url(
        proxy_url_template=PROXY_URL_TEMPLATE,
        index=1,
        session=session
    )
    if success:
      print(f"[+] Using proxy for sample {index}/{len(queries)}: {proxy_location}")
      actor_input_proxy = add_proxy_config(
          actor_input=actor_input,
          use_custom_proxy=True,
          proxy_url=proxy_url
      )
    else:
      print(f"[-] Failed to connect to proxy after multiple attempts for query {query}. Defaulting to apify proxy")
      actor_input_proxy = add_proxy_config(actor_input=actor_input)
    
    run_input = actor_input_proxy | parse_input_poats[SOCIAL_MEDIA] if not SCRAP_COMMENTS else actor_input_proxy | parse_input_comments[SOCIAL_MEDIA]

    print(f"[~] Performing search for {query} with the following parameters:")
    print(run_input)

    run = client.actor(APIFY_ACTOR).call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        extracted_queries.append(item)

    # parsing items to extract only the raw data (either post of comment)
    extracted_queries = parsing_action_mapper[SOCIAL_MEDIA](extracted_queries)
    print(f"[+] extracted {len(extracted_queries)} samples for query {query}")
    items += extracted_queries
    print(f"[~] total samples: {len(items)}")
    print("_" * 100)

  # url extraction (post scrap only)
  if not SCRAP_COMMENTS:
    urls = url_action_mapper[SOCIAL_MEDIA](items)
    write_text_file(
      text_file=URL_OUTPUT_PATH,
      raw_data=urls,
      one_line_parsing=True
    )
    print(f"[+] writting urls to {URL_OUTPUT_PATH}")

  if os.path.exists(DATA_FOLDER):
    print(f"[*] output path {DATA_FOLDER} already exists")
  else:
    print(f"[+] creating {DATA_FOLDER} ...")
    os.makedirs(DATA_FOLDER)
  
  print(f"[~] Writting raw data to {DATA_PATH}")
  
  write_json(
        data = items,
        file = DATA_PATH
  )


if __name__ == '__main__':
  main()