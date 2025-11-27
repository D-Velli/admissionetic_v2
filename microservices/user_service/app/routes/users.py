from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db     
from app.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserRead)
def read_current_user(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


@router.get("/", response_model=schemas.UserList)
def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    items = crud.get_users(db, skip=skip, limit=limit)
    total = crud.count_users(db)
    return schemas.UserList(total=total, items=items)


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    # admin: models.User = Depends(get_current_admin),
):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = crud.update_user(db, user, user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_user(db, user)
    return None
