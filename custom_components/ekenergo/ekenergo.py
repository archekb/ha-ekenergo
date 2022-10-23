from functools import reduce
from datetime import datetime
from logging import NullHandler
from typing import Any
import lxml.html
import aiohttp
from homeassistant.util import slugify

from .const import DOMAIN, LOGGER, EKENERO_GET_URL, EKENERO_SEND_URL

SHOULD_CONTAINS = ["address", "debt", "hiddenInputs", "indicators", "isExists"]


class Ekenergo:
    def __init__(self, account: str, phone: str) -> None:
        self._account = account
        self._phone = phone
        self._loaded = None
        self._sended = None
        self._data = {}
        self._indicators_data = {}

    def deviceInfo(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self._account)},
            "manufacturer": "Екатеринбургэнерго",
            "model": "Энергоснабжение",
            "name": f"{DOMAIN}_{self._account}",
        }

    async def isExist(self) -> bool:
        if self._loaded is None:
            await self.pull()

        return self._data.get("isExists", False)

    async def pull(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{EKENERO_GET_URL}{self._account}') as resp:
                self._data = await resp.json()
                if resp.status == 200 and all(x in self._data.keys() for x in SHOULD_CONTAINS):
                    self._loaded = datetime.now()
                    self._indicators_data = {}
                    indicators = self._data.get("indicators", [])
                    if isinstance(indicators, list):
                        for i in range(len(indicators)):
                            self._indicators_data[slugify(indicators[i].get("registr"))] = { "index": i, "new_value": indicators[i].get("previousValue"), "value": indicators[i].get("previousValue"), "attrs":indicators[i], "name": indicators[i].get("registr") }

                else:
                    raise Exception(f"Can't load or data format is broken, responce code {resp.status}")

    async def push(self) -> None:
        if not self.push_validate():
            return

        post_data = await self.parseHiddenInputs()
        post_data["phone"] = "" if self._phone is None else self._phone
        for v in self._indicators_data.values():
            post_data[f"show{v['index']}"] = v["new_value"]

        async with aiohttp.ClientSession() as session:
            async with session.post(EKENERO_SEND_URL, data=post_data) as resp:
                if resp.status == 200 and "Показания приняты в обработку" in await resp.text():
                    self._sended = datetime.now()

    def push_validate(self) -> bool:
        has_new = False
        for v in self._indicators_data.values():
            if v["value"] != v["new_value"]:
                has_new = True
                break

        if not has_new:
            LOGGER.warning("Nothing for push")
            return False

        return True


    async def parseHiddenInputs(self) -> dict:
        data = {}
        for input in self._data.get("hiddenInputs", []):
            h = lxml.html.fragment_fromstring(input, create_parent=False)
            inp = h.xpath("//input")
            for i in inp:
                if i.attrib["name"].strip() != "":
                    data[i.attrib["name"].strip()] = i.attrib["value"].strip()
        return data

    def setIndicator(self, index: str, value: int) -> None:
        self._indicators_data[index]["new_value"] = value

    def get(self, path:str, default:Any = None) -> Any:
        if path == "last_update":
            return self._loaded
        elif path == "last_send":
            return self._sended        
        elif path == "account":
            return self._account
        elif path == "indicator_data":
            return self._indicators_data
        elif path.startswith("indicator_data"):
            p = path.split(".")
            return ichain(self._indicators_data, *p[1:], default = default)

        p = path.split(".")
        return ichain(self._data, *p, default = default)

def ichain(obj: object, *items: list, default:Any = None) -> Any:
    """
    Gets through a chain of items handling exceptions with None value.
    Useful for data restored from a JSON string: ichain(data, 'result', 'users', 0, 'address', 'street')
    """
    if obj is None:
        return default

    def get_item(obj, item):
        if obj is None:
            return default

        try:
            return obj[item]

        except:
            try:
                return obj[int(item)]

            except:
                return default


    return reduce(get_item, items, obj)

# get:
# account: null
# address: null
# calculateUntil: null
# debt: null
# district: null
# email: null
# hiddenInputs: null
# indicators: null
# isExists: false
# isUL: false
# manager: null
# phone: null

# post:
# show0: 4380
# show1: 3760
# show00: 27322801            
# show01: День
# show02: 4378
# show03: 01.06.2022
# show04: 4378
# show05: 01.06.2022
# show06: 
# show07: 111508732
# show08: 1
# show09: 5317113005
# show010: Меркурий 206 N (6,2) 2-зон
# show011: 1
# col: 12
# row: 2
# show10: 27322801            
# show11: Ночь
# show12: 3745
# show13: 01.06.2022
# show14: 3745
# show15: 01.06.2022
# show16: 
# show17: 111508732
# show18: 2
# show19: 5317113005
# show110: Меркурий 206 N (6,2) 2-зон
# show111: 1
# col: 12
# row: 2
# ip: 10.52.4.254
# phone: 