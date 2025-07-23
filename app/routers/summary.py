from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.summary import SummaryCreate, SummaryOut
from app.db.session import get_db
from app.models.user import User
from app.models.summary import Summary
from app.services.auth import get_current_user, get_current_admin
from app.utils.summarizer import summarize_url

router = APIRouter()


@router.post("/", response_model=SummaryOut)
async def summarize_article(data: SummaryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    url_str = str(data.url)
    summary_text = summarize_url(url_str)
    summary = Summary(
        url=url_str,
        summary_text=summary_text,
        owner_id=current_user.id
    )
    db.add(summary)
    await db.commit()
    await db.refresh(summary)
    return summary


@router.get("/all", response_model=list[SummaryOut])
def get_all_summaries(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return db.query(Summary).all()
