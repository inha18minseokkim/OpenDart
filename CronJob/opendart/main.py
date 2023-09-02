import os
from datetime import datetime
import asyncio
from loguru import logger

import dataCollect.openDartAnnouncementSvc as openDartAnnouncementSvc

if __name__ == "__main__":
    try:
        system_date = os.environ.get('SYSTEM_DATE') # input type - YYYYMMDD
        datetime_object = datetime.strptime(system_date, '%Y%m%d')
        procDt = datetime_object.strftime('%Y%m%d')
        logger.debug(system_date)
    except:
        procDt = datetime.now().strftime('%Y%m%d')

    lastReportAt = os.environ.get("LAST_REPORT_AT")
    logger.debug(lastReportAt)
    corpCls = os.environ.get("CORP_CLS")
    logger.debug(corpCls)

    logger.debug(f'{procDt} 기준일자 procDt')
    asyncio.run(openDartAnnouncementSvc.getAnnounceInfoByDay(procDt,procDt,lastReportAt,corpCls))