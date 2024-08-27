document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector(".login-container form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const formData = new FormData(loginForm);

            fetch("/login", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/dashboard";
                } else {
                    const loginMessage = document.getElementById("login-message");
                    if (loginMessage) {
                        loginMessage.textContent = data.error;
                    }
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.querySelector(".signup-container form");

    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const formData = new FormData(signupForm);

            fetch("/signup", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/login";
                } else {
                    const signupMessage = document.getElementById("signup-message");
                    if (signupMessage) {
                        signupMessage.textContent = data.error;
                    }
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const contractLinks = document.querySelectorAll(".contract-link");

    if (contractLinks) {
        contractLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault();
                const contractType = this.getAttribute("href").split("=")[1];

                fetch(`/create_contract?type=${contractType}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Optionally, display the contract details or provide a download link
                            alert("Contract created successfully!");
                        } else {
                            alert("Failed to create contract: " + data.error);
                        }
                    })
                    .catch(error => console.error("Error:", error));
            });
        });
    }
});

