import datetime
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
from declaration import crtfc_key,dbUrl
import requests
import zipfile
import urllib
import asyncio
import xml.etree.ElementTree as elemTree
from loguru import logger
import mongoClient
import codecs
url_code = "https://opendart.fss.or.kr/api/corpCode.xml"

dbClientUrl = dbUrl + "/tb_corp_code/"
logger.debug(sys.path)
async def updateCode():
    logger.debug("dailyCodeRoutine 시작")
    res, _ = urllib.request.urlretrieve(url_code + "?crtfc_key=" +crtfc_key)
    zip_file_object = zipfile.ZipFile(res,'r')
    first_file = zip_file_object.namelist()[0]
    file = zip_file_object.open(first_file)
    logger.debug("dailyCodeRoutine dart에서 파일 파싱 시작")
    curDate = datetime.datetime.now().strftime("%Y%m%d")
    logger.debug(f"처리 기준 날짜 {curDate}")
    codedXmlFile = ""
    with zip_file_object.open(first_file) as readFile:
        for line in codecs.iterdecode(readFile, 'utf8'):
            codedXmlFile += line
    logger.debug("dailyCodeRoutine dart에서 파일 파싱 성공")
    tree = elemTree.fromstring(codedXmlFile)

    li = tree.findall('list')

    cnt = 0
    processCnt = 0
    skipCnt = 0
    errorCnt = 0
    for i in li:
        cnt+=1
        requestBody = mongoClient.RequestBody()
        requestBody.corp_code = i.find('corp_code').text
        requestBody.corp_name = i.find('corp_name').text
        requestBody.stock_code = i.find('stock_code').text.strip()
        requestBody.modify_date = i.find('modify_date').text

        rb = {"corp_code" : i.find('corp_code').text,
        "corp_name" : i.find('corp_name').text,
        "stock_code" : i.find('stock_code').text,
        "modify_date" : i.find('modify_date').text}

        if cnt % 500 == 0:
            logger.debug(cnt)

        logger.debug(requestBody.modify_date)
        if curDate == rb['modify_date']:
            logger.debug(f"현재 날짜 : {curDate}, 최종 갱신 날짜 : {rb['modify_date']} 수정 필요")
            try:
                await mongoClient.insertCorpInfo(requestBody)
                #requests.post(dbClientUrl + "insertCorpInfo",json=rb)
                processCnt += 1
            except Exception as e:
                logger.debug("dailyCodeRoutine 리퀘스트 에러 발생")
                errorCnt += 1
        else:
            #logger.debug(f"현재 날짜 : {curDate}, 최종 갱신 날짜 : {rb['modify_date']} 그냥 스킵")
            skipCnt+=1

    #logger.debug(resli[0],resli[-1])
    logger.debug(f"dailyCodeRoutine 성공 총 처리 : {cnt}, 갱신 : {processCnt}, 실패 : {errorCnt}")
if __name__ == "__main__":
    asyncio.run(updateCode())