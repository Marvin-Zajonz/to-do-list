// auth.js

import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";

// Initialize Firebase Authentication
const auth = getAuth();

// User Registration
const registerUser = (email, password) => {
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      // Handle registration success
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // Handle registration error
    });
};

// User Login
const loginUser = (email, password) => {
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      // Handle login success
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // Handle login error
    });
};

// Track User Authentication State
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is logged in
    // Update UI or redirect to authenticated routes
  } else {
    // User is logged out
    // Update UI or redirect to login page
  }
});

// Export the functions to be used in other modules or scripts
export { registerUser, loginUser };
