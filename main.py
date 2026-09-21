from uuid import UUID

import httpx
from fastmcp import FastMCP
from starlette.responses import JSONResponse

mcp = FastMCP("Azure Tools")


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


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "azure_tools"})