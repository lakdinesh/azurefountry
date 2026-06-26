import logging
from opentelemetry import trace
from backend.app.config import settings

logger = logging.getLogger("enterprise-agent")
logging.basicConfig(level=logging.INFO)

tracer = trace.get_tracer("enterprise-agent")

if settings.APPLICATIONINSIGHTS_CONNECTION_STRING:
    try:
        from azure.monitor.opentelemetry import configure_azure_monitor

        configure_azure_monitor(
            connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING
        )
        logger.info("Application Insights enabled.")
    except Exception as e:
        logger.warning("Application Insights disabled: %s", e)