import datetime
import sys,os
sys.path.append("../..") #상위 경로를 현재 경로에 넣어 declaration 파일 임포트 가능
from FastApiCore.declaration import crtfc_key,dbUrl
from DBClient.corpCode import corpCodeMain
import requests
import asyncio
import zipfile
import urllib
import xml.etree.ElementTree as elemTree
from loguru import logger
import codecs
url_code = "https://opendart.fss.or.kr/api/corpCode.xml"

dbClientUrl = dbUrl + "/tb_corp_code/"
#db 처음 개시할 때 사용하는 배치
async def initCode():
    logger.debug("initCodeRoutine 시작rr")
    res, _ = urllib.request.urlretrieve(url_code + "?crtfc_key=" +crtfc_key)
    zip_file_object = zipfile.ZipFile(res,'r')
    first_file = zip_file_object.namelist()[0]
    file = zip_file_object.open(first_file)
    logger.debug("initCodeRoutine dart에서 파일 파싱 시작")
    codedXmlFile = ""
    with zip_file_object.open(first_file) as readFile:
        for line in codecs.iterdecode(readFile, 'utf8'):
            codedXmlFile += line
    logger.debug("initCodeRoutine dart에서 파일 파싱 성공")
    tree = elemTree.fromstring(codedXmlFile)

    li = tree.findall('list')

    cnt = 0
    processCnt = 0
    skipCnt = 0
    errorCnt = 0
    requestList = []
    for i in li:
        cnt+=1
        rb = {"corp_code" : i.find('corp_code').text.strip(),
        "corp_name" : i.find('corp_name').text.strip(),
        "stock_code" : i.find('stock_code').text.strip(),
        "modify_date" : i.find('modify_date').text.strip()}
        if(len(rb['stock_code']) != 0):
            logger.debug(rb)
            requestList.append(rb)
        if cnt % 500 == 0:
            logger.debug(cnt)
            processCnt += len(requestList)
            logger.debug({"list": requestList})
            #requests.post(dbClientUrl + 'insertOrUpdateCorpInfoArr',json={"list": requestList})
            corpCodeMain.insertOrUpdateCorpInfoArr(requestList)
            requestList.clear()
    if len(requestList) != 0:
        logger.debug(cnt)
        processCnt += len(requestList)
        logger.debug({"list": requestList})
        #requests.post(dbClientUrl + 'insertOrUpdateCorpInfoArr', json={"list": requestList})
        corpCodeMain.insertOrUpdateCorpInfoArr(requestList)
        requestList.clear()
    logger.debug(f"initCodeRoutine 성공 총 처리 : {cnt}, 갱신 : {processCnt}")
