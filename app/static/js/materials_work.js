document.addEventListener("DOMContentLoaded", function () {
    const sendMatButton = document.querySelector("#send_new_material_type");
    const sendMatTitleButton = document.querySelector("#send_new_material_title");
    const tableClosedByUser = document.querySelector("#closed_by_user-datatable");

    sendMatButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Останавливаем стандартное поведение (перезагрузку страницы)
        // Добавление нового типа материала
        const materialTypeInput = document.querySelector("#material_type_input");
        const materialTypeValue = materialTypeInput.value;
        
        try {
            const response = await fetch("/materialtypes/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    material_type: materialTypeValue 
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.detail); // Показываем сообщение ошибки (например, "Тип материала уже существует")
            } else {
                alert(data.message); // Показываем сообщение успеха
                window.location.reload();
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Произошла ошибка при добавлении");
        }
    });

    sendMatTitleButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Останавливаем стандартное поведение (перезагрузку страницы)
        // Добавление нового наименования материала
        const materialTypeSelect = document.querySelector("#material_title_select");
        const materialTypeValue = materialTypeSelect.value;
        const materialTitleInput = document.querySelector("#material_title_input");
        const materialTitleValue = materialTitleInput.value;
        
        try {
            const response = await fetch("/materialstitles/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    material_type: materialTypeValue,
                    material_title: materialTitleValue
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.detail); // Показываем сообщение ошибки (например, "Тип материала уже существует")
            } else {
                alert(data.message); // Показываем сообщение успеха
                window.location.reload();
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Произошла ошибка при добавлении");
        }
    });

    // подгрузка новых наименований материалов при выборе типа материала
    document.getElementById('material_type_to_stock').addEventListener('change', function() {
        const materialTypeId = this.value;
        const materialTitleSelect = document.getElementById('material_title_to_stock');

        if (materialTypeId) {
            // Очищаем предыдущие варианты
            materialTitleSelect.innerHTML = '<option value="">Загрузка...</option>';

            // Запрашиваем наименования материалов по выбранному типу
            fetch(`/materialstitles/material_titles_by_type?type_id=${materialTypeId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        materialTitleSelect.innerHTML = '<option value="">Выберите наименование</option>';
                        data.forEach(material => {
                            const option = document.createElement('option');
                            option.value = material.id;
                            option.textContent = material.material_title;
                            materialTitleSelect.appendChild(option);
                        });
                        materialTitleSelect.disabled = false;
                    } else {
                        materialTitleSelect.innerHTML = '<option value="">Нет доступных наименований</option>';
                    }
                })
                .catch(error => {
                    console.error('Ошибка при загрузке наименований:', error);
                    materialTitleSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
                });
        } else {
            materialTitleSelect.innerHTML = '<option value="">Сначала выберите тип материала</option>';
            materialTitleSelect.disabled = true;
        }
    });

    document.getElementById('send_quantity_material_to_stock').addEventListener("click", async function (event) {
        event.preventDefault(); // Останавливаем стандартное поведение (перезагрузку страницы)
        
        const materialTitleId = document.getElementById('material_title_to_stock').value;
        const quantity = parseInt(document.getElementById('quantity_to_stock').value, 10);

        if (!materialTitleId || !quantity) {
            alert('Заполните все поля!');
            return;
        }

        try {
            const response = await fetch("/materialsstock/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    material_title_id: materialTitleId,
                    quantity: quantity
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.detail); // Показываем сообщение ошибки (например, "Тип материала уже существует")
            } else {
                alert(data.message); // Показываем сообщение успеха
                window.location.reload();
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Произошла ошибка при добавлении");
        }
    });

    // подгрузка новых наименований материалов при выборе типа материала для выдачи пользователю
    document.getElementById('material_type_to_user').addEventListener('change', function() {
        const materialTypeId = this.value;
        const materialTitleSelect = document.getElementById('material_title_to_user');

        if (materialTypeId) {
            // Очищаем предыдущие варианты
            materialTitleSelect.innerHTML = '<option value="">Загрузка...</option>';

            // Запрашиваем наименования материалов по выбранному типу
            fetch(`/materialstitles/material_titles_by_type?type_id=${materialTypeId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        materialTitleSelect.innerHTML = '<option value="">Выберите наименование</option>';
                        data.forEach(material => {
                            const option = document.createElement('option');
                            option.value = material.id;
                            option.textContent = material.material_title;
                            materialTitleSelect.appendChild(option);
                        });
                        materialTitleSelect.disabled = false;
                    } else {
                        materialTitleSelect.innerHTML = '<option value="">Нет доступных наименований</option>';
                    }
                })
                .catch(error => {
                    console.error('Ошибка при загрузке наименований:', error);
                    materialTitleSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
                });
        } else {
            materialTitleSelect.innerHTML = '<option value="">Сначала выберите тип материала</option>';
            materialTitleSelect.disabled = true;
        }
    });

    // подгрузка инпута для ввода количества материала для выдачи пользователю
    document.getElementById('material_title_to_user').addEventListener('change', function() {
        const materialTitleId = this.value;
        const materialUserDiv = document.getElementById('material_user_div');
        
        // Запрашиваем наименования материалов по выбранному типу
        fetch(`/materialsstock/material_quantity_by_id?material_title_id=${materialTitleId}`)
        .then(response => response.json())
        .then(data => {
            if (data > 0) {
                let user_material_text = `<label class="col-md-12 col-form-label" for="quantity_to_user">Данного материала на скаде - ${data}. Укажите сколько хотите выдать</label>`;
                user_material_text += '<div class="col-md-12">';
                user_material_text += '<input type="text" class="form-control" id="quantity_to_user" name="quantity_to_stock" placeholder="Укажите количество...">';
                user_material_text += '</div>';
                user_material_text += '<div class="col-md-12">';
                user_material_text += '<br><button class="btn btn-success waves-effect waves-light" dir="ltr" data-style="expand-left" id="send_quantity_material_to_user">Выдать</button>';
                user_material_text += '</div>';
                materialUserDiv.innerHTML = user_material_text;

                document.getElementById('send_quantity_material_to_user').addEventListener("click", async function (event) {
                    event.preventDefault(); // Останавливаем стандартное поведение (перезагрузку страницы)
                    
                    const materialUserId = document.getElementById('material_user_id').value;
                    const materialTitleId = document.getElementById('material_title_to_user').value;
                    const quantity = parseInt(document.getElementById('quantity_to_user').value, 10);
            
                    if (!materialUserId || !materialTitleId || !quantity) {
                        alert('Заполните все поля!');
                        return;
                    }
            
                    try {
                        const response = await fetch("/materalusers/add/", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({ 
                                material_title_id: materialTitleId,
                                user_id: materialUserId,
                                quantity: quantity
                            }),
                        });
            
                        const data = await response.json();
            
                        if (!response.ok) {
                            alert(data.detail); // Показываем сообщение ошибки (например, "Тип материала уже существует")
                        } else {
                            alert(data.message); // Показываем сообщение успеха
                            window.location.reload();
                        }
                    } catch (error) {
                        console.error("Ошибка:", error);
                        alert("Произошла ошибка при добавлении");
                    }
                });
            } else {
                materialUserDiv.innerHTML = '<p>Данного материала нет на складе</p>';
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке количества:', error);
        });
    });

    tableClosedByUser.addEventListener("click", async function (event) {
        // Обновление текста жалобы
        if (event.target.classList.contains("write_of_material_from_user")) {
            alert(1);

            
        }
    });

    
});