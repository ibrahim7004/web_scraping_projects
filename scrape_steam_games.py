import requests     # For accessing the web page (could access via lxml as well, but can cause issues for some webpages)
from lxml import html

url = 'https://store.steampowered.com/search/?sort_by=Released_DESC&os=win&filter=popularnew'

webpage = requests.get(url)

doc = html.fromstring(webpage.content)

new_releases = doc.xpath('//div[@id="search_resultsRows"]')[0]    
# // is the 'forall' equivalent in lmxl, and div tells lxml we're searching for a div tag.

titles = new_releases.xpath('.//span[@class="title"]/text()')     
# the . before // tells lxml that we're only interested in the children tags of the new releases tag.
# /text() identifies that we want the text contained in that tag (so the title in this case).

prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

dates = new_releases.xpath('.//div[@class="col search_released responsive_secondrow"]/text()')

# Extracting the platform name from the displayed image - will use the pre-set names used as class names for different platforms.
main_div = new_releases.xpath('.//div[@class="col search_name ellipsis"]')     # Extracting the main div tag containing the platform tag

total_platforms = []    

for game in main_div:  # iterating over all main tags to find all contained platform image tags
    temp = game.xpath('.//span[contains(@class, "platform_img")]')  # store all platform tags which are class tags and contain 'platform_img' in the class name
    platforms = [t.get('class').split(' ')[-1] for t in temp]   # Using list comprehension to obtain class names (via '.get'), 
    # and split them using '.split' to get the last part of the class name (e.g. 'win', 'mac', etc.)
    if 'hmd_separator' in platforms:    # 'hmd_separator' often included in these tags but is not a platform, so remove that.
        platforms.remove('hmd_separator')
    total_platforms.append(platforms)   # Append to our list of all the platforms.


output = []

for info in zip(titles,prices, dates, total_platforms):     # Using zip to iterate over all the lists in parallel.
    resp = {}
    resp['Title'] = info[0]
    resp['Price'] = info[1]
    resp['Release Date'] = info[2]
    resp['Platform'] = info[3][0]
    output.append(resp)     # Store all info into final output list.

for i in output:
    for a, b in i.items():
        print('{}: {}'.format(a, b))
