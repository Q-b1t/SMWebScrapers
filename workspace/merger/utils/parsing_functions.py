import json

# facebook functions
def get_facebook_comments(facebook_data):
  facebook_comments = list()
  for comment in facebook_data:
    comment_ = {
        'comment':comment['text'],
        "created_at":comment['date'],
        'social_network':'Facebook',
        'interactions': int(comment.get("likesCount") or 0) + int(comment.get("commentsCount") or 0) + 1
    }
    facebook_comments.append(comment_)
  return facebook_comments

def get_facebook_posts(facebook_data):
  facebook_posts = list()
  for post in facebook_data:

    post_ = {
        'comment':post['message'],
        "created_at":post['create_date'],
        'social_network':'Facebook',
        'interactions': int(post.get("comments_count") or 0) + int(post.get("reactions_count") or 0) + 1
    }
    facebook_posts.append(post_)
  return facebook_posts




# instagram functions
def clean_instagram_data(instagram_data):
  """
  The script will fail if it encounters a failed instagram post/coment.
  This functions receives the instagram data of posts or comments and cleans the
  samples with error keys
  """
  return [sample for sample in instagram_data if 'error' not in sample.keys()]



def get_instagram_comments(instagram_data):
  instagram_data = clean_instagram_data(instagram_data)
  instagram_comments = list()
  for comment in instagram_data:

    comment_ = {
        'comment':comment['text'],
        "created_at":comment['timestamp'],
        'social_network':'Instagram',
        'interactions': int(comment.get("likesCount") or 0) + 1
    }
    instagram_comments.append(comment_)
  return instagram_comments

def get_instagram_posts(instagram_data):
  instagram_data = clean_instagram_data(instagram_data)
  instagram_posts = list()
  for post in instagram_data:

    post_ = {
        'comment':post['caption'],
        "created_at":post['timestamp'],
        'social_network':'Instagram',
        'interactions': int(post.get("likesCount") or 0) + int(post.get("commentsCount") or 0) + 1
    }
    instagram_posts.append(post_)
  return instagram_posts

# tiktok functions

def get_tiktok_comments(tiktok_data):
  tiktok_comments = list()
  for comment in tiktok_data:
    likes_count = comment.get("likes_count", 0) or 0
    reply_count = comment.get("reply_count", 0) or 0
    comment_ = {
        'comment':comment['text'],
        'created_at': comment['createTimeISO'],
        'social_network': 'Tiktok',
        'interactions' : 1 + likes_count + reply_count 
    }
    tiktok_comments.append(comment_)
  return tiktok_comments


def get_tiktok_posts(tiktok_data):
  tiktok_posts = list()
  for post in tiktok_data:
    likes_count = post.get("diggCount", 0) or 0
    share_count = post.get("shareCount", 0) or 0
    play_count = post.get("playCount", 0) or 0
    collect_count = post.get("collectCount", 0) or 0
    comment_count = post.get("commentCount", 0) or 0
    post_ = {
        'comment':post['text'],
        'created_at': post['createTimeISO'],
        'social_network': 'Tiktok',
        'interactions' : 1 + likes_count + share_count + play_count + collect_count + comment_count
    }
    tiktok_posts.append(post_)
  return tiktok_posts

# youtube functions

def extract_youtube_comments(youtube_data):
  """
  This function extracts the comments from each youtube data sample since youtube's
  API extracts posts and comments together.
  """
  # extract comments from youtube
  youtube_comments = list()
  raw = youtube_data
  for video in raw:
    youtube_comments += video['comments']
  return youtube_comments



def get_youtube_posts(youtube_data):
  youtube_posts = list()
  for post in youtube_data:
    like_count = int(post.get("like_count")) if post['like_count'] != 'N/A' else 0
    favorite_count = int(post.get("favorite_count")) if post['favorite_count'] != 'N/A' else 0
    comment_count = int(post.get("comment_count")) if post['comment_count'] != 'N/A' else 0
    favorite_count = int(post.get("favorite_count")) if post['favorite_count'] != 'N/A' else 0
    view_count = int(post.get("view_count")) if post['view_count'] != 'N/A' else 0


    post_ = {
        'comment':post['title'],
        "created_at":post['creation_date'],
        'social_network':'Youtube',
        'interactions': like_count + favorite_count + comment_count + favorite_count + view_count #int(comment.get("like_count") or 0) + int(comment.get("favorite_count") or 0) +  int(comment.get("comment_count") or 0) + int(comment.get("view_count") or 0)+  int(comment.get("favorite_count") or 0) + 1
    }
    youtube_posts.append(post_)
  return youtube_posts


def get_youtube_comments(youtube_data):
  """
  The youtube api sends the comments and post in the same response. This functions receives the raw
  youtube data as received from extracion, extract the comments for each posts, and parses them according
  to our universal format.
  """
  # exract youtube comments
  raw_youtube_comments = extract_youtube_comments(youtube_data)
  # parse tourube comments
  youtube_comments = list()
  for comment in raw_youtube_comments:
    like_count = int(comment.get("like_count")) if comment['like_count'] != 'N/A' else 0

    comment_ = {
        'comment':comment['text'],
        "created_at":comment['published_at'],
        'social_network':'Youtube',
        'interactions': like_count + 1
    }
    youtube_comments.append(comment_)
  return youtube_comments


def get_youtube_data(youtube_data):
  youtube_parsed_data = list()
  youtube_posts = get_youtube_posts(youtube_data)
  youtube_comments = get_youtube_comments(youtube_data)
  youtube_parsed_data += youtube_posts
  youtube_parsed_data += youtube_comments

  return youtube_parsed_data


# x functions

def get_x_data(x_data):
  x_posts_comments = list()
  for item in x_data:
    filtered_item = {
        'comment': item.get('text'),
        'created_at': item.get('created_at'),
        'social_network': 'X',
        'interactions' : 1 + item.get("likes", 0) + item.get("impressions", 0) + item.get("replies", 0)
      }
    x_posts_comments.append(filtered_item)

  return x_posts_comments



# operational functions
def create_data_mapping(files_list):
  mapping = dict()
  for fl in files_list:
    path_handler = '/' if '/' in fl else '\\'
    social_media = fl.split(path_handler)[-1].split('.')[0].split('_')[0].lower()
    with open(fl,'r',encoding='utf-8') as f:
      mapping[social_media] = json.load(f)
    f.close()
  return mapping


def get_data_mappings(post_files,comment_files,hibrid_files):
  # load comment data
  post_mapping = create_data_mapping(post_files)
  comment_mapping = create_data_mapping(comment_files)
  hibrid_data_mapping = create_data_mapping(hibrid_files)
  return post_mapping,comment_mapping,hibrid_data_mapping



def action_mappings():
  post_action_mappings = {
      "instagram": lambda data : get_instagram_posts(data),
      "facebook": lambda data : get_facebook_posts(data),
      'tiktok':lambda data : get_tiktok_posts(data)
  }
  comment_action_mappings = {
      "instagram": lambda data : get_instagram_comments(data),
      "facebook": lambda data : get_facebook_comments(data),
      'tiktok':lambda data : get_tiktok_comments(data)

  }
  hybrid_action_mappings = {
      'youtube':lambda data : get_youtube_data(data),
      'x':lambda data : get_x_data(data)
  }
  return post_action_mappings, comment_action_mappings, hybrid_action_mappings

def merge_data(post_mapping,comment_mapping,hibrid_data_mapping):
  # get action mappings for different social networks
  post_action_mappings,comment_action_mappings,hybrid_action_mappings = action_mappings()


  total_samples = list()
  # get post information of posts
  print("[~] merging post data...")
  for social_media,data in post_mapping.items():
    print(f"[+] {len(data)} post samples found for {social_media}")
    total_samples += post_action_mappings[social_media](data)
  print('\n')
  # merge comment information for posts
  print("[~] merging comment data...")
  for social_media,data in comment_mapping.items():
    print(f"[+] {len(data)} comment samples found for {social_media}")
    total_samples += comment_action_mappings[social_media](data)
  print('\n')
  # hibrid samples
  print("[~] merging hibrid data...")
  for social_media,data in hibrid_data_mapping.items():
    out_data = hybrid_action_mappings[social_media](data)
    total_samples += out_data
    print(f"[+] {len(out_data)} samples found for {social_media}")
  print('\n')

  print(f"[+] {len(total_samples)} samples were extracted for all social media")
  return total_samples