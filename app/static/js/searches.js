document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.querySelector("#main_search_form");

    if (searchForm) {
        searchForm.addEventListener("submit", async function (event) {
            event.preventDefault(); // Останавливаем стандартное поведение (перезагрузку страницы)
            console.log("Форма отправлена!");
            
            const formData = new FormData(searchForm);
            const data = Object.fromEntries(formData.entries());
            
            const searchNumber = data.subscriber_number;
            console.log("Данные с формы: ", searchNumber);
            const response = await fetch(`/searchnumber/searchnumber/${searchNumber}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const result = response.json();
            console.log("Ответ от сервера:", result);
            window.location.href = `/pages/searchnumber/${searchNumber}`;
            // try {
            //     const searchNumber = data.subscriber_number;
            //     console.log("Данные с формы: ", searchNumber);
            //     const response = await fetch(`/pages/searchnumber/${searchNumber}`, {
            //         method: 'GET',
            //         headers: {
            //             'Content-Type': 'application/json'
            //         }
            //     });
        
            //     // Проверяем успешность ответа
            //     if (!response.ok) {
            //         // Получаем данные об ошибке
            //         const errorData = await response.json();
            //         // displayErrors(errorData);  // Отображаем ошибки
            //         alert(errorData.message || 'Ошибка при обработке запроса');
            //         return;  // Прерываем выполнение функции
            //     }
        
            //     const result = await response.json();
            //     console.log("Ответ от сервера:", result);
        
            //     // if (result.message) {  // Проверяем наличие сообщения о успешной регистрации
            //     //     window.location.href = '/pages/searchnumber';  // Перенаправляем пользователя на страницу логина
            //     // } else {
            //     //     alert(result.message || 'Неизвестная ошибка');
            //     // }
            // } catch (error) {
            //     // console.error('Ошибка:', error);
            //     alert('Произошла ошибка при отправке формы. Пожалуйста, попробуйте снова.');
            // }
        });
    } else {
        console.error("Форма с id 'main_search_form' не найдена!");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const sendApplicationButton = document.querySelector("#send_application");

    if (sendApplicationButton) {
        sendApplicationButton.addEventListener("click", async function (event) {
            event.preventDefault(); // Останавливаем стандартное поведение (перезагрузку страницы)

            // Получаем форму и собираем данные из неё
            const form = document.getElementById('new-application-form');
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/application/add/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                console.log('Ответ сервера:', response)
        
                // Проверяем успешность ответа
                if (!response.ok) {
                    // Получаем данные об ошибке
                    const errorData = await response.json();
                    console.log(errorData);  // Отображаем ошибки
                    return;  // Прерываем выполнение функции
                }
        
                const result = await response.json();
        
                if (result.message) {  // Проверяем наличие сообщения о успешной регистрации
                    window.location.href = '/pages/searchnumber/' + data.subscriber_number;  // Перенаправляем пользователя на страницу логина
                } else {
                    alert(result.message || 'Неизвестная ошибка');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
            }
        });
    } else {
        console.error("Форма с id 'add_application' не найдена!");
    }


});

async function logoutFunction() {
    try {
        // Отправка POST-запроса для удаления куки на сервере
        let response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Проверка ответа сервера
        if (response.ok) {
            // Перенаправляем пользователя на страницу логина
            window.location.href = '/pages/login';
        } else {
            // Чтение возможного сообщения об ошибке от сервера
            const errorData = await response.json();
            console.error('Ошибка при выходе:', errorData.message || response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети', error);
    }
}