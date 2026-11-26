const API_URL = "https://propertywise-et4z.onrender.com";

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


        const response =
            await fetch(
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


    if (data.risks && data.risks.length > 0) {

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

    }
    else {

        const li =
            document.createElement(
                "li"
            );

        li.textContent =
            "No specific risks identified.";

        risksList.appendChild(
            li
        );

    }


    // --------------------------
    // GROQ EXPLANATION
    // --------------------------

    const explanationElement =
        document.getElementById(
            "explanationText"
        );

    explanationElement.innerHTML =
        formatPropertyExplanation(
            data.explanation
        );


    // --------------------------
    // ML SCORE
    // --------------------------

    const mlScoreElement =
        document.getElementById(
            "mlScore"
        );

    if (mlScoreElement) {

        mlScoreElement.textContent =
            data.ml_score;

    }


    // --------------------------
    // SHAP EXPLANATIONS
    // --------------------------

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
// PROPERTY EXPLANATION FORMATTER
// ------------------------------

function formatPropertyExplanation(text) {

    if (!text) {
        return "";
    }


    // Normalize escaped line breaks
    // coming from the model response.
    let content =
        text
            .replace(/\\r\\n/g, "\n")
            .replace(/\\n/g, "\n")
            .replace(/\\+/g, "")
            .replace(/\r\n/g, "\n")
            .replace(/\r/g, "\n");


    // Escape HTML before adding our
    // own safe formatting.
    content =
        escapeHTML(content);


    const lines =
        content.split("\n");


    let html = "";
    let inBulletList = false;
    let inTable = false;
    let tableRows = [];


    function closeBulletList() {

        if (inBulletList) {
            html += "</ul>";
            inBulletList = false;
        }

    }


    function closeTable() {

        if (!inTable) {
            return;
        }


        if (tableRows.length > 0) {

            html += `
                <div class="property-table-wrapper">
                    <table class="property-table">
                        <tbody>
                            ${tableRows.join("")}
                        </tbody>
                    </table>
                </div>
            `;

        }


        tableRows = [];
        inTable = false;

    }


    for (let i = 0; i < lines.length; i++) {

        let line =
            lines[i].trim();


        // Empty line
        if (!line) {

            closeBulletList();
            closeTable();

            continue;

        }


        // Remove standalone Markdown
        // table separator rows.
        if (
            /^\|?\s*:?-+:?\s*\|/.test(line)
        ) {
            continue;
        }


        // Markdown table row
        if (
            line.includes("|")
        ) {

            const cells =
                line
                    .replace(/^\|/, "")
                    .replace(/\|$/, "")
                    .split("|")
                    .map(cell => cell.trim());


            if (
                cells.length >= 2
            ) {

                closeBulletList();

                if (!inTable) {
                    inTable = true;
                }


                const isHeader =
                    tableRows.length === 0;


                tableRows.push(`
                    <tr>
                        ${cells
                            .map(cell => {

                                const tag =
                                    isHeader
                                        ? "th"
                                        : "td";

                                return `
                                    <${tag}>
                                        ${formatInlineMarkdown(cell)}
                                    </${tag}>
                                `;

                            })
                            .join("")
                        }
                    </tr>
                `);

                continue;

            }

        }


        // Bullet point
        if (
            /^[-*]\s+/.test(line)
        ) {

            closeTable();

            if (!inBulletList) {

                html += "<ul>";
                inBulletList = true;

            }


            const bulletText =
                line.replace(
                    /^[-*]\s+/,
                    ""
                );


            html += `
                <li>
                    ${formatInlineMarkdown(
                        bulletText
                    )}
                </li>
            `;

            continue;

        }


        // Numbered list
        if (
            /^\d+\.\s+/.test(line)
        ) {

            closeTable();
            closeBulletList();

            html += `
                <div class="numbered-item">
                    ${formatInlineMarkdown(
                        line.replace(
                            /^\d+\.\s+/,
                            ""
                        )
                    )}
                </div>
            `;

            continue;

        }


        // Bold section heading
        const boldHeading =
            line.match(
                /^\*\*(.*?)\*\*\\?$/
            );


        if (boldHeading) {

            closeBulletList();
            closeTable();

            html += `
                <h4 class="explanation-heading">
                    ${formatInlineMarkdown(
                        boldHeading[1]
                    )}
                </h4>
            `;

            continue;

        }


        // Markdown heading
        const markdownHeading =
            line.match(
                /^#{1,4}\s+(.+)$/
            );


        if (markdownHeading) {

            closeBulletList();
            closeTable();

            html += `
                <h4 class="explanation-heading">
                    ${formatInlineMarkdown(
                        markdownHeading[1]
                    )}
                </h4>
            `;

            continue;

        }


        // Normal paragraph
        closeBulletList();
        closeTable();

        html += `
            <p class="explanation-paragraph">
                ${formatInlineMarkdown(line)}
            </p>
        `;

    }


    closeBulletList();
    closeTable();


    return html;

}


// ------------------------------
// INLINE MARKDOWN
// ------------------------------

function formatInlineMarkdown(text) {

    return text

        // Bold
        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        )

        // Inline code
        .replace(
            /`([^`]+)`/g,
            "<code>$1</code>"
        );

}


// ------------------------------
// HTML ESCAPING
// ------------------------------

function escapeHTML(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

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
