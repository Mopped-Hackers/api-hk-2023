import pandas as pd
import os
from application.main.config import settings
from application.main.components.GenAlg.town import *
class LoggerInstance(object):
    def __new__(cls):
        from application.main.utility.logger.custom_logging import LogHandler

        return LogHandler()

class DefaultTownInstance():
    def __new__(cls):
        from application.main.components.GenAlg import town

        return town.create_default_town()


class IncludeAPIRouter(object):
    def __new__(cls):
        from fastapi.routing import APIRouter

        router = APIRouter()

        # route 1 -> /
        # ------------------------
        from application.main.routers.default import router as default
        router.include_router(default, prefix="", tags=["default route"])

        # route 2 -> /ai
        # ------------------------
        from application.main.routers.ai import router as ai
        router.include_router(ai, prefix="/ai", tags=["ai route"])

        # route 3 -> /geom
        # ------------------------
        from application.main.routers.geom import router as geom
        router.include_router(geom, prefix="/geom", tags=["geom route"])

        return router

DEFAULT_TOWN = DefaultTownInstance()
# print(calculate_score_for_town(DEFAULT_TOWN))
# update_town(DEFAULT_TOWN, [1,2])
# instance creation
logger_instance = LoggerInstance()
