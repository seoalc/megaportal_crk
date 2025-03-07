from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import RedirectResponse
from app.users.auth import get_password_hash, authenticate_user, create_access_token
# from app.users.dependencies import get_current_user, get_current_admin_user
from app.materials_types.models import Material_type
from app.materials_types.schemas import SMaterialtypeAdd
from app.materials_types.dao import MaterialtypeDAO
from app.utils.logging_config import logger


router = APIRouter(prefix='/materialtypes', tags=['Auth'])

@router.post("/add/")
async def add_material_type(material: SMaterialtypeAdd) -> dict:
    logger.info(f"Тип материала: {material}")
    try:
        new_material_type = await MaterialtypeDAO.add_material_type(material_type=material.material_type)
        return {
            "message": "Новый тип материала успешно добавлен!",
            "material_type": new_material_type.material_type,
            "id": new_material_type.id,
            "ok": True
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Тип материала уже существует")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при добавлении типа материала: {str(e)}")