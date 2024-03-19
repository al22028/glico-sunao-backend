# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Server
from aws_lambda_powertools.utilities.typing import LambdaContext
from database.base import BGLModel
from middlewares.common import handler_middleware
from pydantic import BaseModel, Field
from routes import bgl

logger = Logger()

if not BGLModel.exists():
    logger.info("Creating BGLModel table")
    BGLModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


servers = [
    Server(
        url="http://localhost:3333/local", description="Local Development Server", variables=None
    ),
]
app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(
    path="/swagger",
    title="Glico SUNAO Application API",
    summary="Documentation Glico SUNAO Application API",
    description="This is the API documentation for Glico SUNAO Application API.",
    servers=servers,
)

app.include_router(router=bgl.router, prefix="/bgl")


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
