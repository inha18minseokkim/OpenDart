import json
import sys

sys.path.append("../..")  # 상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
sys.path.append("..")
from FastApiCore.declaration import crtfc_key, dbUrl, sendDiscordMessage
from .eventPushSvcIntf import CmnEventPushSvcIntf

'''
사용 파라미터 : 회사코드, 날짜
주요 내용 조립해서 푸시 서버에 보내줌
서버에서 한번 보내줌
'''
# 무상증자 결정
import requests
from loguru import logger


class FreeIssueIntf(CmnEventPushSvcIntf):
    def __init__(self,msgInfo: dict):
        self.requestUrl = "https://opendart.fss.or.kr/api/fricDecsn.json"  # 무상증자 결정 api url
        self.msgInfo = msgInfo
        self.classification = '무상증자결정'
        self.msgInfo['classification'] = self.classification

    def pushMessageLoad(self) -> dict:
        self.msg = f"무상증자 결정 \n 회사명{self.msgInfo['corp_name']} \n 발행주식 수{self.msgInfo['nstk_ostk_cnt']} \n 주당액면가 {self.msgInfo['fv_ps']}" \
              f"\n 신주상장예정일 {self.msgInfo['nstk_lstprd']} \n접수번호 : {self.msgInfo['rcept_no']}"
        return self.msg
