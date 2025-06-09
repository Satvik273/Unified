import { db } from './main.js';
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-firestore.js";

export async function logAction(userId, action, details) {
    await addDoc(collection(db, 'logs'), {
        userId,
        action,
        details,
        timestamp: serverTimestamp()
    });
}
