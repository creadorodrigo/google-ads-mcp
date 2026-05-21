import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ads_mcp.server import mcp

BASE_URL = os.getenv(
    "GOOGLE_ADS_MCP_BASE_URL",
    "https://rc-google-mcp-google-mcp.adefxc.easypanel.host"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)

# Endpoint exigido pelo ChatGPT e claude.ai
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

# Monta o MCP na rota /mcp
app.mount("/mcp", mcp.get_asgi_app())
