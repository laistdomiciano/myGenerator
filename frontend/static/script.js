document.addEventListener("DOMContentLoaded", function () {
    // Handle login form submission
    handleLoginForm();

    // Handle signup form submission
    handleSignupForm();

    // Handle contract link clicks
    handleContractLinks();
});

function handleLoginForm() {
    const loginForm = document.querySelector(".login-container form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(loginForm);

            fetch("/login", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/dashboard"; // Redirect to dashboard on successful login
                } else {
                    const loginMessage = document.getElementById("login-message");
                    if (loginMessage) {
                        loginMessage.textContent = data.error; // Display error message
                    }
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
}

function handleSignupForm() {
    const signupForm = document.querySelector(".signup-container form");

    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(signupForm);

            fetch("/signup", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/login"; // Redirect to login on successful signup
                } else {
                    const signupMessage = document.getElementById("signup-message");
                    if (signupMessage) {
                        signupMessage.textContent = data.error; // Display error message
                    }
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
}

function handleContractLinks() {
    const contractLinks = document.querySelectorAll(".contract-link");

    if (contractLinks) {
        contractLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault(); // Prevent the default link navigation

                const contractType = this.getAttribute("href").split("=")[1];

                fetch(`/create_contract?type=${contractType}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Contract created successfully!"); // Display success message
                            // Optionally, you can redirect the user or show a modal with contract details here
                        } else {
                            alert("Failed to create contract: " + data.error); // Display error message
                        }
                    })
                    .catch(error => console.error("Error:", error));
            });
        });
    }
}

