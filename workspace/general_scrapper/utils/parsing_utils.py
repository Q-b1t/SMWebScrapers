"""
Parsing post functions
These functions are called depending on the social media between the extraction and
the writting of the posts data. If there is some extra operations that needs to be done to
properly extract the raw posts, which will depend on the actor you are running, you can put
it in here. 
"""

def parse_facebook_posts(raw):
    data = [post for post in raw if 'post_id' in post.keys()]
    return data

def parse_tiktok_posts(raw):
    data = [post for post in raw if 'id' in post.keys()]
    return data

def parse_instagram_posts(raw):
    posts = list()
    for item in raw:
        posts += (item['topPosts'])
    return posts

def parse_youtube_posts(raw):
    return raw

def parse_x_posts(raw):
    return raw


"""
Parsing comment functions
These functions are called depending on the social media between the extraction and
the writting of the comment data. If there is some extra operations that needs to be done to
properly extract the raw posts, which will depend on the actor you are running, you can put
it in here. 
"""

def parse_facebook_comments(raw):
    return raw

def parse_tiktok_comments(raw):
    return raw

def parse_instagram_comments(raw):
    return raw

def parse_youtube_comments(raw):
    return raw

def parse_x_comments(raw):
    return raw


# action mapper 
def get_action_mappers(comments):
    """
    Returns the cooresponding action mapper for parsing data depending on whether the
    run is for posts extraction or comment extraction
    """
    if comments:
        return {
            'instagram':lambda data : parse_instagram_comments(data),
            'facebook':lambda data : parse_facebook_comments(data),
            'tiktok':lambda data : parse_tiktok_comments(data),
            'x':lambda data : parse_x_comments(data),
            'youtube':lambda data : parse_youtube_comments(data),
        }
    else: 
        return {
            'instagram':lambda data : parse_instagram_posts(data),
            'facebook':lambda data : parse_facebook_posts(data),
            'tiktok':lambda data : parse_tiktok_posts(data),
            'x':lambda data : parse_x_posts(data),
            'youtube':lambda data : parse_youtube_posts(data),
        }
    
"""
URL extraction mappers
These set of function are only to be triggered when running a post scraping operation.
Depending on the social network, they extract the urls and write them to the corresponding,
as this urls are the main input for the comments scrapper.
"""

def extract_facebook_urls(raw):
    urls = [post['url'] for post in raw]
    return urls

def extract_instagram_urls(raw):
    urls = [post['url'] for post in raw]
    return urls

def extract_tiktok_urls(raw):
    urls = [post['webVideoUrl'] for post in raw]
    return urls

def extract_x_urls(raw):
    return raw

def extract_youtube_urls(raw):
    return raw

def get_url_extraction_action_mapper():
    return {
        'instagram':lambda data : extract_instagram_urls(data),
        'facebook':lambda data : extract_facebook_urls(data),
        'tiktok':lambda data : extract_tiktok_urls(data),
        'x':lambda data : extract_x_urls(data),
        'youtube':lambda data : extract_youtube_urls(data),
    }