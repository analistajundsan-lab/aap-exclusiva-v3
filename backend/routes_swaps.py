from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from models import Swap, AuditLog, get_db
from schemas import SwapCreate, SwapResponse, SwapUpdate
from auth import get_current_user, require_role
from models import User, UserRole
from typing import List, Optional

router = APIRouter(prefix="/swaps", tags=["swaps"])


@router.post("/", response_model=SwapResponse, status_code=status.HTTP_201_CREATED)
async def create_swap(
    body: SwapCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if body.vehicle_out == body.vehicle_in:
        raise HTTPException(
            status_code=422,
            detail="Os prefixos SAI e ENTRA não podem ser iguais",
        )
    swap = Swap(**body.model_dump(), created_by=current_user.id)
    db.add(swap)
    db.flush()  # garante swap.id antes do AuditLog
    db.add(AuditLog(user_id=current_user.id, action="CREATE", resource="swap", resource_id=swap.id))
    db.commit()
    db.refresh(swap)
    return swap


@router.get("/", response_model=List[SwapResponse])
async def list_swaps(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    vehicle_out: Optional[str] = None,
    vehicle_in: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Swap).order_by(Swap.created_at.desc())
    
    if vehicle_out:
        query = query.filter(Swap.vehicle_out.ilike(f"%{vehicle_out}%"))
    if vehicle_in:
        query = query.filter(Swap.vehicle_in.ilike(f"%{vehicle_in}%"))
    
    return query.offset(skip).limit(limit).all()


@router.get("/{swap_id}", response_model=SwapResponse)
async def get_swap(
    swap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    if not swap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Troca não encontrada")
    return swap


@router.put("/{swap_id}", response_model=SwapResponse)
async def update_swap(
    swap_id: int,
    body: SwapUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    if not swap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Troca não encontrada")
    
    if current_user.role != UserRole.ADMIN and swap.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")
    
    if body.vehicle_out and body.vehicle_in and body.vehicle_out == body.vehicle_in:
        raise HTTPException(status_code=422, detail="Os prefixos SAI e ENTRA não podem ser iguais")
    
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(swap, field, value)
    
    db.add(AuditLog(user_id=current_user.id, action="UPDATE", resource="swap", resource_id=swap_id))
    db.commit()
    db.refresh(swap)
    return swap


@router.delete("/{swap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_swap(
    swap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SUPERVISOR, UserRole.ADMIN)),
):
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    if not swap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Troca não encontrada")
    # SUPERVISOR e ADMIN podem deletar qualquer swap
    db.add(AuditLog(user_id=current_user.id, action="DELETE", resource="swap", resource_id=swap_id))
    db.delete(swap)
    db.commit()

