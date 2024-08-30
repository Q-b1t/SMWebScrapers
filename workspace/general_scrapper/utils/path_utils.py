from glob import glob
import json
import os 

def load_json(file):
  with open(file,'r',encoding='utf-8') as f:
    data = json.load(f)
  f.close()
  return data

def write_json(data,file):
  with open(file,'w',encoding='utf-8') as f:
    json.dump(data,f,indent=4)
  f.close()

def merge_json_files(folder_path, output_file):
  # List to hold all the data
  merged_data = []

  # Iterate through all files in the folder
  for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
      file_path = os.path.join(folder_path, filename)
      with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        merged_data.extend(data)  # Append data to the list

  # Write the merged data to the output file
  with open(output_file, 'w', encoding='utf-8') as output:
    json.dump(merged_data, output, ensure_ascii=False, indent=4)


def load_text_file(text_file):
  with open(text_file,'r',encoding='utf-8') as f:
    data = f.readlines()
  f.close()
  return data


def write_text_file(text_file,raw_data,one_line_parsing=True):
  if one_line_parsing:
    data = [f"{sample}\n" for sample in raw_data]
  with open(text_file,'w+',encoding='utf-8') as f:
    f.writelines(data)
  f.close()
  

def search_path_4_param(path_list,param):
  """
  Searches for a path in the given filepath that contains the param as substring
  and returns it should it exists and returns None otherwise
  """
  out_file = None
  for path in path_list:
    if param in path:
      out_file = os.path.join(path,param)
      break
  return out_file
      

def search_file_workspace(filepath):
  """searches a path relative the to the workspace"""
  pwd = os.getcwd()
  past = os.path.join(pwd,'..')
  dir = None
  for path in os.listdir(past):
    if filepath in path:
      dir = os.path.join(past,filepath)
  return dir

def parse_actor_input_file(path,social_media,comments):
  last_path = search_file_workspace(filepath=path)
  if last_path is not None:
    if not comments:
      post_path = os.path.join(last_path,'posts')
      if os.path.exists(post_path):
        post_input_file = None
        for file in glob(os.path.join(post_path,'*.json')):
          if social_media in file:
            post_input_file = file
            break
        return post_input_file
      else:
        raise FileNotFoundError
    else:
      comments_path = os.path.join(last_path,'comments')
      if os.path.exists(comments_path):
        comments_input_file = None
        for file in glob(os.path.join(comments_path,'*.json')):
          if social_media in file:
            comments_input_file = file
            break
        return comments_input_file
      else:
        raise FileNotFoundError

  else:
    raise FileNotFoundError
    
def parse_data_folder(data_path,social_media,comments):
  last_path = search_file_workspace(filepath=data_path)
  if last_path is not None:
    data_path_parsed = ''
    if social_media != 'x':
        data_path_parsed = os.path.join(last_path,'comments') if comments else os.path.join(last_path,'posts')
    else:
      data_path_parsed = os.path.join(last_path,'hybrid')
    return data_path_parsed
  else:
    raise FileNotFoundError

def parse_scrapper_input_folder(scraper_input_path,social_media,comments):
  previus_relative_path = search_file_workspace(filepath=scraper_input_path)
  if previus_relative_path is not None:
    scraper_input_path_parsed = ''
    if comments:
      scraper_input_path_parsed = os.path.join(previus_relative_path,'urls')
    else:
      scraper_input_path_parsed = os.path.join(previus_relative_path,'queries')
    return scraper_input_path_parsed
  else:
    raise FileNotFoundError
  

def check_scrapper_input_paths(scraper_input_path):
  """
  Creates the scrapper's input paths
  """
  social_media = ['facebook','x','twitter','instagram','youtube ']
  relative_input_path = os.path.join(os.path.join(os.getcwd(),'..'),scraper_input_path)

  if not os.path.exists(relative_input_path):
    print(f"[~] creating {relative_input_path}")
    os.makedirs(relative_input_path)

  
  post_input = os.path.join(relative_input_path,'queries')
  comment_input = os.path.join(relative_input_path,'urls')
  for path in [post_input,comment_input]:
    if not os.path.exists(path):
      os.mkdir(path)
      print(f"[~] creating {path}")
    else:
      print(f"[~] {path} already exists")
  """
  for path in [post_input,comment_input]:
    for sm in social_media:
      create_path = os.path.join(path,sm)
      if not os.path.exists(create_path):
        os.mkdir(create_path)
        print(f"[~] creating {create_path}")
      else:
        print(f"[~] {create_path} already exists")
  """

def get_url_output_path(scraper_input_path):
  """
  This function returns the comment's input path that will be used to write the comments
  when making a post scraping operation
  """
  relative_input_path = os.path.join(os.path.join(os.getcwd(),'..'),scraper_input_path)
  comment_input_path = os.path.join(relative_input_path,'urls')
  return comment_input_path
