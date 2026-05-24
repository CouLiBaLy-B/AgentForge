import hmac
import hashlib
import time
from fastapi import Request, HTTPException
from backend.core.config import settings

async def verify_slack_signature(request: Request):
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    
    if not timestamp or not signature:
        raise HTTPException(status_code=400, detail="Missing Slack headers")
        
    if abs(time.time() - int(timestamp)) > 60 * 5:
        raise HTTPException(status_code=400, detail="Request too old")
        
    body = await request.body()
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    
    my_sig = "v0=" + hmac.new(
        settings.SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(my_sig, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    return True
