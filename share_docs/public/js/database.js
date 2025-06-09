import { auth, db, storage } from './main.js';
import { ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-storage.js";
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-firestore.js";

export async function uploadDocument() {
    const fileInput = document.getElementById('docFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file first');
        return;
    }

    try {
        // Create a unique filename using timestamp
        const timestamp = new Date().getTime();
        const fileName = `${timestamp}_${file.name}`;
        const storageRef = ref(storage, `documents/${fileName}`);

        // Upload file to Firebase Storage
        const snapshot = await uploadBytes(storageRef, file);
        const downloadURL = await getDownloadURL(snapshot.ref);

        // Store file metadata in Firestore
        await addDoc(collection(db, 'documents'), {
            fileName: file.name,
            storagePath: `documents/${fileName}`,
            downloadURL,
            uploadedAt: serverTimestamp(),
            uploadedBy: auth.currentUser?.uid || 'anonymous'
        });

        alert('Document uploaded successfully!');
    } catch (error) {
        console.error('Upload failed:', error);
        alert(`Upload failed: ${error.message}`);
    }
}

export async function shareDocument() {
    const shareToInput = document.getElementById('shareTo');
    const recipient = shareToInput.value;

    if (!recipient) {
        alert('Please enter an Aadhaar number or email');
        return;
    }

    try {
        await addDoc(collection(db, 'shares'), {
            recipient,
            sharedBy: auth.currentUser?.uid || 'anonymous',
            sharedAt: serverTimestamp()
        });
        alert('Document shared successfully!');
    } catch (error) {
        console.error('Sharing failed:', error);
        alert(`Sharing failed: ${error.message}`);
    }
}
