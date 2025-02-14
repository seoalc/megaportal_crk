document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("tbody");

    tableBody.addEventListener("click", async function (event) {
        // Назначение исполнителя
        if (event.target.classList.contains("assign_user")) {
            const row = event.target.closest("tr");
            const selectElement = row.querySelector(".user_select");
            // const selectedUserId = selectElement.value;
            const selectedUsers = [...row.querySelector(".user_select").selectedOptions].map(option => option.value);
            const applicationId = selectElement.dataset.applicationId;

            if (selectedUsers.length === 0) {
                alert("Выберите хотя бы одного исполнителя!");
                return;
            }

            try {
                const response = await fetch("/application/remedialuserupdate/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ 
                        application_id: applicationId, 
                        application_status: 1, 
                        remedial_user_ids: selectedUsers.map(Number) 
                    }),
                });

                if (!response.ok) {
                    throw new Error("Ошибка при назначении исполнителя");
                }

                window.location.reload();
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при назначении исполнителя");
            }
        }

        // Обновление текста жалобы
        if (event.target.classList.contains("change_complaint_text")) {
            const row = event.target.closest("tr");
            const complaintTextArea = row.querySelector(".complaint_text");
            const complaintText = complaintTextArea.value;
            const applicationId = complaintTextArea.dataset.applicationId;

            try {
                const response = await fetch("/application/complainttextupdate/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ 
                        application_id: applicationId, 
                        complaint_text: complaintText 
                    }),
                });

                if (!response.ok) {
                    throw new Error("Ошибка при обновлении текста");
                }

                window.location.reload();
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при обновлении текста");
            }
        }

        // Изменение даты явки
        if (event.target.classList.contains("change_appearance_date")) {
            const row = event.target.closest("tr");
            const appearanceDateInput = row.querySelector(".appearance_date");
            const appearanceDate = appearanceDateInput.value;
            const applicationId = appearanceDateInput.dataset.applicationId;

            try {
                const response = await fetch("/application/changeappearancedate/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ 
                        application_id: applicationId, 
                        appearance_date: appearanceDate 
                    }),
                });

                if (!response.ok) {
                    throw new Error("Ошибка при изменении даты");
                }
                
                window.location.reload();
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при изменении даты");
            }
        }

        // Удаление заявки
        if (event.target.classList.contains("delete_application_button")) {
            const row = event.target.closest("tr");
            const appearanceDateInput = row.querySelector(".appearance_date");
            const applicationId = appearanceDateInput.dataset.applicationId;

            const isConfirmed = window.confirm("Вы собираетесь удалить неназначенную заявку.\nПодтвердите действие.");

            if (!isConfirmed) {
                return; // Отмена удаления, если пользователь нажал "Отмена"
            }

            try {
                const response = await fetch("/application/deleteapplication/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ 
                        application_id: applicationId 
                    }),
                });

                if (!response.ok) {
                    throw new Error("Ошибка при удалении заявки");
                }
                
                window.location.reload();
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при удалении заявки");
            }
        }
    });
});

// document.addEventListener("DOMContentLoaded", function () {
//     const userIdForApplicationButton = document.querySelector("#user_id_for_application_button");
//     const selectElement = document.querySelector("#user_id_for_application");
//     const applicationIdElement = document.querySelector("#application_id");
//     const changeComplaintTextButton = document.querySelector("#change_complaint_text");
//     const complaintTextArea = document.querySelector("#complaint_text");

//     if (userIdForApplicationButton) {
//         userIdForApplicationButton.addEventListener("click", async function (event) {
//             const selectedUserId = selectElement.value;
//             const applicationId = applicationIdElement.value;
//             console.log(selectedUserId);

//             if (!selectedUserId || selectedUserId === "Выберите исполнителя") {
//                 alert("Выберите исполнителя!");
//                 return;
//             }

//             try {
//                 const response = await fetch("/application/remedialuserupdate/", {
//                     method: "POST",
//                     headers: {
//                         "Content-Type": "application/json",
//                     },
//                     body: JSON.stringify({ application_id: applicationId, application_status: 1, remedial_user_id: selectedUserId }),
//                 });

//                 if (!response.ok) {
//                     throw new Error("Ошибка при назначении исполнителя");
//                 }

//                 const data = await response.json();
//                 window.location.href = `/pages/unassigned_applications/`;
//             } catch (error) {
//                 console.error("Ошибка:", error);
//                 alert("Произошла ошибка при назначении исполнителя");
//             }
//         });
//     }

//     if (changeComplaintTextButton) {
//         changeComplaintTextButton.addEventListener("click", async function (event) {
//             const complaintText = complaintTextArea.value;
//             const applicationId = applicationIdElement.value;
            
//             try {
//                 const response = await fetch("/application/complainttextupdate/", {
//                     method: "POST",
//                     headers: {
//                         "Content-Type": "application/json",
//                     },
//                     body: JSON.stringify({ application_id: applicationId, complaint_text: complaintText }),
//                 });

//                 if (!response.ok) {
//                     throw new Error("Ошибка при обновлении текста");
//                 }

//                 const data = await response.json();
//                 window.location.href = `/pages/unassigned_applications/`;
//             } catch (error) {
//                 console.error("Ошибка:", error);
//                 alert("Произошла ошибка при обновлении текста");
//             }
//         });
//     }
// });