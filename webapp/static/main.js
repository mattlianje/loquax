async function translateText() {
    const text = document.getElementById("inputText").value;
    const with_scansion = document.getElementById("with_scansion").checked;
    const with_ipa = document.getElementById("with_ipa").checked;

    const response = await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, with_scansion: with_scansion, with_ipa: with_ipa }),
    });

    const data = await response.json();

    document.getElementById("outputText").value = data.translation;
}