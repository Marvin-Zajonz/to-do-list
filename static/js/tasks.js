import firebase from 'firebase/app';
import 'firebase/database';

// Initialize the Firebase app
const firebaseConfig = {
    apiKey: "AIzaSyDFLYAvjWBMdXAOTZi4FqL2KWFlPWeO6HY",
    authDomain: "to-do-list-386919.firebaseapp.com",
    projectId: "to-do-list-386919",
    storageBucket: "to-do-list-386919.appspot.com",
    messagingSenderId: "20275524707",
    appId: "1:20275524707:web:213ef37f4c97cb0d0eb456"
  };

firebase.initializeApp(firebaseConfig);

// Reference to the Firebase Realtime Database
const database = firebase.database();

// Function to add a new task
function addTask(task) {
  // Generate a new unique key for the task
  const newTaskRef = database.ref('tasks').push();

  // Set the task data under the generated key
  newTaskRef.set(task);
}

// Function to update a task
function updateTask(taskId, updates) {
  const taskRef = database.ref(`tasks/${taskId}`);
  taskRef.update(updates);
}

// Function to delete a task
function deleteTask(taskId) {
  const taskRef = database.ref(`tasks/${taskId}`);
  taskRef.remove();
}

// Function to listen for real-time updates on tasks
function listenForTaskUpdates(callback) {
  const tasksRef = database.ref('tasks');
  tasksRef.on('value', (snapshot) => {
    const tasks = snapshot.val();
    callback(tasks);
  });
}

export { addTask, updateTask, deleteTask, listenForTaskUpdates };
