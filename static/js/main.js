// Navigation Interactions
const navbar = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.navbar-brand');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// Form Validation
const loginForm = document.querySelector('form');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        if (!username || !password) {
            e.preventDefault();
            alert('Please fill in all fields');
        }
    });
}

// Smooth Scrolling
const scrollLinks = document.querySelectorAll('a[href^="#"]');
scrollLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        target.scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Dynamic Content Loading
async function loadPatients() {
    const response = await fetch('/api/patients');
    const patients = await response.json();
    console.log(patients);
}

document.addEventListener('DOMContentLoaded', loadPatients);