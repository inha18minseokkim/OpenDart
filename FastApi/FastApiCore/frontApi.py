from fastapi import APIRouter
from loguru import logger
import sys
sys.path.append("../../CmnUtl/DBClient")
from DBClient.corpCmnAnn import corpCmnAnnMain
frontRouter = APIRouter(tags=["Frontend"])

@frontRouter.get("/annouceDataByDate")
async def annouceDataByDate(startDt: str, endDt: str):
    logger.debug(f"수행 시작{startDt}~{endDt}")
    res = await corpCmnAnnMain.selectCorpCmnAnnByDate(startDt, endDt)
    return res
