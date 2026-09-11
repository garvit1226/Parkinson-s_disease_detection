const form = document.getElementById("predictionForm");
const button = document.getElementById("predictBtn");
const result = document.getElementById("result");
const resultText = document.getElementById("resultText");
const confidenceText = document.getElementById("confidenceText");

const featureNames = [
    "MDVP:Fo(Hz)",
    "MDVP:Fhi(Hz)",
    "MDVP:Flo(Hz)",
    "MDVP:Jitter(%)",
    "MDVP:Jitter(Abs)",
    "MDVP:RAP",
    "MDVP:PPQ",
    "Jitter:DDP",
    "MDVP:Shimmer",
    "MDVP:Shimmer(dB)",
    "Shimmer:APQ3",
    "Shimmer:APQ5",
    "MDVP:APQ",
    "Shimmer:DDA",
    "NHR",
    "HNR",
    "RPDE",
    "DFA",
    "spread1",
    "spread2",
    "D2",
    "PPE"
];

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const values = featureNames.map(name => {
        const input = form.elements[name];
        return Number(input.value);
    });

    if (values.some(value => !Number.isFinite(value))) {
        alert("Please enter valid values for all 22 features.");
        return;
    }

    button.disabled = true;
    button.querySelector("span").textContent = "Predicting...";

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ features: values })
        });

        const data = await response.json();

        result.classList.remove("hidden");

        if (!data.success) {
            resultText.textContent = "Prediction unavailable";
            confidenceText.textContent = data.error || "Unknown error";
            return;
        }

        resultText.textContent = data.result;

        if (data.confidence !== null && data.confidence !== undefined) {
            confidenceText.textContent = `Model confidence: ${data.confidence}%`;
        } else {
            confidenceText.textContent = "Prediction generated successfully.";
        }

        result.scrollIntoView({ behavior: "smooth", block: "nearest" });

    } catch (error) {
        result.classList.remove("hidden");
        resultText.textContent = "Server error";
        confidenceText.textContent = error.message;
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent = "Run Prediction";
    }
});
