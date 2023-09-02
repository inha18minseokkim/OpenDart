import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
from declaration import crtfc_key,dbUrl
import requests
from datetime import datetime, timedelta
from loguru import logger

url_code = "https://opendart.fss.or.kr/api/cvbdIsDecsn.json"
'''
crtfc_key	API 인증키	    STRING(40)	Y	발급받은 인증키(40자리)
corp_code	고유번호	        STRING(8)	Y	공시대상회사의 고유번호(8자리)
bgn_de	    시작일(최초접수일)	STRING(8)	Y	검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
end_de	    종료일(최초접수일)	STRING(8)	Y	검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
'''
dbClientUrlCB = dbUrl + '/tb_cb_info/'
dbClientUrlCode = dbUrl + '/tb_corp_code/'

dataCnt = 250
dayCnt = 100000/dataCnt

today = datetime.now() #+ timedelta(days=-31)

endDate = today.strftime('%Y%m%d')
startDate = (today - timedelta(dayCnt)).strftime("%Y%m%d")

def getSeed():
    start_date = datetime(1999, 10, 20)
    today = datetime.now()
    delta = today - start_date
    return int(delta.days) + 2
async def getCBEvent():
    # db에서 상장주식 목록 가져온다.
    # 오늘 날짜 YYYYMMDD로 가져온다.
    # 이벤트 있으면 DB에 적재. 일단 사모든 공모든 적재.
    # 여기다가 for문을 넣어야됨. 그리고 DBClient corp 부분에 한번에 다 select 해서 가져올 수 있는 리퀘스트 받아야함

    curDate = getSeed()
    logger.debug(curDate)
    n = curDate % dayCnt
    sidx = int(dataCnt * (n - 1) + 1)
    eidx = int(dataCnt * n)

    logger.debug(f'{sidx}  {eidx} 범위의 데이터 읽어옴')
    targetCorpCode = dbClientUrlCode + f'selectCorpInfoByRange/{sidx}/{eidx}'
    corpInfoByRangeRes = requests.get(targetCorpCode).json()['res']
    requestCnt = 0
    eventCnt = 0
    errorCnt = 0
    for i in corpInfoByRangeRes: #후에 로직 수정 후 바꿀 예정
        '''
        data = {
            "crtfc_key" : crtfc_key,
            "corp_code" : "00797364",
            "bgn_de" : curDate,
            "end_de" : curDate
        }
        '''
        logger.debug(i)
        logger.debug(i['corp_code'])
        data = {
            "crtfc_key" : crtfc_key,
            "corp_code" : i['corp_code'],
            "bgn_de" : startDate,
            "end_de" : endDate
        }
        res = requests.get(url_code,params=data)
        logger.debug(f'{i["corp_code"]} 에 대해서 {startDate} {endDate} 까지 데이터 조회')
        if res.json()['status'] != '000':
            if res.json()['status'] == '013':
                logger.debug('dailyCBRoutine 아무것도 없음')
                requestCnt += 1
                continue #정상 응답이 아니면 그냥 continue
            else:
                logger.debug('dailyCBRoutine 뭔가 조회 실패')
                errorCnt += 1
                continue
        try:
            resj = res.json()['list'][0]
            logger.debug(resj)
            dbres = requests.post(dbClientUrlCB + 'setCurCBInfo', json=resj,verify=False).json()
            logger.debug(dbres)
            eventCnt += 1
        except:
            logger.debug('dailyCBRoutine '+resj['corp_code'] + ' db 반영 호출 실패')
            errorCnt+=1
        else:
            logger.debug(f"dailyCBRoutine: DB반영 결과 : {dbres['code']}")
        requestCnt+=1
    logger.debug(f"dailyCBRoutine 배치 실행 결과 : 총 {requestCnt} 건 이벤트 {eventCnt} 건 실패 {errorCnt} 건")
    return

if __name__ == "__main__":
    getCBEvent()