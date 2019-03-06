#!/usr/bin/env python3

# Distributed under the MIT License.

"""An API for Mitsuku[https://www.pandorabots.com/mitsuku/], a chatbot.

This is _not_ official.  It's just a little project that I'm working
on.  Usage:
```sh
python3 main.py [file]
```
file: input to chatbot.  If not found, you will enter it in stdin.

As for now, it just outputs the response to stdout.

You need the following stuff for it to work:
- Any distribution of Python, version 3.6 or above
- beautifulsoup4
- lxml
- requests
- Internet access
"""

import json
import random
import re
import sys
import urllib.parse

import bs4
import requests


if len(sys.argv) == 2:
    with open(sys.argv[-1]) as file:
        query = file.join()
elif len(sys.argv) == 1:
    print('Enter your input. Use Ctrl-D for end.')
    query = ' '.join(line for line in sys.stdin)
else:
    print('Invalid usage.')
    print()
    print(__doc__)
query = re.sub(r'\s+', ' ', query).strip()
query = urllib.parse.quote(query)

print('Retrieving response.')
url = 'https://www.pandorabots.com/mitsuku/'
session = requests.Session()
session.headers.update({
    'User-Agent': ' '.join(('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2)',
                            'AppleWebKit/537.36 (KHTML, like Gecko)',
                            'Chrome/72.0.3626.119 Safari/537.36')),
    'Referer': url
})

main_page = session.get(url).text
main_soup = bs4.BeautifulSoup(main_page, 'lxml')
botkey = re.search(r'PB_BOTKEY: "(.*)"', main_page).groups()[0]

# Mitsuku does not check your client_name really carefully (smirk) as
# long as the length is 13.
client_name = str(random.randint(1337, 9696913371337)).rjust(13, '0')
response_raw = session.post(
    f'https://miapi.pandorabots.com/talk?'
    f'botkey={botkey}&'
    f'input={query}&'
    f'client_name={client_name}&'
    f'sessionid=null&'
    f'channel=6').text
try:
    response_json = json.loads(response_raw)
except json.JSONDecodeError:
    # Sometimes Mitsuku sends stuff like pictures.
    response_json = {'responses': ["<i can't understand it, bro>"]}
# If the query is too long, Mitsuku answers in several lines.  Here
# I'll just put it into paragraphs.
response = '\n\n'.join(response_json['responses'])
print(response)
