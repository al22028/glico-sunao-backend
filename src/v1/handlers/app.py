# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Server
from aws_lambda_powertools.utilities.typing import LambdaContext
from config.api import STAGE
from database.base import BGLModel, Hba1cModel
from middlewares.common import handler_middleware
from pydantic import BaseModel, Field
from routes import bgl, hba1c

logger = Logger()

if STAGE == "local" or STAGE == "dev":
    if not BGLModel.exists():
        logger.info("Creating BGLModel table")
        BGLModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    if not Hba1cModel.exists():
        logger.info("Creating Hba1cModel table")
        Hba1cModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

local_server = Server(
    url="http://localhost:3333", description="Local Development Server", variables=None
)
dev_server = Server(
    url="https://loa1jiqb4j.execute-api.ap-northeast-1.amazonaws.com/dev",
    description="Development Server",
    variables=None,
)

servers = []
if STAGE == "local":
    servers.append(local_server)
if STAGE == "dev":
    servers.append(dev_server)

app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(
    path="/swagger",
    title="Glico SUNAO Application API",
    summary="Documentation Glico SUNAO Application API",
    description="This is the API documentation for Glico SUNAO Application API.",
    servers=servers,
)

app.include_router(router=bgl.router, prefix="/bgl")
app.include_router(router=hba1c.router, prefix="/hba1c")


class HealthCheckSchema(BaseModel):
    status: str = Field(..., description="Health Check Status", example="ok")  # type: ignore


@app.get(
    "/healthcheck",
    cors=True,
    summary="Health Check",
    description="Check the health of the application.",
    response_description="Health Check",
    tags=["default"],
    operation_id="healthcheck",
)
def health_check() -> HealthCheckSchema:
    return HealthCheckSchema(**{"status": "ok"})


@handler_middleware
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict[str, str | int]:
    return app.resolve(event, context)
