import { auth } from './main.js';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-auth.js";

export async function register() {
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const otp = document.getElementById('otp').value;

    if (otp !== '123456') {
        alert('Invalid OTP');
        return;
    }

    try {
        await createUserWithEmailAndPassword(auth, email, password);
        alert('Registered successfully!');
        window.location.href = 'index.html';
    } catch (e) {
        alert(e.message);
    }
}

export async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        await signInWithEmailAndPassword(auth, email, password);
        alert('Logged in successfully!');
        window.location.href = 'dashboard.html';
    } catch (e) {
        alert(e.message);
    }
}
