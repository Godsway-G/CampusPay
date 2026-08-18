const passwordField = document.querySelector("#password");

const eye = document.querySelector("#togglePassword");

if (passwordField && eye) {

    eye.addEventListener("click", () => {

        if (passwordField.type === "password") {

            passwordField.type = "text";

            eye.classList.replace(

                "bi-eye",

                "bi-eye-slash"

            );

        }

        else {

            passwordField.type = "password";

            eye.classList.replace(

                "bi-eye-slash",

                "bi-eye"

            );

        }

    });

}