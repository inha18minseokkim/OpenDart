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
# 전환사채권발행 결정
import requests
from loguru import logger


class ConvertibleBondIntf(CmnEventPushSvcIntf):
    def __init__(self,msgInfo: dict):
        self.requestUrl = "https://opendart.fss.or.kr/api/cvbdIsDecsn.json"  # 전환사채권발행결정 결정 api url
        self.msgInfo = msgInfo
        self.classification = '전환사채권발행결정'
        self.msgInfo['classification'] = self.classification

    def pushMessageLoad(self) -> dict:
        self.msg = f"전환사채권 발행 결정 " \
                   f"\n회사명{self.msgInfo['corp_name']}" \
                   f"\종류 {self.msgInfo['bd_knd']} " \
                   f"\권면총액 {self.msgInfo['bd_fta']}" \
                   f"\사채 이율(표면) {self.msgInfo['bd_intr_ex']} " \
                   f"\사채만기일 {self.msgInfo['bd_mtd']}" \
                   f"\사채발행방법{self.msgInfo['']} " \
                   f"\전환비율(%) {self.msgInfo['']}" \
                   f"\전환가액{self.msgInfo['bdis_mthn']} " \
                   f"\발행주식종류 {self.msgInfo['cvisstk_knd']} " \
                   f"\전환청구기간 {self.msgInfo['cvrqpd_bgd']} ~ {self.msgInfo['cvrqpd_edd']}" \
                   f"\청약일 {self.msgInfo['sbd']} " \
                   f"납입일 {self.msgInfo['pymd']}" \
                   f"\대표주관회사{self.msgInfo['rpmcmp']} " \
                   f"\보증기관 {self.msgInfo['grint']}"
        return self.msg
