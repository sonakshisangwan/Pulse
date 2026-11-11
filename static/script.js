/**
 * Pulse - Student Quiz & Academic Performance System
 * Vanilla JavaScript for essential UI interactions and form validations
 */

document.addEventListener('DOMContentLoaded', function () {
    
    // 1. Flash message dismiss button
    const closeButtons = document.querySelectorAll('.close-flash');
    closeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const alertBox = this.closest('.flash-message');
            if (alertBox) {
                alertBox.style.display = 'none';
            }
        });
    });

    // 2. Quiz form submission verification
    const quizForm = document.getElementById('quizForm');
    if (quizForm) {
        quizForm.addEventListener('submit', function (event) {
            const questionCards = document.querySelectorAll('.question-card');
            const totalQuestions = questionCards.length;
            let answeredCount = 0;

            questionCards.forEach(function (card) {
                const inputs = card.querySelectorAll('input[type="radio"]');
                let isAnswered = false;
                inputs.forEach(function (radio) {
                    if (radio.checked) {
                        isAnswered = true;
                    }
                });
                if (isAnswered) {
                    answeredCount++;
                }
            });

            if (answeredCount < totalQuestions) {
                const confirmMsg = `You have answered ${answeredCount} out of ${totalQuestions} questions.\nDo you want to submit anyway?`;
                if (!confirm(confirmMsg)) {
                    event.preventDefault();
                }
            } else {
                if (!confirm('Are you sure you want to submit your quiz?')) {
                    event.preventDefault();
                }
            }
        });
    }

    // 3. Student Registration Password Check
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password');

            if (confirmPassword && password !== confirmPassword.value) {
                alert('Passwords do not match. Please re-enter your password.');
                event.preventDefault();
            }
        });
    }

    // 4. Admin Delete Question Confirmation
    const deleteButtons = document.querySelectorAll('.btn-delete-question');
    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this question? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
});
