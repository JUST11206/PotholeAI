import {
    initializeApp
} from "https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js";

import {
    getAuth,
    signInWithEmailAndPassword
} from "https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js";

import {
    firebaseConfig
} from "./firebase-config.js";


const app = initializeApp(firebaseConfig);

const auth = getAuth(app);


// =========================
// LOGIN
// =========================

window.loginUser = async function () {

    const email =
        document.getElementById("email").value.trim();

    const password =
        document.getElementById("password").value;


    if (!email || !password) {

        alert("Enter email and password.");

        return;
    }


    try {

        // Firebase Login
        const userCredential =
            await signInWithEmailAndPassword(
                auth,
                email,
                password
            );


        const user =
            userCredential.user;


        // Get Firebase ID Token
        const idToken =
            await user.getIdToken();


        // Send token to Flask
        const response =
            await fetch("/auth/session", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    idToken: idToken
                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.message ||
                "Login failed."
            );

            return;
        }


        // Redirect based on role
        window.location.href =
            data.redirect;


    } catch (error) {

        console.error(
            "Login Error:",
            error
        );


        if (
            error.code ===
            "auth/invalid-credential"
        ) {

            alert(
                "Invalid email or password."
            );

        } else if (
            error.code ===
            "auth/user-not-found"
        ) {

            alert(
                "User does not exist."
            );

        } else if (
            error.code ===
            "auth/wrong-password"
        ) {

            alert(
                "Wrong password."
            );

        } else {

            alert(
                error.message ||
                "Login failed."
            );
        }
    }
};