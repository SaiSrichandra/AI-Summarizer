from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserOut, UserWithSummaries
from app.db.session import get_db
from app.services.auth import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_own_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/summaries", response_model=UserWithSummaries)
async def get_my_summaries(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(User)
        .options(selectinload(User.summaries))
        .where(User.id == current_user.id)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user

@router.get("/all", response_model=list[UserWithSummaries])
async def get_all_users_with_summaries(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    stmt = select(User).options(selectinload(User.summaries))
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users
