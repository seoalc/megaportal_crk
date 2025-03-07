from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from fastapi.responses import RedirectResponse
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.materials_titles.schemas import SMaterialtitleAdd
from app.materials_titles.dao import MaterialtitleDAO
from app.utils.logging_config import logger


router = APIRouter(prefix='/materialstitles', tags=['Auth'])

@router.post("/add/")
async def add_material_type(material: SMaterialtitleAdd) -> dict:
    logger.info(f"Новый вид материала: {material}")
    try:
        new_material_title = await MaterialtitleDAO.add_material_title(
            material_type_id=material.material_type,  # ID типа материала
            material_title=material.material_title    # Наименование
        )
        return {
            "message": "Новое наименование материала успешно добавлено!",
            "material_title": new_material_title.material_title,
            "material_type_id": new_material_title.material_type_id,  # Исправляем поле
            "id": new_material_title.id,
            "ok": True
        }
    except ValueError as e:
        logger.warning(f"Конфликт: {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Наименование материала уже существует")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при добавлении наименования материала: {str(e)}")

@router.get("/material_titles_by_type")
async def get_material_titles_by_type(type_id: int = Query(...)):
    material_titles = await MaterialtitleDAO.get_materials_titles_by_type(material_type_id=type_id)
    return [{"id": material.id, "material_title": material.material_title} for material in material_titles]

