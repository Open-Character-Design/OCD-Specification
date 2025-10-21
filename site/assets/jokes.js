document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("why-ocd-quip");
    if (!el) return;
  
    const quips = [
      "Why learn something new? I have Notepad…",
      "Because your characters deserve more than a folder named *final_final_v3_reallythisone.json*.",
      "Because brilliant ideas deserve better than sticky notes and half-finished docs.",
      "Because a well-structured character file beats chaos in a thousand config.yaml(s).",
      "Because creativity shouldn’t get lost between concept art, dialogue scripts, and data schemas.",
      "Because even your characters need a little organization therapy."
    ];
  
    // Deterministic per-page (same quip for the same URL during one session)
    const key = location.pathname + (document.title || "");
    let seed = 0;
    for (let i = 0; i < key.length; i++) seed = (seed * 31 + key.charCodeAt(i)) >>> 0;
    const idx = seed % quips.length;
  
    el.innerHTML = quips[idx];
  });
  
  // Optional: “shuffle” on click
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-quip-shuffle]")) {
      const el = document.getElementById("why-ocd-quip");
      if (!el) return;
      const quips = Array.from(new Set(el.dataset.allQuips?.split("|") || []));
    }
  });
  