chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {

    if (changeInfo.status === "complete" && tab.url) {

        // Ignore chrome internal pages
        if (tab.url.startsWith("chrome://") || tab.url.startsWith("edge://")) {
            return;
        }

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ url: tab.url })
        })
        .then(res => res.json())
        .then(data => {

            // Inject warning only if risky
            if (data.result.includes("Phishing") || data.result.includes("Suspicious")) {

                chrome.scripting.executeScript({
                    target: { tabId: tabId },
                    func: showWarning,
                    args: [data.result, data.risk_score]
                });

            }

        })
        .catch(() => {});
    }
});


// 🔥 Injected into page
function showWarning(result, risk) {

    // Prevent duplicate banners
    if (document.getElementById("phishing-warning")) return;

    let banner = document.createElement("div");

    banner.id = "phishing-warning";
    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.padding = "12px";
    banner.style.zIndex = "999999";
    banner.style.fontSize = "14px";
    banner.style.textAlign = "center";
    banner.style.fontFamily = "Arial";

    if (result.includes("Phishing")) {
        banner.style.background = "#dc2626";
    } else {
        banner.style.background = "#f59e0b";
    }

    banner.style.color = "white";

    banner.innerText = result + " | Risk Score: " + (risk * 100).toFixed(1) + "%";

    document.body.appendChild(banner);
}