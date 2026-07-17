const startButton = document.getElementById("start-button");
const outputEl = document.getElementById("output");
const statusEl = document.getElementById("status");

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  statusEl.textContent = "Web Speech API not supported in this browser.";
  startButton.disabled = true;
} else {
  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-US";

  let isListening = false;
  let finalTranscript = "";

  startButton.addEventListener("click", () => {
    if (!isListening) {
      recognition.start();
    } else {
      recognition.stop();
    }
  });

  recognition.addEventListener("start", () => {
    isListening = true;
    startButton.textContent = "Stop Listening";
    statusEl.textContent = "Listening...";
  });

  recognition.addEventListener("end", () => {
    isListening = false;
    startButton.textContent = "Start Listening";
    statusEl.textContent = "Idle";
  });

  recognition.addEventListener("error", (e) => {
    statusEl.textContent = "Error: " + (e.error || "unknown");
    isListening = false;
    startButton.textContent = "Start Listening";
  });

  recognition.addEventListener("result", (event) => {
    let interim = "";
    finalTranscript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript + " ";
      } else {
        interim += transcript;
      }
    }
    outputEl.textContent = (finalTranscript + interim).trim();
  });
}
