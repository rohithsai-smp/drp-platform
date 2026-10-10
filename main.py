import asyncio
import logging
from enum import Enum
from typing import List, Optional
import uuid
from fastapi import FastAPI, BackgroundTasks, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DRPEngine")

app = FastAPI(
    title="Digital Risk Protection Platform Core Engine",
    description="Cloud-native engine for Social & App monitoring, Risk Scoring, and Automated Downstream Takedowns."
)

templates = Jinja2Templates(directory="templates")

# --- MODEL DATA SCHEMAS ---
class AssetType(str, Enum):
    SOCIAL_PROFILE = "social_profile"
    BRAND_PAGE = "brand_page"
    MOBILE_APP = "mobile_app"

class ThreatStatus(str, Enum):
    ANALYZING = "analyzing"
    HIGH_RISK_VERIFIED = "high_risk_verified"
    TAKEDOWN_REQUESTED = "takedown_requested"

class AssetPayload(BaseModel):
    brand_id: str
    target_brand_name: str
    asset_type: AssetType
    source_platform: str
    claimed_identity: str
    profile_url_or_package_id: str
    avatar_url: Optional[str] = None
    follower_count: int = 0
    has_phishing_links: bool = False

class RiskAssessment(BaseModel):
    threat_id: str
    risk_score: int
    text_similarity_score: int
    visual_similarity_score: int
    flagged_reasons: List[str]
    status: ThreatStatus

# --- CORE ALGORITHM PROCESSING ---
def get_text_similarity_percentage(s1: str, s2: str) -> int:
    """Calculates name variation matching logic via distance analysis."""
    s1, s2 = s1.lower(), s2.lower()
    if len(s1)  65 and text_score  50 else 0
    if visual_score > 80:
        flagged_reasons.append(f"Asset icon branding match match threshold critical ({visual_score}%)")

    # Threat logic evaluation calculations
    base_score = int((text_score * 0.5) + (visual_score * 0.5))
    if payload.has_phishing_links:
        base_score += 25
        flagged_reasons.append("Malicious domain phishing/credential-harvest link detected")

    final_score = min(max(base_score, 0), 100)
    current_status = ThreatStatus.HIGH_RISK_VERIFIED if final_score >= 75 else ThreatStatus.ANALYZING

    assessment = RiskAssessment(
        threat_id=threat_id, risk_score=final_score, text_similarity_score=text_score,
        visual_similarity_score=visual_score, flagged_reasons=flagged_reasons, status=current_status
    )

    # Dispatches the async backend operations loop for verified high-severity vectors
    if final_score >= 75:
        background_tasks.add_task(mock_takedown_worker, threat_id, payload)
        assessment.status = ThreatStatus.TAKEDOWN_REQUESTED

    return assessment

async def mock_takedown_worker(threat_id: str, payload: AssetPayload):
    """Simulates an asynchronous background legal abuse report dispatch loop."""
    logger.info(f"[Worker Thread] Processing automated DMCA mitigation protocol for {threat_id}")
    await asyncio.sleep(2)
    logger.info(f"[Worker Dispatched] Abuse API payload successfully submitted to {payload.source_platform}")

if __name__ == "__main__":
    import uvicorn
    # Cloud environments usually provide their own port routing proxy, listening on all interfaces (0.0.0.0) is ideal
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


