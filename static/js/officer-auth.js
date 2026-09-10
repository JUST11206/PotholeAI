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


// OFFICER LOGIN
window.officerLogin = async function () {

    const email =
        document
            .getElementById("officer-email")
            .value
            .trim();

    const password =
        document
            .getElementById("officer-password")
            .value;


    if (!email || !password) {

        alert("Email and password are required.");

        return;
    }


    try {

        // Firebase login
        const userCredential =
            await signInWithEmailAndPassword(
                auth,
                email,
                password
            );


        // Get Firebase ID token
        const idToken =
            await userCredential.user.getIdToken();


        // Send token to Flask
        const response =
            await fetch(
                "/auth/officer/session",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        idToken: idToken
                    })
                }
            );


        const result =
            await response.json();


        if (result.success) {

            window.location.href =
                result.redirect;

        } else {

            alert(
                result.message ||
                "Officer login failed."
            );
        }


    } catch (error) {

        console.error(
            "Officer login error:",
            error
        );


        if (
            error.code ===
            "auth/invalid-credential"
        ) {

            alert(
                "Invalid officer email or password."
            );

        } else if (
            error.code ===
            "auth/user-not-found"
        ) {

            alert(
                "Officer account not found."
            );

        } else if (
            error.code ===
            "auth/wrong-password"
        ) {

            alert(
                "Incorrect password."
            );

        } else {

            alert(
                error.message ||
                "Officer login failed."
            );
        }
    }
};