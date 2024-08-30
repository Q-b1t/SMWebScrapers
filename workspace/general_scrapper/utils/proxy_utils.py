import requests


def add_proxy_config(actor_input,use_custom_proxy=False,proxy_url=None):
  updated_actor = actor_input.copy()
  proxy_config = dict()
  if use_custom_proxy:
    assert proxy_url is not None, '[-] proxy url required required'
    proxy_config = {
        "proxyConfiguration": {
            "useCustomProxy": True,
            "customProxyUrl": proxy_url
            }
        }
  else:
    proxy_config = {
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": [
                "RESIDENTIAL"
                ],
        "apifyProxyCountry": "MX"
        }
      }

  updated_actor |= proxy_config 
  return updated_actor


def get_proxy_location(session, proxy_url):
  session.proxies.update({"http": proxy_url, "https": proxy_url})
  try:
    response = session.get("http://ip-api.com/json")
    data = response.json()
    return {
      "ip": data.get("query"),
      "country": data.get("country"),
      "region": data.get("regionName"),
      "city": data.get("city"),
    }
  except Exception as e:
    return {"error": str(e)}


def get_proxy_url(proxy_url_template,index,session,retries = 3):
  proxy_location = None
  success = False
  for attempt in range(retries):
    proxy_url = f"{proxy_url_template}/{index}"
    print(f"[*] attempting to fecth proxy for {proxy_url}: attempt {attempt+1}/{retries}")
    proxy_location = get_proxy_location(session, proxy_url)
    if "error" in proxy_location: # fail
      print(f"[-] Failed to connect to proxy: {proxy_location['error']}. Retrying ({attempt + 1}/{retries})...")
    else: # success
      success = True 
      break
  return proxy_url,proxy_location,success
