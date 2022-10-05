from time import sleep as sl
from colored import fore, style
from os import system as s

import os
import json
import time
import requests
from hmac import new
from typing import Union
from hashlib import sha1
from base64 import b64encode
from threading import Thread

from random import choice
from datetime import datetime
import string
import hmac
from os import urandom, mkdir
from time import time as timestamp



name = """
╔╗─╔╗──────────╔═══╗─────╔╗
║║─║║──────────║╔══╝─────║║
║║─║╠══╦══╦═╗──║╚══╦╦═╗╔═╝╠══╦═╗
║║─║║══╣║═╣╔╝──║╔══╬╣╔╗╣╔╗║║═╣╔╝
║╚═╝╠══║║═╣║───║║──║║║║║╚╝║║═╣║
╚═══╩══╩══╩╝───╚╝──╚╩╝╚╩══╩══╩╝
"""


links = """

Made by Xsarz (@DXsarz)
GitHub: https://github.com/xXxCLOTIxXx
Telegram channel: https://t.me/DxsarzUnion
YouTube: https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q
Discord server: https://discord.gg/GtpUnsHHT4

"""


finish = """

╔═══╦══╦═╗─╔╦══╦═══╦╗─╔╗
║╔══╩╣╠╣║╚╗║╠╣╠╣╔═╗║║─║║
║╚══╗║║║╔╗╚╝║║║║╚══╣╚═╝║
║╔══╝║║║║╚╗║║║║╚══╗║╔═╗║
║║──╔╣╠╣║─║║╠╣╠╣╚═╝║║─║║
╚╝──╚══╩╝─╚═╩══╩═══╩╝─╚╝
"""


class UnknownError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class AccountLimitReached(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class TooManyRequests(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class IpTemporaryBan(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class UserNotFound(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class NotMember(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class Pohui(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)



class Generator():
    def __init__(self):
    	PREFIX = bytes.fromhex("42")
    	SIG_KEY = bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93")
    	DEVICE_KEY = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")\


    def deviceId(self):
        try:
            with open("device.json", "r") as stream:
                data = json.load(stream)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            device = self.generate_device_info()
            with open("device.json", "w") as stream:
                json.dump(device, stream, indent=4)
            with open("device.json", "r") as stream:
                data = json.load(stream)
        return data


    def generate_device_info(self):
        identifier = urandom(20)
        key = bytes.fromhex("02B258C63559D8804321C5D5065AF320358D366F")
        mac = hmac.new(key, bytes.fromhex("42") + identifier, sha1)
        device = f"42{identifier.hex()}{mac.hexdigest()}".upper()
        return {
            "device_id": device,
            "user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.5.33562)"
        }

    def signature(self, data) -> str:
        try: dt = data.encode("utf-8")
        except Exception: dt = data
        mac = new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), dt, sha1)
        return b64encode(bytes.fromhex("42") + mac.digest()).decode("utf-8")



class headers():
	def __init__(self, data = None, content_type = None, deviceId: str = None, sid: str = None):
		self.device = Generator().deviceId()
		self.User_Agent = self.device["user_agent"]
		self.sid = sid
		if deviceId!=None:self.device_id = deviceId
		else:self.device_id = self.device["device_id"]


		self.headers = {
			"NDCDEVICEID": self.device_id,
			"Accept-Language": "en-US",
			"Content-Type": "application/json; charset=utf-8",
			"User-Agent": self.User_Agent,
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Upgrade"
		}

		if data is not None:
			self.headers["Content-Length"] = str(len(data))
			self.headers["NDC-MSG-SIG"] = Generator().signature(data=data)
		if self.sid is not None:
			self.headers["NDCAUTH"] = f"sid={self.sid}"
		if content_type is not None:
			self.headers["Content-Type"] = content_type



class LIB:
    def __init__(self, proxies: dict = None, deviceId: str = None):
        self.api = "https://service.narvii.com/api/v1"
        self.proxies = proxies
        self.uid = None
        self.sid = None
        self.session = requests.Session()
        self.web_api = "https://aminoapps.com/api"
        if deviceId:self.deviceId=deviceId
        else:self.deviceId=Generator().deviceId()['device_id']

    def parser(self, data = None, content_type: str = None):
        return headers(data=data, content_type=content_type, deviceId=self.deviceId, sid=self.sid).headers




    def login(self, email: str, password: str):

        data = json.dumps({
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.deviceId,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(timestamp() * 1000)
        })
        with self.session.post(f"{self.api}/g/s/auth/login",  headers=self.parser(data=data), data=data, proxies=self.proxies) as response:
            if response.status_code != 200: return self.checkExceptions(response.text)
            else:json_response = json.loads(response.text)
        self.sid = json_response["sid"]
        self.uid = json_response["account"]["uid"]
        return self.uid



    def get_from_link(self, link: str):
        response = self.session.get(f"{self.api}/g/s/link-resolution?q={link}", headers=self.parser(), proxies=self.proxies)
        if response.status_code != 200: return self.checkExceptions(response.text)
        else: return json.loads(response.text)

    def get_user_info(self, userId: str, comId: str = None):
        if comId:response = self.session.get(f"{self.api}/x{comId}/s/user-profile/{userId}", headers=self.parser(), proxies=self.proxies)
        else:response = self.session.get(f"{self.api}/g/s/user-profile/{userId}", headers=self.parser(), proxies=self.proxies)
        if response.status_code != 200: return self.checkExceptions(response.text)
        else: return json.loads(response.text)["userProfile"]


    def join_community(self, comId):

        data = json.dumps({"timestamp": int(timestamp() * 1000)})
        response = self.session.post(f"{self.api}/x{comId}/s/community/join", headers=self.parser(data=data), data=data, proxies=self.proxies)
        if response.status_code != 200: return self.checkExceptions(response.text)
        else: return response.status_code


    def checkExceptions(self, data):
        try:
            data = json.loads(data)
            try:api_code = data["api:statuscode"]
            except:raise UnknownError(data)
        except json.decoder.JSONDecodeError:api_code = 403

        if api_code == 403:raise IpTemporaryBan(data)
        elif api_code == 219:raise AccountLimitReached(data) or TooManyRequests(data)
        elif api_code == 225:raise UserNotFound(data)
        elif api_code == 230:raise NotMember(data)
        elif api_code == 107 or api_code == 814:raise Pohui(data)
        else:raise Exception(data)


class Main:
    def __init__(self):
        self.error_color = fore.RED
        self.regular_color = fore.WHITE
        self.input_color = fore.DEEP_SKY_BLUE_2
        self.succes_color = fore.GREEN
        self.client = LIB()
        self.communities = None
        self.comIds = list()
        self.userId = None
        self.comCompleted=0
        self.dir = self.genName()
        s("cls || clear")
        print(fore.RED + style.BOLD, name, links, fore.WHITE)


    def genName(self, num: int = 8):
        g = ""
        for x in range(num):
            g = g + choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        return g

    def loadCommunityes(self):
        try:self.communities = open("communities.txt", encoding='utf-8').read().split("\n")
        except FileNotFoundError:print(self.error_color,'Communities.txt',' not found, create this file and add communities links there.',self.regular_color); exit()
        except Exception as error:print(self.error_color, f"Failed to load communities:\n{error}\n", self.regular_color); exit()

    def auth(self):
        try:
            self.client.login(email=input(f"{self.input_color}\nEmail #~ {self.regular_color}"), password=input(f"{self.input_color}\nPassword #~ {self.regular_color}"))
        except AccountLimitReached or TooManyRequests:print(f'{self.error_color}\nToo many requests, try later.\n{self.regular_color}\n');exit()
        except IpTemporaryBan:print(f'{self.error_color}\nTemporary IP ban, try later.\n{self.regular_color}\n');exit()
        except Exception as error:
            print(self.error_color,f'\nError login:\n{error}\n',self.regular_color)
            self.auth()

    def getUser(self):
        def selectTp():
            print(f'{self.succes_color}\n1)Input user Id\n2)Input user link\n')
            tp = input(f"{self.input_color}\nSelect type #~ {self.regular_color}")
            if tp == '1':getUid()
            elif tp == '2':getByLink()
            else:
                print(self.error_color, f"Select type!\n", self.regular_color)
                selectTp()
        def getUid():
            uid = input(f"{self.input_color}\nUid #~ {self.regular_color}")
            if uid not in ['', ' ']:self.userId = uid
            else:
                print(self.error_color, f"You did not enter a user ID!\n", self.regular_color)
                self.getUser()
        def getByLink():
            try:
                link_info = self.client.get_from_link(input(f"{self.input_color}\nUser Link #~ {self.regular_color}"))
                self.userId = link_info["linkInfoV2"]['extensions']['linkInfo']['objectId']
            except Exception as error:
                print(self.error_color,f'\nFail:\n{error}\n',self.regular_color)
                self.getUser()

        selectTp()


    def writer(self, text: str):
        try:mkdir(self.dir)
        except:pass
        if f'{self.userId}.txt' not in os.listdir(self.dir):open(f'{self.dir}/{self.userId}.txt', 'w')
        with open(f'{self.dir}/{self.userId}.txt', 'r', encoding="utf-8", errors="ignore") as file:
            text = f"{file.read()}\n{text}"
            file.close()
        with open(f'{self.dir}/{self.userId}.txt', 'w', encoding="utf-8", errors="ignore") as file:
            file.write(text)
            file.close()



    def searchProcess(self):
        info = self.client.get_user_info(self.userId)
        name = info['nickname']
        icon = info['icon']
        aminoId = info['aminoId']
        createTime = info['createdTime']
        uid = info['uid']
        text = f"""
        ===============GLOBAL PROFILE===============
        GLOBAL NAME: {name}
        GLOBAL ICON: {icon}
        AMINO ID: {aminoId}
        CREATE TIME: {createTime}
        USER ID: {uid}
        =============== communities ===============
        """
        self.writer(text)
        print(f'{self.succes_color}\nGlobal profile data received, all information will be in the folder "{self.dir}".{fore.ORANGE_4A}\n\nSearching for a user among communities is a long process, we recommend that you leave the script running while doing your own thing.{self.regular_color}\n')
        for comL in self.communities:
            try:
                self.comCompleted+=1
                profileStatus = f'{self.error_color}Profile not found'
                users=list()
                com = self.client.get_from_link(comL)["linkInfoV2"]["extensions"]["community"]
                sl(4.5)
                name = com["name"]
                comId = com["ndcId"]
                try:self.client.join_community(comId)
                except:pass
                try:
                    try:
                        info = self.client.get_user_info(self.userId, comId)
                        profileStatus = f'{self.succes_color}Profile found'
                    except UserNotFound:pass
                    local_name = info['nickname']
                    local_icon = info['icon']
                    text = f"""
                    -----------{name}-----------
                    ~community url: {comL}
                    ~user name: {local_name}
                    ~user icon: {local_icon}
                    """
                    if profileStatus == f'{self.succes_color}Profile found': self.writer(text)
                except AccountLimitReached or TooManyRequests:print(f'{self.error_color}\nToo many requests, pause 160 seconds.{self.regular_color}\n');sl(160)
                except IpTemporaryBan:print(f'{self.error_color}\nTemporary IP ban, pause 360 seconds.{self.regular_color}\n');sl(360)
                print(f"\n~# {self.input_color}COMMUNITY: {self.succes_color}{name}{self.regular_color}\n~# {self.input_color}PROFILE: {profileStatus}{self.regular_color}\n~# {self.input_color}COMMUNITIES COMPLETED: {self.succes_color}[{self.error_color}{int(self.comCompleted/len(self.communities)*100)}% ({self.comCompleted} of {len(self.communities)}){self.succes_color}]{self.regular_color}\n")

            except AccountLimitReached or TooManyRequests:print(f'{self.error_color}\nToo many requests, pause 160 seconds.{self.regular_color}\n');sl(160)
            except IpTemporaryBan:print(f'{self.error_color}\nTemporary IP ban, pause 360 seconds.{self.regular_color}\n')
            except NotMember:print(f'{self.error_color}\nFailed to enter the community "{name}" (maybe it is closed).\n{self.regular_color}\n')
            except Pohui:pass
            except Exception as error:print(f'{self.error_color}\nError:\n{error}{self.regular_color}\n')
        print(self.succes_color, finish, self.regular_color)

if __name__ == '__main__':
    main = Main()
    main.loadCommunityes()
    main.auth()
    main.getUser()
    main.searchProcess()