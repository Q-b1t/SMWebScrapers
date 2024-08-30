import configparser

def get_config_parser(config_filepath):
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_filepath)
    return config

def fetch_apify_params(config_parser,social_media,comments):
    """
    This only works for apify, later, the code will be adapted for youtube and X as well.
    Parameters:
        config_parser: The config parser object built with the configuration file
        social_media: The social media name in str format as received from the cli
        posts: Wether to scrap for posts or comments.
    """
    assert config_parser['APIFY']["bearer_token"] != "" ,f"[-] The configuration file does not contain bearer token"
    if not comments:
        assert config_parser[social_media.upper()]["post_actor"] != "" ,f"[-] The configuration file does not the post actor for {social_media}"
    else:
        assert config_parser[social_media.upper()]["comment_actor"] != "" ,f"[-] The configuration file does not contain the comment actor for {social_media}"
    
    actor = config_parser[social_media.upper()]["post_actor"] if not comments else config_parser[social_media.upper()]["comment_actor"]
    return config_parser['APIFY']["bearer_token"],actor

def fetch_proxy_params(config_parser):
    assert config_parser['PROXY']["proxy_username"] != "" ,f"[-] The configuration file does not contain the proxy's username"
    assert config_parser['PROXY']["proxy_password"] != "" ,f"[-] The configuration file does not contain the proxy's password"
    assert config_parser['PROXY']["dns_settings"] != "" ,f"[-] The configuration file does not contain the proxy's dns settings"
    return config_parser['PROXY']["proxy_username"],config_parser['PROXY']["proxy_password"],config_parser['PROXY']["dns_settings"]


def fetch_actor_input_filepath(config_parser):
    assert config_parser['PATH']["actor_input_file"] != "" ,f"[-] The configuration file does not contain the proxy's actor's input file' name"
    return config_parser['PATH']["actor_input_file"] 
def fetch_data_folder(config_parser):
    assert config_parser['PATH']["data_folder"] != "" ,f"[-] The configuration file does not contain the scraper's data folder's name"
    return config_parser['PATH']["data_folder"] 

def fetch_input_folder(config_parser):
    assert config_parser['PATH']['scraper_input_folder'] != '', f"[-] The configuration file does not contain the scraper's input folder's name"
    return config_parser['PATH']['scraper_input_folder']