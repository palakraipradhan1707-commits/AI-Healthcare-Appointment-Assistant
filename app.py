import os
import pandas as pd

from flask import Flask, render_template, request, jsonify

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


# ============================================================
# 1. CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# 2. LOAD DOCTOR DATA
# ============================================================

try:
    doctors_df = pd.read_csv("doctors.csv")
except FileNotFoundError:
    raise FileNotFoundError(
        "doctors.csv was not found. "
        "Please place doctors.csv in the same folder as app.py."
    )


# ============================================================
# 3. CHECK GROQ API KEY
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("\nWARNING: GROQ_API_KEY is not set.")
    print("Please set your Groq API key before using the AI features.\n")


# ============================================================
# 4. CREATE AI MODEL
# ============================================================

if GROQ_API_KEY:

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

else:
    llm = None


# ============================================================
# 5. AI ROUTER PROMPT
# ============================================================

ROUTER_SYSTEM_PROMPT = """
You are an AI healthcare appointment routing assistant.

Your job is to classify the patient's problem into exactly ONE
of the following categories:

1. emergency
2. mental_health
3. general

EMERGENCY includes:
- chest pain
- severe bleeding
- difficulty breathing
- unconsciousness
- serious accidents
- heart attack symptoms
- severe urgent physical conditions

MENTAL_HEALTH includes:
- anxiety
- depression
- panic attacks
- suicidal thoughts
- self-harm
- severe emotional distress
- trauma-related problems

GENERAL includes:
- routine checkups
- mild fever
- cold
- headache
- minor aches
- common non-urgent problems
- follow-up appointments
- chronic but non-urgent conditions

Return ONLY ONE of these words:

emergency

mental_health

general
"""


# ============================================================
# 6. SAFETY KEYWORDS
# ============================================================

EMERGENCY_KEYWORDS = [
    "chest pain",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "severe bleeding",
    "unconscious",
    "heart attack",
    "major accident"
]


CRISIS_KEYWORDS = [
    "suicide",
    "kill myself",
    "self-harm",
    "want to die",
    "end my life"
]


# ============================================================
# 7. CLASSIFY PATIENT
# ============================================================

def classify_patient(age, query):

    query_lower = query.lower()

    # --------------------------------------------------------
    # Crisis safety check
    # --------------------------------------------------------

    if any(keyword in query_lower for keyword in CRISIS_KEYWORDS):

        return (
            "mental_health",
            "Crisis keyword detected — routed immediately for safety."
        )


    # --------------------------------------------------------
    # Emergency safety check
    # --------------------------------------------------------

    if any(keyword in query_lower for keyword in EMERGENCY_KEYWORDS):

        return (
            "emergency",
            "Emergency keyword detected — routed immediately for safety."
        )


    # --------------------------------------------------------
    # AI classification
    # --------------------------------------------------------

    if llm is None:

        return (
            "general",
            "AI model is unavailable. Defaulted to general ward."
        )


    try:

        response = llm.invoke([
            SystemMessage(
                content=ROUTER_SYSTEM_PROMPT
            ),

            HumanMessage(
                content=(
                    f"Patient age: {age}\n"
                    f"Patient symptoms: {query}"
                )
            )
        ])


        result = response.content.strip().lower()


        # ----------------------------------------------------
        # Identify AI response
        # ----------------------------------------------------

        if "emergency" in result:

            ward = "emergency"

        elif (
            "mental_health" in result
            or "mental health" in result
        ):

            ward = "mental_health"

        elif "general" in result:

            ward = "general"

        else:

            ward = "general"


        reasoning = (
            f"AI classified the patient's problem "
            f"as {ward}."
        )


        return ward, reasoning


    except Exception as error:

        print("AI ERROR:", error)

        return (
            "general",
            "AI classification failed. "
            "Defaulted to general ward."
        )


# ============================================================
# 8. FIND AVAILABLE DOCTOR
# ============================================================

def find_doctor(ward):

    global doctors_df


    # --------------------------------------------------------
    # Find active doctors belonging to the selected ward
    # --------------------------------------------------------

    available = doctors_df[
        (doctors_df["ward"] == ward)
        &
        (doctors_df["status"] == "active")
    ]


    # --------------------------------------------------------
    # No doctor available
    # --------------------------------------------------------

    if available.empty:

        return None


    # --------------------------------------------------------
    # Select first available doctor
    # --------------------------------------------------------

    doctor = available.iloc[0]


    doctor_name = doctor["doctor_name"]


    # --------------------------------------------------------
    # Mark doctor as busy
    # --------------------------------------------------------

    doctors_df.loc[
        doctors_df["doctor_name"] == doctor_name,
        "status"
    ] = "busy"


    # --------------------------------------------------------
    # Return doctor information
    # --------------------------------------------------------

    return {

        "doctor_name": doctor_name,

        "next_slot": str(
            doctor["next_slot"]
        ),

        "slot_minutes": int(
            doctor["slot_minutes"]
        ),

        "available": True
    }


# ============================================================
# 9. HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# 10. TRIAGE API
# ============================================================

@app.route(
    "/api/triage",
    methods=["POST"]
)
def triage():

    try:

        # ----------------------------------------------------
        # Get JSON data from frontend
        # ----------------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error": "No data received."

            }), 400


        # ----------------------------------------------------
        # Get patient information
        # ----------------------------------------------------

        name = str(
            data.get("name", "")
        ).strip()


        age = str(
            data.get("age", "")
        ).strip()


        query = str(
            data.get("query", "")
        ).strip()


        # ----------------------------------------------------
        # Validate input
        # ----------------------------------------------------

        if not name:

            return jsonify({

                "success": False,

                "error": "Please enter your name."

            }), 400


        if not age:

            return jsonify({

                "success": False,

                "error": "Please enter your age."

            }), 400


        if not query:

            return jsonify({

                "success": False,

                "error": "Please describe your problem."

            }), 400


        # ----------------------------------------------------
        # Classify patient
        # ----------------------------------------------------

        ward, reasoning = classify_patient(
            age,
            query
        )


        # ----------------------------------------------------
        # Find doctor
        # ----------------------------------------------------

        doctor = find_doctor(ward)


        # ----------------------------------------------------
        # Prepare response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "patient": {

                "name": name,

                "age": age,

                "symptoms": query

            },

            "triage": {

                "ward": ward,

                "reasoning": reasoning

            },

            "doctor": doctor

        })


    except Exception as error:

        print("SERVER ERROR:", error)


        return jsonify({

            "success": False,

            "error": "Something went wrong on the server."

        }), 500


# ============================================================
# 11. DOCTORS API
# ============================================================

@app.route("/api/doctors")
def get_doctors():

    try:

        return jsonify(
            doctors_df.to_dict(
                orient="records"
            )
        )

    except Exception as error:

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ============================================================
# 12. RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\n==========================================")
    print(" AI Healthcare Appointment Assistant")
    print("==========================================")
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("==========================================\n")


    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )