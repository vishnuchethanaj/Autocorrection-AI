/* =========================================================
   AI-Powered Autocorrect Tool — Frontend Script
   Communicates with Flask backend via REST (POST /correct)
   ========================================================= */

const API_URL = "/correct"; // Same-origin Flask endpoint

const inputText   = document.getElementById("inputText");
const charCounter = document.getElementById("charCounter");
const correctBtn  = document.getElementById("correctBtn");
const clearBtn    = document.getElementById("clearBtn");
const loading     = document.getElementById("loading");
const errorBox    = document.getElementById("errorBox");
const resultSec   = document.getElementById("resultSection");
const originalEl  = document.getElementById("originalText");
const correctedEl = document.getElementById("correctedText");
const copyBtn     = document.getElementById("copyBtn");
const copyMsg     = document.getElementById("copyMsg");

const MAX = 5000;

/* ---------- Character counter ---------- */
function updateCounter() {
  const len = inputText.value.length;
  charCounter.textContent = `${len} / ${MAX} characters`;
}
inputText.addEventListener("input", updateCounter);
updateCounter();

/* ---------- Clear ---------- */
clearBtn.addEventListener("click", () => {
  inputText.value = "";
  updateCounter();
  resultSec.classList.add("hidden");
  errorBox.classList.add("hidden");
  inputText.focus();
});

/* ---------- Correct ---------- */
correctBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  errorBox.classList.add("hidden");
  resultSec.classList.add("hidden");

  if (!text) {
    inputText.focus();
    return;
  }

  setLoading(true);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();

    originalEl.textContent  = data.original ?? text;
    correctedEl.textContent = data.corrected ?? "";

    resultSec.classList.remove("hidden");
    resultSec.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    console.error(err);
    errorBox.classList.remove("hidden");
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  correctBtn.disabled = isLoading;
  clearBtn.disabled   = isLoading;
  loading.classList.toggle("hidden", !isLoading);
  correctBtn.querySelector(".btn-label").textContent =
    isLoading ? "Correcting..." : "Correct Text";
}

/* ---------- Copy ---------- */
copyBtn.addEventListener("click", async () => {
  const text = correctedEl.textContent || "";
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    // Fallback
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }
  copyMsg.classList.remove("hidden");
  setTimeout(() => copyMsg.classList.add("hidden"), 1800);
});
