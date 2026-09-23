import re
from uuid import UUID

import httpx
from fastmcp import FastMCP
from starlette.responses import JSONResponse

mcp = FastMCP("Azure Tools")

DOMAIN_NAME_PATTERN = re.compile(
    r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\Z",
    re.IGNORECASE,
)


def validate_domain_name(domain_name: str) -> str:
    """Validate and return a DNS domain name suitable for tenant lookup."""
    if not DOMAIN_NAME_PATTERN.fullmatch(domain_name):
        raise ValueError(
            "tenant_name must be a valid domain name, such as example.com"
        )
    return domain_name


@mcp.tool
async def azure_sub_to_tenant(subscription_id: UUID) -> dict:
    """Look up Azure tenant details from an Azure subscription ID."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://sub2tenant.com/api/lookup",
                json={"subscriptionId": str(subscription_id)},
            )
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException as exc:
        raise RuntimeError("The lookup service timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Lookup service returned HTTP {exc.response.status_code}."
        ) from exc


@mcp.tool
async def azure_tenant_id_info(tenant_id: UUID) -> dict:
    """Look up Azure tenant details from a tenant ID."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://sub2tenant.com/api/lookup",
                json={"subscriptionId": str(tenant_id)},
            )
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException as exc:
        raise RuntimeError("The lookup service timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Lookup service returned HTTP {exc.response.status_code}."
        ) from exc


@mcp.tool
async def azure_tenant_name_info(tenant_name: str) -> dict:
    """Look up Azure tenant details from a tenant domain name."""
    tenant_name = validate_domain_name(tenant_name)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://sub2tenant.com/api/lookup",
                json={"subscriptionId": str(tenant_name)},
            )
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException as exc:
        raise RuntimeError("The lookup service timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Lookup service returned HTTP {exc.response.status_code}."
        ) from exc


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "azure_tools"})
