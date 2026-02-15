// Wait until the page fully loads
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully");

    // Simple client-side form validation
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const inputs = form.querySelectorAll("input[required]");
            let valid = true;

            inputs.forEach(function (input) {
                if (input.value.trim() === "") {
                    valid = false;
                    input.style.border = "1px solid red";
                } else {
                    input.style.border = "";
                }
            });

            if (!valid) {
                event.preventDefault();
                alert("Please fill in all required fields.");
            }
        });
    });
});
