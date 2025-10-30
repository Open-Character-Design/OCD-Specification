document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("why-ocd-quip");
    if (!el) return;
  
    const prefixes = [
      "Because",
      "Well...",
      "Maybe",
      "Perhaps",
      "We believe",
      "Let's face it,",
      "Studies show",
      "Unpopular opinion:",
    ];
    const quips = [
      "chaotic mess works better as a character backstory.",
      "chaotic is a great character trait, not so much a workflow.",
      "chaos makes great stories, not great pipelines.",
      "a well-structured character file beats chaos in a thousand txts.",
      "brilliant ideas deserve better than half-finished docs.",
      "clarity beats caffeine.",
      "consistency is sexier than improv continuity.",
      "consistency shouldn't be a plot twist.",
      "creativity thrives when the docs aren't on fire.",
      "creativity's fun. file management isn't. ocd fixes that.",
      "even imagination needs documentation.",
      "even your characters need a little organization therapy.",
      "final_v12_really_final.txt was a cry for help.",
      "ideas deserve better than your file naming conventions.",
      "notepad isn't version control.",
      "nothing kills flow like finding character_notes_v4_backup_old.",
      "order > panic saves.",
      "organization: the underrated art form.",
      "sticky notes don't scale.",
      "structure won't kill your vibe, just your chaos.",
      "world-building shouldn't feel like archaeology.",
      "you shouldn't need a lore historian to find your notes.",
      "your canon shouldn't be an improv.",
      "your characters deserve more than twelve slightly different google docs.",
      "your creativity called... it wants a folder structure.",
      "your lore shouldn't live in dms.",
      "someday you'll actually remember which 'final' is final.",
      "your world-building notes shouldn't look like a ransom letter."
    ];

  // Random per refresh
  const idx = Math.floor(Math.random() * quips.length);
  const prefixIdx = Math.floor(Math.random() * prefixes.length);
  el.textContent = prefixes[prefixIdx] + " " + quips[idx];
  });
