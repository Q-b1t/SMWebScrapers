import configparser
import glob
import os

from utils.date_functions import *
from utils.parsing_functions import *


def get_config_parser(config_filepath):
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_filepath)
    return config

def fetch_input_params(config_parser):
    """
    Retrive input path and folders from configuration
    """
    assert config_parser['INPUT_PATH']["input_path"] != "" ,f"[-] The configuration file does not contain an input path."
    assert config_parser['INPUT_PATH']["posts_folder"] != "" ,f"[-] The configuration file does not contain an post folder."
    assert config_parser['INPUT_PATH']["comments_folder"] != "" ,f"[-] The configuration file does not contain an comments folder."
    assert config_parser['INPUT_PATH']["hybrid_folder"] != "" ,f"[-] The configuration file does not contain an hybrid folder."

    return config_parser['INPUT_PATH']["input_path"],config_parser['INPUT_PATH']["posts_folder"],config_parser['INPUT_PATH']["comments_folder"],config_parser['INPUT_PATH']["hybrid_folder"]


def fetch_output_params(config_parser):
    """
    Retrive input path and folders from configuration
    """
    assert config_parser['OUTPUT_PATH']["output_path"] != "" ,f"[-] The configuration file does not contain an output path."
    assert config_parser['OUTPUT_PATH']["output_folder"] != "" ,f"[-] The configuration file does not contain an output folder."

    return config_parser['OUTPUT_PATH']["output_path"],config_parser['OUTPUT_PATH']["output_folder"]




if __name__ == '__main__':
    CONFIG_FILE = 'merger.cfg'
    config = get_config_parser(CONFIG_FILE)
    
    # retrieve input params 
    input_path,posts_folder,comments_folder,hybrid_folder = fetch_input_params(config_parser=config)

    post_path = os.path.join(input_path,posts_folder)
    comments_path = os.path.join(input_path,comments_folder)
    hybrid_path = os.path.join(input_path,hybrid_folder)

    #print(post_path,comments_path,hybrid_path)

    # retrive output params 
    output_path, output_folder = fetch_output_params(config_parser=config)
    merged_path= os.path.join(output_path,output_folder)
    merged_file = 'merged_data.json' # to be specified in command line interface
    
    for path in [post_path,comments_path,hybrid_path,merged_path]:
        if not os.path.exists(path):
            print(f"[*] creating {path} ...")
            os.makedirs(path)
        else:
            print(f"[+] {path} already exists, skipping ...")

    # get all the files
    post_files = glob.glob(f'{post_path}/*.json')
    comment_files = glob.glob(f'{comments_path}/*.json')
    hybrid_files = glob.glob(f'{hybrid_path}/*.json')

    #print(post_files,comment_files,hybrid_files)

    # load the data into memory and organize them
    post_mapping,comment_mapping,hibrid_data_mapping = get_data_mappings(
        post_files = post_files,
        comment_files = comment_files,
        hibrid_files = hybrid_files
    )

    #print(post_mapping.keys(),comment_mapping.keys(),hibrid_data_mapping.keys())
    merged_data = merge_data(
        comment_mapping=comment_mapping,
        post_mapping=post_mapping,
        hibrid_data_mapping=hibrid_data_mapping
    )

    # normalize dates
    for sample in merged_data:
        date = normalize_date(sample['created_at'])
        sample['created_at'] = date



    # write the data
    with open(os.path.join(merged_path,merged_file),'w',encoding='utf-8') as f:
        json.dump(merged_data,f,indent=4)
    f.close()