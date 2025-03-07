from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from fastapi.responses import RedirectResponse
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.material_stocks.schemas import SMaterialstockAdd
from app.material_stocks.dao import MaterialstocksDAO
from app.utils.logging_config import logger


router = APIRouter(prefix='/materialsstock', tags=['Auth'])

@router.post("/add/")
async def add_material_quantity(material: SMaterialstockAdd) -> dict:
    logger.info(f"Количество материала: {material}")
    try:
        new_material_title = await MaterialstocksDAO.add_material_to_stock(
            material_title_id=material.material_title_id,  # ID типа материала
            quantity=material.quantity    # Наименование
        )
        return {
            "message": "Новое количество материала успешно добавлено!",
            "material_title": new_material_title.material_title_id,
            "quantity": new_material_title.quantity,  # Исправляем поле
            "id": new_material_title.id,
            "ok": True
        }
    except ValueError as e:
        logger.warning(f"Конфликт: {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Наименование материала уже существует")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка при добавлении количества материала: {str(e)}")

@router.get("/material_quantity_by_id")
async def get_material_quantity_by_id(material_title_id: int):
    rez = await MaterialstocksDAO.get_materials_quantity_by_id(material_title_id)
    if rez:
        logger.info(f"Данные по количеству: {rez.quantity}")
        return rez.quantity
    else:
        return 0