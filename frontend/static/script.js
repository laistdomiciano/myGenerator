// frontend/static/js/scripts.js

document.addEventListener("DOMContentLoaded", function () {
    // Initialize Bootstrap tooltips if needed
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Handle form validations
    (function () {
        'use strict'
        var forms = document.querySelectorAll('.needs-validation')

        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
    })()

    // Handle contract generation
    handleContractGeneration()
})

function handleContractGeneration() {
    const contractItems = document.querySelectorAll('.dropdown-item[data-type]')
    const contractModal = new bootstrap.Modal(document.getElementById('contractModal'))
    const contractTypeName = document.getElementById('contractTypeName')
    const confirmGenerateBtn = document.getElementById('confirmGenerate')

    let selectedType = ''

    contractItems.forEach(item => {
        item.addEventListener('click', function (event) {
            event.preventDefault()
            selectedType = this.getAttribute('data-type')
            const typeText = this.textContent
            contractTypeName.textContent = typeText
            contractModal.show()
        })
    })

    confirmGenerateBtn.addEventListener('click', function () {
        if (selectedType) {
            generateContract(selectedType)
            contractModal.hide()
        }
    })
}

function generateContract(contractType) {
    const token = getToken()

    fetch(`${BACKEND_API_URL}/create_contract`, {  // Ensure BACKEND_API_URL is defined
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ type: contractType })  // Adjust based on backend requirements
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message or redirect
            alert("Contract created successfully! You can download it from your contracts section.")
            // Optionally, redirect to contracts page
        } else {
            alert("Failed to create contract: " + data.error)
        }
    })
    .catch(error => console.error("Error:", error))
}

function getToken() {
    return sessionStorage.getItem('access_token') || null
}
