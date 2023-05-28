from datetime import datetime
import traceback
from urllib.request import urlopen, Request
from json import loads, load
from csv import DictReader, DictWriter

from bs4 import BeautifulSoup as BSoup
from lxml import etree
import plotly.express as px 

IPINFO_TOKEN = None
CACHE_FILE_PATH = None
CONFIG_FILE_PATH = "config.json"
IP_LOC_CACHE = {}

def get_history_link(source_page):
    '''
        Locate and return the edit history link for a given page
    '''
    print("Finding edit history link")
    history_link = None
    
    response = urlopen(source_page).read().decode()
    tree = etree.HTML(response)

    history_element = tree.xpath("//li[@id='ca-history']/a")
    if history_element:
        history_element = history_element[0]
        history_link = history_element.get("href")

    if history_link: 
        history_link = f"https://en.wikipedia.org{history_link}&offset=&limit=500"
        print("Link found")

    return history_link

def get_edit_history(source_page):
    '''
        For a given edit history, identifies all anonymous edits and its log time
    '''

    print("Parsing edit history")
    response = urlopen(source_page).read().decode()
    tree = etree.HTML(response)

    ip_change_log = {}
    edit_logs = tree.xpath("//*[@id='pagehistory']/ul[@class='mw-contributions-list']//li")
    for log in edit_logs:
        user_id = log.xpath(".//*[contains(@class, 'mw-anonuserlink')]")
        if not user_id: 
            continue
        user_ip = user_id[0].xpath('./bdi')[0].text
        
        log_datetime = log.xpath(".//*[@class='mw-changeslist-date']")
        if log_datetime: 
            log_datetime = log_datetime[0].text
        else: continue

        log_datetime = datetime.strptime(log_datetime, '%H:%M, %d %B %Y')

        if user_ip not in ip_change_log:
            ip_change_log[user_ip] = []
        ip_change_log[user_ip].append(log_datetime)        
    
    return ip_change_log

def get_config(config_file_path):
    '''
        Read and populate config variables
    '''
    global IPINFO_TOKEN, CONFIG_FILE_PATH, CACHE_FILE_PATH

    try:
        with open(config_file_path, 'r') as f:
            json_data = load(f)
            IPINFO_TOKEN = json_data['IPINFO_TOKEN']
            CACHE_FILE_PATH = json_data['CACHE_FILE_PATH']
    except Exception as e:
        traceback.print_exc()
        exit()

def read_cache(cache_file_path):
    '''
        Return JSON object created from CSV file
    '''
    cache_data = {}
    field_names = []
    with open(cache_file_path, 'r') as f:
        csv_reader = DictReader(f)
        field_names = csv_reader.fieldnames
        for row in csv_reader:
            cache_data[row['ip']] = row
        
    return {
        "cache_data": cache_data, 
        "field_names": field_names
    }

def update_cache(cache_file_path, write_data):
    if write_data.__class__ == dict:
        write_data = [write_data, ]
    
    with open(cache_file_path, 'r') as f:
        reader = DictReader(f)
        field_names = reader.fieldnames
    
    write_headers = False
    if not field_names:
        write_headers = True
        field_names = list(write_data[0].keys())
    
    with open(cache_file_path, 'a') as f:
        writer = DictWriter(f, field_names)
        if write_headers:
            print("Writing headers")
            writer.writeheader()
        writer.writerows(write_data)

def convert_ip_to_location(ip_addresses):
    '''
        For given IP, first check in cache for existing geolocation details.
        If not found, make an api call to fetch the details.
        For IPs where API call was needed, are updated in cache file as well as process object.
    '''
    global IPINFO_TOKEN, IP_LOC_CACHE, CACHE_FILE_PATH

    url = "https://ipinfo.io/{ip_addr}?token={token}"
    if IP_LOC_CACHE == {}:
        cache_data = read_cache(CACHE_FILE_PATH)
        IP_LOC_CACHE = cache_data['cache_data']
    
    cache_update_data = {}
    ip_location = {}

    for ip_addr in ip_addresses:
        # Check in cache
        if ip_addr in IP_LOC_CACHE:
            print(f"{ip_addr} found from cache")
            ip_location[ip_addr] = IP_LOC_CACHE[ip_addr]['loc']
            continue
        
        # Not found in cache
        response = urlopen(Request(
            url=url.format(ip_addr=ip_addr, token=IPINFO_TOKEN)
        ))
        response_data = loads(response.read().decode())
        # Update cache
        IP_LOC_CACHE[ip_addr] = response_data
        cache_update_data[ip_addr] = response_data
        ip_location[ip_addr] = response_data['loc']

    update_cache(CACHE_FILE_PATH, list(cache_update_data.values()))

    return ip_location

def main_func():
    get_config(CONFIG_FILE_PATH)
    # Get edit history source
    history_link = get_history_link("https://en.wikipedia.org/wiki/Web_scraping")

    # Parse edit history
    anon_change_log = get_edit_history(history_link)

    # Convert anonymous edits to geolocations
    ip_to_location = convert_ip_to_location(list(anon_change_log.keys()))

    # Create a geoplot for anonymous edits
    all_locations = list(ip_to_location.items())
    ip_addresses, latitudes, longitudes = [], [], []
    for ip_addr, location in all_locations:
        lat, long = location.split(",")
        ip_addresses.append(ip_addr)
        latitudes.append(lat)
        longitudes.append(long)

    fig = px.scatter_geo(hover_name=ip_addresses, lat=latitudes, lon=longitudes, projection="natural earth")
    fig.show()
    
    # data = read_cache(CACHE_FILE_PATH)
    # update_cache(CACHE_FILE_PATH, { "ip": "103.137.152.169", "city": "Mumbai", "region": "Maharashtra", "country": "IN", "loc": "19.0728,72.8826", "org": "AS58678 Intech Online Private Limited", "postal": "400070", "timezone": "Asia/Kolkata" })

if __name__ == "__main__":
    main_func()