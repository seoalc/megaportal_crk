from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.responses import RedirectResponse
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.database import async_session_maker
from app.material_users.models import Material_user
from app.utils.logging_config import logger
from app.material_users.schemas import SMaterialtouserAdd
from app.material_users.dao import MaterialuserDAO
from app.material_stocks.dao import MaterialstocksDAO  # Добавляем импорт


router = APIRouter(prefix='/materalusers', tags=['Auth'])

@router.post("/add/")
async def add_material_quantity_to_user(material: SMaterialtouserAdd) -> dict:
    logger.info(f"Добавление материала пользователю: {material}")
    
    async with async_session_maker() as session:
        try:
            async with session.begin():
                # 1. Проверяем наличие материала на складе
                stock = await MaterialstocksDAO.get_materials_quantity_by_id(material.material_title_id)
                if not stock or stock.quantity < material.quantity:
                    raise ValueError("Недостаточно материала на складе или материал отсутствует")

                # 2. Добавляем материал пользователю
                new_material_title = await MaterialuserDAO.add_material_to_user(
                    material_title_id=material.material_title_id,
                    user_id=material.user_id,
                    quantity=material.quantity
                )

                # 3. Уменьшаем количество на складе
                await MaterialstocksDAO.decrease_quantity(
                    material_title_id=material.material_title_id,
                    quantity=material.quantity
                )

                await session.commit()  # Фиксируем изменения

            return {
                "message": "Материал успешно выдан пользователю и обновлён на складе!",
                "material_title": new_material_title.material_title_id,
                "quantity": new_material_title.quantity,
                "id": new_material_title.id,
                "ok": True
            }
        except ValueError as e:
            await session.rollback()
            logger.warning(f"Ошибка: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            await session.rollback()
            logger.error(f"Неизвестная ошибка: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка при выдаче материала: {str(e)}")

@router.get("/materials")
async def get_materials():
    return {"message": "Materials endpoint"}