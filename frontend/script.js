const API_URL = "http://127.0.0.1:8001"

let selectedDecision = "buy";


// ------------------------------
// PAGE LOAD
// ------------------------------

document.addEventListener("DOMContentLoaded", () => {

    const token = localStorage.getItem("propertywise_token");

    if (token) {
        showApp();
    } else {
        showLogin();
    }


    // Login form
    const loginForm =
        document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", login);
    }


    // Property form
    const propertyForm =
        document.getElementById("propertyForm");

    if (propertyForm) {
        propertyForm.addEventListener(
            "submit",
            analyzeProperty
        );
    }


    // Decision cards
    const buyCard =
        document.getElementById("buyCard");

    const sellCard =
        document.getElementById("sellCard");

    if (buyCard) {
        buyCard.addEventListener("click", () => {
            selectDecision("buy");
        });
    }

    if (sellCard) {
        sellCard.addEventListener("click", () => {
            selectDecision("sell");
        });
    }


    // Logout
    const logoutButton =
        document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener(
            "click",
            logout
        );
    }

});


// ------------------------------
// LOGIN
// ------------------------------

async function login(event) {

    event.preventDefault();

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    const loginError =
        document.getElementById("loginError");

    loginError.textContent = "";


    try {

        /*
         * FastAPI OAuth2PasswordRequestForm
         * expects application/x-www-form-urlencoded
         * rather than JSON.
         */

        const formData =
            new URLSearchParams();

        formData.append(
            "username",
            username
        );

        formData.append(
            "password",
            password
        );


        const response = await fetch(
            `${API_URL}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },

                body: formData
            }
        );


        if (!response.ok) {

            const errorData =
                await response.json();

            throw new Error(
                errorData.detail ||
                "Login failed"
            );

        }


        const data =
            await response.json();


        // Store JWT
        localStorage.setItem(
            "propertywise_token",
            data.access_token
        );


        showApp();

    }

    catch (error) {

        loginError.textContent =
            error.message ||
            "Unable to connect to PropertyWise API.";

    }

}


// ------------------------------
// SHOW LOGIN
// ------------------------------

function showLogin() {

    const loginSection =
        document.getElementById(
            "loginSection"
        );

    const appSection =
        document.getElementById(
            "appSection"
        );

    loginSection.classList.remove(
        "hidden"
    );

    appSection.classList.add(
        "hidden"
    );

}


// ------------------------------
// SHOW APPLICATION
// ------------------------------

function showApp() {

    const loginSection =
        document.getElementById(
            "loginSection"
        );

    const appSection =
        document.getElementById(
            "appSection"
        );

    loginSection.classList.add(
        "hidden"
    );

    appSection.classList.remove(
        "hidden"
    );

}


// ------------------------------
// LOGOUT
// ------------------------------

function logout() {

    localStorage.removeItem(
        "propertywise_token"
    );

    showLogin();

}


// ------------------------------
// DECISION SELECTION
// ------------------------------

function selectDecision(decision) {

    selectedDecision =
        decision;

    const buyCard =
        document.getElementById(
            "buyCard"
        );

    const sellCard =
        document.getElementById(
            "sellCard"
        );


    if (decision === "buy") {

        buyCard.classList.add(
            "active"
        );

        sellCard.classList.remove(
            "active"
        );

    }

    else {

        sellCard.classList.add(
            "active"
        );

        buyCard.classList.remove(
            "active"
        );

    }

}


// ------------------------------
// PROPERTY ANALYSIS
// ------------------------------

async function analyzeProperty(event) {

    event.preventDefault();


    const price =
        Number(
            document.getElementById(
                "price"
            ).value
        );

    const size =
        Number(
            document.getElementById(
                "size"
            ).value
        );

    const age =
        Number(
            document.getElementById(
                "age"
            ).value
        );

    const rent =
        Number(
            document.getElementById(
                "rent"
            ).value
        );

    const location =
        document.getElementById(
            "location"
        ).value.trim();


    const loadingSection =
        document.getElementById(
            "loadingSection"
        );

    const resultSection =
        document.getElementById(
            "resultSection"
        );


    loadingSection.classList.remove(
        "hidden"
    );

    resultSection.classList.add(
        "hidden"
    );


    const token =
        localStorage.getItem(
            "propertywise_token"
        );


    try {

        const response =
            await fetch(
                `${API_URL}/analyze`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`

                    },

                    body: JSON.stringify({

                        decision:
                            selectedDecision,

                        price:
                            price,

                        size:
                            size,

                        age:
                            age,

                        rent:
                            rent,

                        location:
                            location

                    })

                }
            );


        // --------------------------
        // SESSION EXPIRED
        // --------------------------

        if (
            response.status === 401
        ) {

            localStorage.removeItem(
                "propertywise_token"
            );

            showLogin();

            throw new Error(
                "Your session has expired. Please sign in again."
            );

        }


        // --------------------------
        // API ERROR
        // --------------------------

        if (!response.ok) {

            const errorData =
                await response.json();

            throw new Error(
                errorData.detail ||
                "Property analysis failed."
            );

        }


        // --------------------------
        // SUCCESS
        // --------------------------

        const data =
            await response.json();

        displayResults(data);

    }

    catch (error) {

        alert(
            error.message ||
            "Unable to analyze the property."
        );

    }

    finally {

        loadingSection.classList.add(
            "hidden"
        );

    }

}


// ------------------------------
// DISPLAY RESULTS
// ------------------------------

function displayResults(data) {

    const resultSection =
        document.getElementById(
            "resultSection"
        );


    // --------------------------
    // BASIC RESULT
    // --------------------------

    document.getElementById(
        "score"
    ).textContent =
        data.score;


    document.getElementById(
        "recommendation"
    ).textContent =
        data.recommendation;


    document.getElementById(
        "resultLocation"
    ).textContent =
        data.location;


    document.getElementById(
        "rentalYield"
    ).textContent =
        data.rental_yield;


    document.getElementById(
        "resultDecision"
    ).textContent =
        selectedDecision.toUpperCase();


    // --------------------------
    // REASONS
    // --------------------------

    const reasonsList =
        document.getElementById(
            "reasonsList"
        );

    reasonsList.innerHTML = "";


    data.reasons.forEach(reason => {

        const li =
            document.createElement(
                "li"
            );

        li.textContent =
            reason;

        reasonsList.appendChild(
            li
        );

    });


    // --------------------------
    // RISKS
    // --------------------------

    const risksList =
        document.getElementById(
            "risksList"
        );

    risksList.innerHTML = "";


    data.risks.forEach(risk => {

        const li =
            document.createElement(
                "li"
            );

        li.textContent =
            risk;

        risksList.appendChild(
            li
        );

    });


    // --------------------------
    // GROQ EXPLANATION
    // --------------------------

    document.getElementById(
        "explanationText"
    ).textContent =
        data.explanation;


    /*
     * Optional ML/SHAP display.
     *
     * These elements are only updated if
     * they already exist in index.html.
     *
     * This keeps the current frontend
     * working while we add the new
     * customer-facing sections.
     */

    const mlScoreElement =
        document.getElementById(
            "mlScore"
        );

    if (mlScoreElement) {

        mlScoreElement.textContent =
            data.ml_score;

    }


    const shapList =
        document.getElementById(
            "shapList"
        );

    if (shapList) {

        shapList.innerHTML = "";


        data.shap_explanations.forEach(
            factor => {

                const li =
                    document.createElement(
                        "li"
                    );

                const contribution =
                    Number(
                        factor.contribution
                    );


                const sign =
                    contribution >= 0
                        ? "+"
                        : "";


                li.textContent =
                    `${factor.feature}: ${sign}${contribution}`;


                shapList.appendChild(
                    li
                );

            }
        );

    }


    // --------------------------
    // SHOW RESULT
    // --------------------------

    resultSection.classList.remove(
        "hidden"
    );


    resultSection.scrollIntoView({
        behavior: "smooth"
    });

}


// ------------------------------
// NEW ANALYSIS
// ------------------------------

function startNewAnalysis() {

    document.getElementById(
        "propertyForm"
    ).reset();


    document.getElementById(
        "resultSection"
    ).classList.add(
        "hidden"
    );


    document.getElementById(
        "buyCard"
    ).classList.add(
        "active"
    );


    document.getElementById(
        "sellCard"
    ).classList.remove(
        "active"
    );


    selectedDecision =
        "buy";


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}