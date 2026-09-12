// ============================================================
// GET HTML ELEMENTS
// ============================================================

const form =
    document.getElementById("appointmentForm");


const loading =
    document.getElementById("loading");


const result =
    document.getElementById("result");


const errorMessage =
    document.getElementById("errorMessage");


const submitButton =
    document.getElementById("submitButton");


// ============================================================
// FORM SUBMISSION
// ============================================================

form.addEventListener(
    "submit",
    async function(event) {

        // ----------------------------------------------------
        // Stop normal form submission
        // ----------------------------------------------------

        event.preventDefault();


        // ----------------------------------------------------
        // Get values
        // ----------------------------------------------------

        const name =
            document.getElementById("name").value.trim();


        const age =
            document.getElementById("age").value.trim();


        const query =
            document.getElementById("query").value.trim();


        // ----------------------------------------------------
        // Basic validation
        // ----------------------------------------------------

        if (!name || !age || !query) {

            showError(
                "Please fill in all the fields."
            );

            return;

        }


        // ----------------------------------------------------
        // Show loading
        // ----------------------------------------------------

        loading.style.display = "block";

        result.style.display = "none";

        errorMessage.style.display = "none";

        submitButton.disabled = true;

        submitButton.textContent =
            "Processing...";


        // ----------------------------------------------------
        // Send request to Flask
        // ----------------------------------------------------

        try {

            const response = await fetch(
                "/api/triage",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        name: name,

                        age: age,

                        query: query

                    })

                }
            );


            // ------------------------------------------------
            // Convert response to JSON
            // ------------------------------------------------

            const data =
                await response.json();


            // ------------------------------------------------
            // Check success
            // ------------------------------------------------

            if (!data.success) {

                showError(
                    data.error ||
                    "Something went wrong."
                );

                return;

            }


            // ------------------------------------------------
            // Display patient information
            // ------------------------------------------------

            document.getElementById(
                "patientName"
            ).textContent =
                data.patient.name;


            document.getElementById(
                "patientAge"
            ).textContent =
                data.patient.age;


            // ------------------------------------------------
            // Display ward
            // ------------------------------------------------

            document.getElementById(
                "ward"
            ).textContent =
                formatWard(
                    data.triage.ward
                );


            // ------------------------------------------------
            // Display reasoning
            // ------------------------------------------------

            document.getElementById(
                "reason"
            ).textContent =
                data.triage.reasoning;


            // ------------------------------------------------
            // Display doctor information
            // ------------------------------------------------

            if (data.doctor) {

                document.getElementById(
                    "doctor"
                ).textContent =
                    data.doctor.doctor_name;


                document.getElementById(
                    "nextSlot"
                ).textContent =
                    data.doctor.next_slot;


                document.getElementById(
                    "slotMinutes"
                ).textContent =
                    data.doctor.slot_minutes +
                    " minutes";

            }

            else {

                document.getElementById(
                    "doctor"
                ).textContent =
                    "No doctor currently available";


                document.getElementById(
                    "nextSlot"
                ).textContent =
                    "Please wait in queue";


                document.getElementById(
                    "slotMinutes"
                ).textContent =
                    "-";

            }


            // ------------------------------------------------
            // Show result
            // ------------------------------------------------

            result.style.display = "block";


            // ------------------------------------------------
            // Scroll to result
            // ------------------------------------------------

            result.scrollIntoView({
                behavior: "smooth"
            });

        }


        catch (error) {

            console.error(
                "Error:",
                error
            );


            showError(
                "Unable to connect to the server. "
                + "Please make sure Flask is running."
            );

        }


        finally {

            // ------------------------------------------------
            // Hide loading
            // ------------------------------------------------

            loading.style.display = "none";


            // ------------------------------------------------
            // Enable button
            // ------------------------------------------------

            submitButton.disabled = false;

            submitButton.textContent =
                "Check Appointment";

        }

    }
);


// ============================================================
// FORMAT WARD NAME
// ============================================================

function formatWard(ward) {

    if (ward === "mental_health") {

        return "Mental Health";

    }


    if (ward === "emergency") {

        return "Emergency";

    }


    if (ward === "general") {

        return "General";

    }


    return ward;

}


// ============================================================
// SHOW ERROR
// ============================================================

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.style.display =
        "block";

    result.style.display =
        "none";

}
fetch("/api/triage", {