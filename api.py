import requests as r

# move these to a config file eventually
# NOTE: both of these should just contain the token; transform handled in _build_options
ck = None
jsessionid = None

instance_url = "https://dev304050.service-now.com/"
endpoints = {
    "table" : "api/now/table/"
}

def get_tables():
    url = instance_url + endpoints["table"] + "sys_db_object"
    options = _build_options()
    if (options == False):
        print("Error gathering headers for https request.")
        return
    options = dict(options)
    print(options)
    response = r.get(url, headers=options)
    
    if (response.status_code == 200):
        return response.json()
    else:
        print("Unsuccessful response detected - status_code:", response.status_code)
        return response

def get_records(table, query=None, limit=None):
    url = instance_url + endpoints['table'] + table
    params = ""
    if (query != "" and query != None):
        if (params == ""):
            params += "?"
        params += "sysparm_query=" + query
    if (limit != None and limit.isdigit()):
        if (params == ""):
            params += "?"
        params += "sysparm_limit=" + limit
    if (params != ""):
        url += params
    options = _build_options()
    if (options == False):
        print("Error gathering headers for https request.")
        return
    options = dict(options)
    response = r.get(url, headers=options)
    if (response.status_code == 200):
        print("Response received. Parsing JSON.")
        return response.json()
    else:
        print("Unsuccessful response detected - status_code:", response.status_code)
        return response


def _build_options():
    need_ck = False
    need_jsid = False
    msg = ""
    if (ck == None):
        need_ck = True
        msg += "Please set gck token "
    if (jsessionid == None):
        need_jsid = True
        if (msg == ""):
            msg += "Please set jsessionid "
        else:
            msg += "and jsessionid "
    
    if (need_ck or need_jsid):
        msg += "before attempting API calls. GCK token can be found at endpoint '/sn_devstudio_/v1/get_publish_info', and JSessionID can be found in browser dev console Network > Cookies."
        print(msg)
        return False
    
    headers = {
        "Accept": "application/json",
        "X-UserToken": ck,
        "Cookie": "JSESSIONID=" + jsessionid 
    }
    
    return headers
