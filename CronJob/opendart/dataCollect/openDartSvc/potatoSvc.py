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
# 감자 결정
import requests
from loguru import logger


class potatoIntf(CmnEventPushSvcIntf):
    def __init__(self,msgInfo: dict):
        self.requestUrl = "https://opendart.fss.or.kr/api/crDecsn.json"  # 감자 결정 api url
        self.msgInfo = msgInfo
        self.classification = '감자결정'
        self.msgInfo['classification'] = self.classification

    def pushMessageLoad(self) -> dict:
        self.msg = f"감자결정 \n회사 명{self.msgInfo['corp_name']} \n감자비율(보통주식){self.msgInfo['cr_rt_ostk']} " \
                   f"\n감자비율(기타주식){self.msgInfo['cr_rt_estk']} " \
                   f"\n감자사유{self.msgInfo['cr_rs']} \n명의개서정지기간{self.msgInfo['crsc_trnmsppd']}" \
                   f" \n매매거래 정지예정기간{self.msgInfo['crsc_trspprpd_bgd']}~{self.msgInfo['crsc_trspprpd_edd']}"
        return self.msg
