import pandas as pd
from urllib.parse import urlparse,urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
import whois
from datetime import datetime
import requests
import whois
from datetime import datetime

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


def getDomain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain = domain.replace("www.", "")  # Remove 'www.' if present
    return domain

def havingIP(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = 0
  return ip

def haveAtSign(url):
  if "@" in url:
    at = 1    
  else:
    at = 0    
  return at

def getLength(url):
  if len(url) < 54:
    length = 0            
  else:
    length = 1            
  return length

def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0
  
def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0
  

def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0
    
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            

def web_traffic(url):
    try:
        # Encode URL to handle special characters properly
        url = urllib.parse.quote(url)
        
        # Construct the Alexa URL to fetch traffic rank data
        alexa_url = f"http://data.alexa.com/data?cli=10&dat=s&url={url}"
        
        # Fetch the page and parse it as XML using BeautifulSoup
        with urllib.request.urlopen(alexa_url) as response:
            xml_data = response.read()
            soup = BeautifulSoup(xml_data, "xml")
        
        # Find the "REACH" tag which contains the traffic rank
        reach_tag = soup.find("REACH")
        if reach_tag is None or 'RANK' not in reach_tag.attrs:
            raise ValueError("Unable to fetch traffic rank data.")
        
        rank = int(reach_tag['RANK'])
        
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"HTTP error occurred: {e}")
        return 1
    except (ValueError, KeyError, AttributeError) as e:
        print(f"Error occurred: {e}")
        return 1
    
    # Determine if the traffic rank is below 100,000 (indicating high traffic)
    if rank < 100000:
        return 1
    else:
        return 0
 
def domainAge(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        
        # Check if domain_info is a string (indicating an error or no data)
        if isinstance(domain_info, str):
            print(f"Error: {domain_info}")
            return 1
        
        # Check if domain_info is a dictionary (indicates successful WHOIS lookup)
        if isinstance(domain_info, dict):
            # Extract creation_date and expiration_date from domain_info
            creation_date = domain_info.get('creation_date')
            expiration_date = domain_info.get('expiration_date')
            
            # If creation_date or expiration_date are lists, take the first element
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            
            # Convert string dates to datetime objects if they are strings
            if isinstance(creation_date, str):
                creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            if isinstance(expiration_date, str):
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            
            # Check if creation_date or expiration_date is None
            if expiration_date is None or creation_date is None:
                return 1
            
            # Calculate the age of the domain in days
            age_of_domain = abs((expiration_date - creation_date).days)
            
            # Convert age to months and check if less than 6 months
            if (age_of_domain / 30) < 6:
                age = 1
            else:
                age = 0
            
            return age
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
import whois
from datetime import datetime

def domainEnd(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        
        # Check if domain_info is a string (indicating an error or no data)
        if isinstance(domain_info, str):
            print(f"Error: {domain_info}")
            return 1
        
        # Extract expiration_date from domain_info
        expiration_date = domain_info.expiration_date
        
        # If expiration_date is a list, take the first element
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        
        # Convert expiration_date to datetime object if it's a string
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        
        # Check if expiration_date is None
        if expiration_date is None:
            return 1
        
        # Calculate the remaining days until domain expiration
        today = datetime.now()
        remaining_days = (expiration_date - today).days
        
        # Convert remaining days to months and check if less than 6 months
        if (remaining_days / 30) < 6:
            end = 0  # Less than 6 months until expiration
        else:
            end = 1  # 6 months or more until expiration
        
        return end
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1


def iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response):
          return 0
      else:
          return 1
      
def mouseOver(response): 
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response):
      return 1
    else:
      return 0
    
def rightClick(response):
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response):
      return 0
    else:
      return 1
    
def forwarding(url):
    try:
        response = requests.get(url, allow_redirects=True)
        if response.history:
            if len(response.history) <= 2:
                return 0
            else:
                return 1
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return 1 

def statistical_report(url):
    hostname = url
    h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
    z = int(len(h))
    if z != 0:
        y = h[0][1]
        hostname = hostname[y:]
        h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
        z = int(len(h))
        if z != 0:
            hostname = hostname[:h[0][0]]
    url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address = socket.gethostbyname(hostname)
        ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)  
    except:
        return 1
    if url_match:
        return 1
    else:
        return 0


def extract_features(url):
        features_extracted = [0]*25
        features_extracted[0] = getDomain(url)
        features_extracted[1] = havingIP(url)
        features_extracted[3]  = haveAtSign(url)
        features_extracted[4] =getLength(url)
        features_extracted[5] = getDepth(url)
        features_extracted[6] = redirection(url)
        features_extracted[7] = httpDomain(url)
        features_extracted[8] = tinyURL(url)
        features_extracted[9] = prefixSuffix(url)
        features_extracted[10] = web_traffic(url)
        features_extracted[11] = domainAge(url)
        features_extracted[12] = domainEnd(url)
        features_extracted[13] = iframe(url)
        features_extracted[14] = mouseOver(url)
        features_extracted[15] = rightClick(url)
        features_extracted[17] = forwarding(url)
        features_extracted[18] = statistical_report(url)
        #features_extracted[19] = check_iframe(url)
        #features_extracted[20] = check_age_of_domain(url)
        #features_extracted[21] = check_dns_record(url)
        #features_extracted[22] = check_web_traffic(url)
        #features_extracted[23] = get_pagerank(url)
        #features_extracted[24] = check_statistical_report(url)
        return features_extracted   

url="132.com"
print(extract_features(url))

      

  
