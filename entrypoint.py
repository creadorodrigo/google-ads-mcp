import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ads_mcp.server import mcp

BASE_URL = os.getenv(
    "GOOGLE_ADS_MCP_BASE_URL",
    "https://rc-google-mcp-google-mcp.adefxc.easypanel.host"
)

# Cria o ASGI app do MCP
mcp_app = mcp.http_app(path="/mcp")

# FastAPI herdando o lifespan do MCP
app = FastAPI(lifespan=mcp_app.lifespan)

@app.get("/.well-known/oauth-protected-resource")
async def oauth_protected_resource():
    return JSONResponse({
        "resource": BASE_URL,
        "authorization_servers": [BASE_URL],
        "scopes_supported": [
            "openid",
            "https://www.googleapis.com/auth/adwords"
        ],
        "bearer_methods_supported": ["header"]
    })

# Monta o MCP
app.mount("/", mcp_app)
