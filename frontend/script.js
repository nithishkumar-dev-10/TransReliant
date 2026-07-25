// Helper — apply color class based on label
function getLabelClass(label) {
  const l = label.toLowerCase();
  if (l.includes("high"))     return "label-high";
  if (l.includes("medium"))   return "label-medium";
  if (l.includes("on time"))  return "label-ontime";
  if (l.includes("slight"))   return "label-slight";
  if (l.includes("moderate")) return "label-moderate";
  if (l.includes("severe"))   return "label-severe";
  if (l.includes("low"))      return "label-low";
  return "";
}

// Main predict function
async function predict() {
  // Read form values
  const train_number         = parseInt(document.getElementById("train_number").value);
  const class_of_travel      = document.getElementById("class_of_travel").value;
  const source_station       = document.getElementById("source_station").value.trim().toUpperCase();
  const destination_station  = document.getElementById("destination_station").value.trim().toUpperCase();
  const date_of_journey      = document.getElementById("date_of_journey").value;
  const number_of_passengers = parseInt(document.getElementById("number_of_passengers").value);
  const waitlist_position    = parseFloat(document.getElementById("waitlist_position").value) || 0;

  // Basic validation
  if (!train_number || !class_of_travel || !source_station || !destination_station || !date_of_journey || !number_of_passengers) {
    showError("Please fill in all fields before submitting.");
    return;
  }

  // Update route line labels (cosmetic only — does not affect request)
  updateRouteLabels(source_station, destination_station);

  // Show loading
  showLoading(true);
  hideResults();
  hideError();

  // Build request body
  const body = {
    user: {
      train_number,
      source_station,
      destination_station,
      date_of_journey,
      class_of_travel,
      number_of_passengers,
      waitlist_position
    }
  };

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.detail || "Something went wrong. Please try again.");
      return;
    }

    // Render results
    renderResults(data);

  } catch (err) {
    showError("Could not connect to server. Make sure the backend is running.");
  } finally {
    showLoading(false);
  }
}

// Render all result cards
function renderResults(data) {
  const confProb  = data.ticket.confirmation_probability;
  const confLabel = data.ticket.confirmation_label;
  const delayTime = data.delay.delay_readable;
  const delayLabel= data.delay.delay_label;
  const relScore  = data.reliability.score;
  const relLabel  = data.reliability.label;

  // Confirmation card
  document.getElementById("conf-prob").textContent  = confProb + "%";
  const confLabelEl = document.getElementById("conf-label");
  confLabelEl.textContent  = confLabel;
  confLabelEl.className    = "card-label " + getLabelClass(confLabel);

  // Delay card
  document.getElementById("delay-time").textContent  = delayTime;
  const delayLabelEl = document.getElementById("delay-label");
  delayLabelEl.textContent = delayLabel;
  delayLabelEl.className   = "card-label " + getLabelClass(delayLabel);

  // Reliability card
  document.getElementById("rel-score").textContent  = relScore;
  const relLabelEl = document.getElementById("rel-label");
  relLabelEl.textContent   = relLabel;
  relLabelEl.className     = "card-label " + getLabelClass(relLabel);

  // Score bar
  const scoreBarEl = document.getElementById("score-bar");
  scoreBarEl.style.width    = relScore + "%";
  scoreBarEl.style.backgroundColor = getScoreColor(relScore); // cosmetic only
  document.getElementById("score-number").textContent = relScore + " / 100";

  // Show results
  document.getElementById("results").style.display = "block";
}

function showLoading(val) {
  document.getElementById("loading").style.display = val ? "flex" : "none";
}

function hideResults() {
  document.getElementById("results").style.display = "none";
}

function showError(msg) {
  const el = document.getElementById("error-msg");
  el.textContent = msg;
  el.style.display = "block";
}

function hideError() {
  document.getElementById("error-msg").style.display = "none";
}

// Cosmetic helper — maps score to a color for the reliability bar only.
// Does not affect the score value, label, or any request/response data.
function getScoreColor(score) {
  if (score >= 70) return "#1E8E5A";
  if (score >= 40) return "#E8A33D";
  return "#C23B3B";
}

// Cosmetic helper — updates the route-line station labels in the hero.
// Purely visual, does not affect prediction logic or API payload.
function updateRouteLabels(source, destination) {
  const fromEl = document.getElementById("route-from");
  const toEl   = document.getElementById("route-to");
  if (fromEl) fromEl.textContent = source || "SOURCE";
  if (toEl)   toEl.textContent   = destination || "DESTINATION";
}