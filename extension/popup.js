chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

    let url = tabs[0].url;

    document.getElementById("url").innerText = url;

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url})
    })
    .then(res => res.json())
    .then(data => {

        let phishing = data.confidence;
        let safe = 1 - phishing;

        let p = (phishing * 100).toFixed(2);
        let s = (safe * 100).toFixed(2);

        let result = document.getElementById("result");

        if (phishing >= 0.7) {
            result.innerText = "PHISHING (" + p + "%)";
            result.style.color = "red";
        }
        else if (phishing <= 0.3) {
            result.innerText = "SAFE (" + s + "%)";
            result.style.color = "green";
        }
        else {
            result.innerText = "SUSPICIOUS (" + p + "%)";
            result.style.color = "orange";
        }

    })
    .catch(() => {
        document.getElementById("result").innerText = "API ERROR";
    });

});