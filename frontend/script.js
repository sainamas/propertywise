// ==============================
// PropertyWise Frontend
// Connected to FastAPI
// ==============================


// ------------------------------
// Backend API URL
// ------------------------------

const API_URL = "http://127.0.0.1:8000";


// ------------------------------
// Default decision
// ------------------------------

let selectedDecision = "buy";


// ------------------------------
// Select BUY or SELL
// ------------------------------

function selectDecision(decision) {

    selectedDecision = decision;

    const buyCard = document.getElementById("buyCard");
    const sellCard = document.getElementById("sellCard");

    if (decision === "buy") {

        buyCard.classList.add("active");
        sellCard.classList.remove("active");

    } else {

        sellCard.classList.add("active");
        buyCard.classList.remove("active");

    }
}


// ------------------------------
// Display list items
// ------------------------------

function displayList(elementId, items) {

    const element = document.getElementById(elementId);

    element.innerHTML = "";

    items.forEach(function (item) {

        const li = document.createElement("li");

        li.textContent = item;

        element.appendChild(li);

    });
}


// ------------------------------
// Submit property analysis
// ------------------------------

document
    .getElementById("propertyForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();


        // Read property data

        const propertyData = {

            decision: selectedDecision,

            price: Number(
                document.getElementById("price").value
            ),

            size: Number(
                document.getElementById("size").value
            ),

            age: Number(
                document.getElementById("age").value
            ),

            rent: Number(
                document.getElementById("rent").value
            ),

            location:
                document.getElementById("location").value.trim()

        };


        // Basic validation

        if (
            propertyData.price <= 0 ||
            propertyData.size <= 0 ||
            propertyData.age < 0 ||
            propertyData.rent < 0 ||
            propertyData.location === ""
        ) {

            alert("Please enter valid property details.");

            return;

        }


        // Show loading

        document
            .getElementById("loadingSection")
            .classList.remove("hidden");


        // Hide old result

        document
            .getElementById("resultSection")
            .classList.add("hidden");


        try {

            // --------------------------
            // Call FastAPI
            // --------------------------

            const response = await fetch(
                `${API_URL}/analyze`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(propertyData)
                }
            );


            // Check response

            if (!response.ok) {

                throw new Error(
                    `API request failed: ${response.status}`
                );

            }


            // Convert response to JSON

            const result = await response.json();


            // --------------------------
            // Display API response
            // --------------------------

            document.getElementById("score").textContent =
                result.score;


            document.getElementById("recommendation").textContent =
                result.recommendation;


            document.getElementById("analysisLocation").textContent =
                result.location;


            document.getElementById("rentalYield").textContent =
                `${result.rental_yield}%`;


            displayList(
                "reasonsList",
                result.reasons
            );


            displayList(
                "risksList",
                result.risks
            );


            document.getElementById("explanation").textContent =
                result.explanation;


            // Hide loading

            document
                .getElementById("loadingSection")
                .classList.add("hidden");


            // Show result

            document
                .getElementById("resultSection")
                .classList.remove("hidden");


            // Scroll to result

            document
                .getElementById("resultSection")
                .scrollIntoView({
                    behavior: "smooth"
                });

        }

        catch (error) {

            console.error(error);


            alert(
                "Unable to connect to the PropertyWise API. " +
                "Make sure the FastAPI server is running."
            );


            document
                .getElementById("loadingSection")
                .classList.add("hidden");

        }

    });


// ------------------------------
// Start new analysis
// ------------------------------

function startNewAnalysis() {

    document
        .getElementById("propertyForm")
        .reset();


    selectedDecision = "buy";


    document
        .getElementById("buyCard")
        .classList.add("active");


    document
        .getElementById("sellCard")
        .classList.remove("active");


    document
        .getElementById("resultSection")
        .classList.add("hidden");


    document
        .getElementById("loadingSection")
        .classList.add("hidden");


    document
        .getElementById("propertyForm")
        .scrollIntoView({
            behavior: "smooth"
        });

}


// ------------------------------
// Set BUY as default
// ------------------------------

document.addEventListener(
    "DOMContentLoaded",
    function () {

        selectDecision("buy");

    }
);