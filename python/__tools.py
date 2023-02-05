# In the name of Allah

import urllib.request
import json
from base64 import b64encode
import requests

def __ready_json(req):
    if type(req) == dict:
        req = str(json.dumps(req))
    if type(req) == str:
        req = req.encode('utf-8')
    return req

def __add_basic_auth(req, username, password):
    user_pass = "{}:{}".format(username, password)
    user_pass_b = user_pass.encode()
    user_pass_e = b64encode(user_pass_b).decode('ascii')
    req.add_header('Authorization', "Basic {}".format(user_pass_e))

def __create_request(url, json, user_agent='Mozilla/5.0'):
    req = urllib.request.Request(url, json)
    req.add_header('content-type', 'application/json')
    req.add_header('User-Agent', user_agent)
    return req

def __fetch_response(req, timeout):
    response = urllib.request.urlopen(req, timeout=timeout)
    resp = json.loads(response.read())
    return resp

def j2j(url, req_json, timeout=10):
    json = __ready_json(req_json)
    # print(type(json), json)
    req = __create_request(url, json)
    resp = __fetch_response(req, timeout)
    return resp

def j2j_auth_basic(url, req_json, user_name, password, timeout=10):
    json = __ready_json(req_json)
    req = __create_request(url, json)
    __add_basic_auth(req, user_name, password)
    resp = __fetch_response(req, timeout)
    return resp

def pingPongJson(url: str, req_json: dict, timeout: float = 5, method: str = 'post') -> dict:
    method = method.lower()
    header = {
        'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.7) Gecko/2009032803"
    }
    data_json = req_json#json.dumps(req_json)
    if method == 'get':
        r = requests.get(url, json=data_json, timeout=timeout, headers=header)
    elif method == 'post':
        r = requests.post(url, json=data_json, timeout=timeout, headers=header)
    return r.json()

def pingPongBGate(url: str, function_name: str, args: dict, timeout: float = 5, method: str = 'post') -> dict:
    fer = {
        "type": function_name,
        "args": args
    }
    return pingPongJson(url, fer, timeout, method)

import datetime
from .__georgian_jalili import gregorian_to_jalali
import pytz
import typing as T

def jtoday() -> T.Tuple[int, int, int]:
    """Returns (year, month, day) of Jalali today"""
    t = iran_time(today())
    return gregorian_to_jalali(t.year, t.month, t.day)

def today():
    # from_zone = tz.tzutc()
    # to_zone = tz.gettz('Asia/Tehran')
    # utc = datetime.datetime.now()
    # utc = utc.replace(tzinfo=from_zone)
    # final = utc.astimezone(to_zone)
    return datetime.datetime.now()

def tomorrow():
    n = today()
    d = n.date()
    t = n.time()
    d2 = datetime.date.fromordinal(d.toordinal() + 1)
    return datetime.datetime(d2.year, d2.month, d2.day, t.hour, t.minute, t.second, t.microsecond)

def yesterday():
    n = today()
    d = n.date()
    t = n.time()
    d2 = datetime.date.fromordinal(d.toordinal() - 1)
    return datetime.datetime(d2.year, d2.month, d2.day, t.hour, t.minute, t.second, t.microsecond)

__irantz = pytz.timezone('Iran')
def iran_time(time: datetime.datetime=None):
    global __irantz
    if time is None:
        time = today()
    return time.astimezone(__irantz)

def has_passed(t0, t):
    tic = t0
    toc = t
    if toc.toordinal() > tic.toordinal():
        return True
    return toc.timestamp() > tic.timestamp()

def jtoday():
    """(Year, Month, Day)"""
    N = today()
    return gregorian_to_jalali(N.year, N.month, N.day)

def weekday(d=None):
    """saturday=0, friday=6
deprecated: use persian_weekday instead"""
    d = d if d is not None else today()
    return divmod(d.weekday() + 2, 7)[1]

def weekly_compare(target_weekday, target_hour, target_minute, delta, tic=today()):
    """Returns true if target <= tic <= target + delta"""
    k1 = datetime.datetime(year=2020, month=1, day=4 + target_weekday, hour=target_hour, minute=target_minute)
    k2 = k1 + delta
    # print(tic.weekday(), k1.weekday(), k2.weekday())
    if not tic.weekday() in (k1.weekday(), k2.weekday()):
        # print(1)
        return False
    T = tic.hour*60 + tic.minute
    T1 = k1.hour*60 + k1.minute
    T2 = k2.hour*60 + k2.minute
    if k1.weekday() == k2.weekday(): # All on same day
        # print(2)
        return T1 <= T and T <= T2
    elif k1.weekday() == tic.weekday(): # In first day
        # print(3)
        return T1 <= T
    else: # In second day
        # print(4)
        return T <= T2
    # print(5)
    return False

def persian_weekday(target_date: T.Union[datetime.date, datetime.datetime] = today()):
    """Returns persian weekday where:
Shanbeh = 0,
Yek-Shabeh = 1,
...,
Jomoeh = 6"""
    ewd = target_date.weekday()
    pwd = 2 + ewd
    return pwd % 7

def irantime_str(dt: datetime.datetime, include_date: bool = True, include_time: bool = True):
    s = ''
    idt = iran_time(dt)
    if include_date:
        jy, jm, jd = gregorian_to_jalali(idt.year, idt.month, idt.day)
        s += f'{jy}/{jm}/{jd}'
        if include_time:
            s += ' - '
    def zf(val) -> str:
        return str(val).zfill(2)
    s += f'{zf(idt.hour)}:{zf(idt.minute)}:{zf(idt.second)}'
    return s
