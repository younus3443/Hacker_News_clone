document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("togglePassword");

    const password =
        document.getElementById("password") ||  
        document.getElementById("password1");  

    if (toggle && password) {
        toggle.addEventListener("change", function () {
            password.type = this.checked ? "text" : "password";
        });
    }
});
