import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-firestore.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-storage.js";

const firebaseConfig = {
  apiKey: "AIzaSyD_6oCCmAjNuAiuRFug6lgzaPQUOtD8_qs",
  authDomain: "govdocs-satvik2025.firebaseapp.com",
  projectId: "govdocs-satvik2025",
  storageBucket: "govdocs-satvik2025.appspot.com",
  messagingSenderId: "236750841574",
  appId: "1:236750841574:web:90c4172200f492afd07d27"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

export { auth, db, storage };

// OPTIONAL: Protect dashboard/profile pages
if (window.location.pathname.includes('dashboard.html') || window.location.pathname.includes('profile.html')) {
    onAuthStateChanged(auth, (user) => {
        if (!user) {
            // Not logged in → redirect to login page
            window.location.href = 'index.html';
        }
    });
}
