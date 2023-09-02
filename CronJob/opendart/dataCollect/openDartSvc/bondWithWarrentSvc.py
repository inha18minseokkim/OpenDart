import json
import sys

sys.path.append("../..")  # 상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append("..")
from .eventPushSvcIntf import CmnEventPushSvcIntf

'''
사용 파라미터 : 회사코드, 날짜
주요 내용 조립해서 푸시 서버에 보내줌
서버에서 한번 보내줌
'''
# 신주인수권부사채권 결정
import requests
from loguru import logger


class BondWithWarrantIntf(CmnEventPushSvcIntf):
    def __init__(self,msgInfo: dict):
        self.requestUrl = "https://opendart.fss.or.kr/api/cvbdIsDecsn.json"  # 신주인수권부사채권 결정 api url
        self.msgInfo = msgInfo
        self.classification = '신주인수권부사채권발행결정'
        self.msgInfo['classification'] = self.classification

    def pushMessageLoad(self) -> dict:
        self.msg = f"{self.msgInfo}"
        return self.msg
