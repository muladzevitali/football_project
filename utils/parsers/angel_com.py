"""
https://angel.co/companies/startups?
ids%5B%5D=671015
&ids%5B%5D=148266
&ids%5B%5D=669553
&ids%5B%5D=240662
&ids%5B%5D=294065
&ids%5B%5D=1146647
&ids%5B%5D=1841370
&ids%5B%5D=104786
&ids%5B%5D=752209
&ids%5B%5D=439454
&ids%5B%5D=672957
&ids%5B%5D=197949
&ids%5B%5D=240664
&ids%5B%5D=104778
&ids%5B%5D=457427
&ids%5B%5D=357104
&ids%5B%5D=365208
&ids%5B%5D=694447
&ids%5B%5D=104930
&ids%5B%5D=130805
&total=620
&page=4
&sort=signal
&new=false
&hexdigest=4da5f6f035d5112215978ff5bbc8aa6f5cd0a949
"""
# "x-csrf-token": "srFd1BcuUhQ2eBUFfz0H2TI9+cuR3pmw+nTATmhyENHU+rvZrr5KcVTH51E97cXr1klIAiTCiQq9oiIHYgdemg==" - H
# 'accept-language: en-US,en;q=0.9,ka-GE;q=0.8,ka;q=0.7' - H
# 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' - H
# 'content-type: application/x-www-form-urlencoded; charset=UTF-8' - H
# 'accept: */*' - H
# 'referer: https://angel.co/companies?locations[]=2003-Egypt' - H
# 'authority: angel.co' - H
# 'x-requested-with: XMLHttpRequest' - -data
# 'filter_data%5Blocations%5D%5B%5D=2003-Egypt&sort=signal' - -compressed
import requests

headers = {
    "Content-Type": "text/plain",
    "Origin": "https://angel.co",
    "Referer": "https://angel.co/companies?locations[]=2003-Egypt",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "x-csrf-token": "srFd1BcuUhQ2eBUFfz0H2TI9+cuR3pmw+nTATmhyENHU+rvZrr5KcVTH51E97cXr1klIAiTCiQq9oiIHYgdemg=="
}

data = {"filter_data[locations][]": "2003-Egypt", "sort": "signal"}
session = requests.session()
session.headers = headers
_ = session.get("https://angel.co/fouc_occurrences", headers=headers)
response = session.post("https://angel.co/company_filters/search_data", headers=headers, data=data)
