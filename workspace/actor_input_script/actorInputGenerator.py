import os
import json 
import configparser
from utils.fetch_actor_input_utils import *



if __name__ == '__main__':
  
  CONFIG_FILE='inputGenerator.cfg'
  config = get_config_parser(config_filepath=CONFIG_FILE)

  date_limit = get_date_limit(config_parser=config)


  input_folder = fetch_input_path(config_parser=config)
  posts_path = os.path.join(input_folder,'posts')
  comments_path = os.path.join(input_folder,'comments')

  # query limits for post and comments
  comments_query_limits,posts_query_limits = fetch_query_limits(config_parser=config)


  # create tree 
  print('[~] creating input file tree...')
  for folder in [posts_path,comments_path]:
    folder_ = os.path.join(input_folder,folder)
    if not os.path.exists(folder_):
      print(f"[*] creating {folder_} ...")
      os.makedirs(folder_)
    else:
      print(f"[+] {folder_} already exists, skipping ...")
  
  # input configurations


  # facebook
  facebook_posts = {
      "max_posts": posts_query_limits,
      "max_retries": config.getint('FACEBOOK','max_retries'),
      "recent_posts": config.getboolean('FACEBOOK','recent_posts'),
      "search_type": config['FACEBOOK']['search_type']
  }

  facebook_comments = {
      "viewOption": config['FACEBOOK']['view_option'],
      "includeNestedComments": config.getboolean('FACEBOOK','include_nested_comments'),
      "resultsLimit": comments_query_limits,
  }

  # instagram

  instagram_posts = {
      "resultsType": config['INSTAGRAM']['results_type_posts'],
      "resultsLimit": posts_query_limits,
      "searchType": config['INSTAGRAM']['search_type'],
      "searchLimit": config.getint('INSTAGRAM','search_limit'),
      'onlyPostsNewerThan': date_limit,
      "addParentData": config.getboolean('INSTAGRAM','add_parent_data'),
  }

  instagram_comments = {
      "resultsType": config['INSTAGRAM']['results_type_comments'],
      "resultsLimit": comments_query_limits,
      "searchType": config['INSTAGRAM']['search_type'],
      "searchLimit": config.getint('INSTAGRAM','search_limit'),
      "addParentData": config.getboolean('INSTAGRAM','add_parent_data'),
      "viewOption": config['INSTAGRAM']['view_option'],
  }


  # tiktok
  tiktok_posts = {
      "shouldDownloadCovers": config.getboolean('TIKTOK','should_download_covers'),
      "shouldDownloadSlideshowImages": config.getboolean('TIKTOK','should_download_slideshow_images'),
      "shouldDownloadSubtitles": config.getboolean('TIKTOK','should_download_subtitles'),
      "shouldDownloadVideos": config.getboolean('TIKTOK','should_download_videos'),
      "searchSection": config['TIKTOK']['search_section'],
      "oldestPostDate": date_limit,
  }

  tiktok_comments = {
      "commentsPerPost": comments_query_limits,                           
      "maxRepliesPerComment": config.getint('TIKTOK','max_replies_per_comment'),
  }
  
  
  
  # post mapping
  comments_input_params = {
      'facebook':facebook_comments,
      'instagram':instagram_comments,
      'tiktok':tiktok_comments
  }
  
  # omment mappings
  posts_input_params = {
      'facebook':facebook_posts,
      'instagram':instagram_posts,
      'tiktok':tiktok_posts
  }
  # write parameters to json file 
  write_params(
      folder=comments_path,
      input_params=comments_input_params
  )

  write_params(
      folder=posts_path,
      input_params=posts_input_params
  )
