from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole, Role
from app.utils.security import decode_token, decode_token_no_expiry
from app.config import settings

security = HTTPBearer(auto_error=False)

# =============================================================================
# ⚠️  DEV MODE — TẮT TOÀN BỘ KIỂM TRA BẢO MẬT KHI DEBUG=True
#     Chỉ dùng để phát triển frontend. KHÔNG dùng trên production!
# =============================================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    # ── DEBUG BYPASS ────────────────────────────────────────────────────────
    if settings.DEBUG:
        # Cố giải mã token (bỏ qua hết hạn)
        if credentials:
            payload = decode_token_no_expiry(credentials.credentials)
            if payload:
                user_id = payload.get("sub")
                if user_id:
                    user = db.query(User).filter(User.user_id == int(user_id)).first()
                    if user:
                        return user
        # Fallback: trả về user đầu tiên trong DB (thường là admin seed)
        fallback = db.query(User).filter(User.status == "active").first()
        if fallback:
            return fallback
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No users in DB — run seed.py first")
    # ── PRODUCTION AUTH (nguyên gốc) ───────────────────────────────────────
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.user_id == int(user_id), User.status == "active").first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or banned")
    return user


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
) -> User | None:
    if settings.DEBUG:
        # Trong dev mode: không bắt buộc user (public endpoints)
        if not credentials:
            return None
        return get_current_user(credentials, db)
    if not credentials:
        return None
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None


def require_role(*roles: str):
    def _checker(current_user: User = Depends(get_current_user)) -> User:
        # ── DEV BYPASS: bỏ qua kiểm tra role ───────────────────────────────
        if settings.DEBUG:
            return current_user
        # ── PRODUCTION ──────────────────────────────────────────────────────
        user_roles = {ur.role.role_name for ur in current_user.user_roles if ur.status == "active"}
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(roles)}",
            )
        return current_user
    return _checker


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    # ── DEV BYPASS ──────────────────────────────────────────────────────────
    if settings.DEBUG:
        return current_user
    # ── PRODUCTION ──────────────────────────────────────────────────────────
    user_roles = {ur.role.role_name for ur in current_user.user_roles if ur.status == "active"}
    if "admin" not in user_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def require_shop_owner(current_user: User = Depends(get_current_user)) -> User:
    # ── DEV BYPASS ──────────────────────────────────────────────────────────
    if settings.DEBUG:
        return current_user
    # ── PRODUCTION ──────────────────────────────────────────────────────────
    user_roles = {ur.role.role_name for ur in current_user.user_roles if ur.status == "active"}
    if "shop" not in user_roles and "admin" not in user_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Shop owner access required")
    return current_user


def require_shipper(current_user: User = Depends(get_current_user)) -> User:
    # ── DEV BYPASS ──────────────────────────────────────────────────────────
    if settings.DEBUG:
        return current_user
    # ── PRODUCTION ──────────────────────────────────────────────────────────
    user_roles = {ur.role.role_name for ur in current_user.user_roles if ur.status == "active"}
    if "shipper" not in user_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Shipper access required")
    return current_user
