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

// Set up an authentication state observer
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in
    // You can perform actions for a signed-in user, such as redirecting to the dashboard
    console.log('User is signed in');
  } else {
    // User is signed out
    // You can perform actions for a signed-out user, such as redirecting to the login page
    console.log('User is signed out');
  }
});

