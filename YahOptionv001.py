# YahOptionv001.py, by Tong, 10/2/2015 12:46 AM
# retrieve option prices from yahoo finance v0.01

from __future__ import division
from urllib2 import Request, urlopen
import re


def ticker_to_url1(ticker):
    url = 'http://finance.yahoo.com/q/op?s=%s+Options' % ticker
    return url


def ticker_to_url2(ticker, maturity):
    url = 'http://finance.yahoo.com/q/op?s=%s&date=%s' % (ticker, maturity)
    return url


def url_require(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
    header = {'User-Agent' : user_agent}
    req = Request(url, headers = header)
    resp = urlopen(req)
    content = resp.read()
    return content


def date_list(ticker, *html):
    if html == ():
        content = url_require(ticker_to_url1(ticker))
    else:
        content = html[0]
    content = url_require(ticker_to_url1(ticker))
    get_date = re.findall('<option data-selectbox-link="/q/op\?s=\w*&date'
                          '=\d*" value="\d*"  >\D* \d*, \d*</option>', content, re.S)
    unix_times = []
    expire_days = []
    for string in get_date:
        unix_times.append(string.split('"')[3])
        expire_days.append(string.split('>')[1].split('<')[0])
    return unix_times, expire_days


def stock_price(ticker, *html):
    if html == ():
        content = url_require(ticker_to_url1(ticker))
    else:
        content = html[0]
    get_price = re.findall('<span id="\w*" data-sq="\w*:value"'
                           '>\d*\.\d*</span>', content, re.S)
    price = float(get_price[0].split('>')[1].split('<')[0])
    return price


def strikes_list(ticker, maturity, *html):
    global split_num
    if html == ():
        content = url_require(ticker_to_url2(ticker, maturity))
    else:
        content = html[0]
    get_strike = re.findall('<a href="/q/op\?s=\w*&strike=\d*.\d*"'
                            '>\d*.\d*</a>', content, re.S)
    strikes = []
    for string in get_strike:
        strikes.append(float(string.split('>')[1].split('<')[0]))
    for i in range(len(strikes)):
        if strikes[i] > strikes[i + 1]:
            split_num = i
            break
    call_strikes = strikes[:split_num + 1]
    put_strikes = strikes[split_num + 1:]
    return call_strikes, put_strikes


def option_prices(ticker, maturity, type, strike, *html):
    if html == ():
        content = url_require(ticker_to_url2(ticker, maturity))
    else:
        content = html[0]
    if type == 'call':
        content_slice = re.findall('calls-table.*puts-table', content, re.S)[0]
        strike_len = len(strikes_list(ticker, maturity, content)[0])
        strike_num = strikes_list(ticker, maturity, content)[0].index(strike)
        row_slice = []
        for i in range(strike_len):
            if i != strike_len - 1:
                row_slice.append(re.findall('<tr data-row="%d".*<tr data-row='
                                            '"%d"' %(i,i+1), content_slice, re.S)[0])
            else:
                row_slice.append(re.findall('<tr data-row="%d".*puts-table' %i, content_slice, re.S)[0])
        a = re.findall('<div class="option_entry Fz-m.*"\s?>.*</div>', row_slice[strike_num])
        b = re.findall('<strong data-sq=":volume" data-raw="\d*">\d*</strong>', row_slice[strike_num])
    else:
        content_slice = re.findall('puts-table.*<!--END td-applet-options-table'
                                   '-->', content, re.S)[0]
        strike_len = len(strikes_list(ticker, maturity, content)[1])
        strike_num = strikes_list(ticker, maturity, content)[1].index(strike)
        row_slice = []
        for i in range(strike_len):
            if i != strike_len - 1:
                row_slice.append(re.findall('<tr data-row="%d".*<tr data-row='
                                            '"%d"' %(i,i+1), content_slice, re.S)[0])
            else:
                row_slice.append(re.findall('<tr data-row="%d".*<!--END td-'
                                            'applet-options-table-->' %i, content_slice, re.S)[0])
        a = re.findall('<div class="option_entry Fz-m.*"\s?>.*</div>', row_slice[strike_num])
        b = re.findall('<strong data-sq=":volume" data-raw="\d*">\d*</strong>', row_slice[strike_num])
    contract_name = a[0].split('>')[2].split('<')[0]
    last = float(a[1].split('>')[1].split('<')[0])
    bid = float(a[2].split('>')[1].split('<')[0])
    ask = float(a[3].split('>')[1].split('<')[0])
    change = float(a[4].split('>')[1].split('<')[0])
    perchange = float(a[5].split('>')[1].split('%')[0])/100
    volume = float(b[0].split('>')[1].split('<')[0])
    open_interest = float(a[6].split('>')[1].split('<')[0])
    implied_var = float(a[7].split('>')[1].split('%')[0])/100
    return contract_name, last, bid, ask, change, perchange, volume, open_interest, implied_var


def option_name(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[0]


def option_last(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[1]


def option_bid(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[2]


def option_ask(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[3]


def option_change(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[4]


def option_perchange(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[5]


def option_volume(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[6]


def option_open_interest(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[7]


def option_implied_var(ticker, maturity, type, strike, *html):
    return option_prices(ticker, maturity, type, strike, *html)[8]






