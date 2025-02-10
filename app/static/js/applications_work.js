document.addEventListener("DOMContentLoaded", function () {
    const userIdForApplicationButton = document.querySelector("#user_id_for_application_button");
    const selectElement = document.querySelector("#user_id_for_application");

    if (userIdForApplicationButton) {
        userIdForApplicationButton.addEventListener("click", async function (event) {
            const selectedUserId = selectElement.value;
            console.log(selectedUserId);

            if (!selectedUserId || selectedUserId === "Выберите исполнителя") {
                alert("Выберите исполнителя!");
                return;
            }
        });
    }
});