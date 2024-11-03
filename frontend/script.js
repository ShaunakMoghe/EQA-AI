// Function to get combined stock analysis summary
async function getCombinedSummary() {
    const symbol = document.getElementById("symbol").value.trim().toUpperCase();
    const sector = document.getElementById("sector").value.trim().toLowerCase();

    if (symbol === "" || sector === "") {
        document.getElementById("combined-result").innerHTML = `<p style="color: red;">Please enter both a valid stock symbol and sector.</p>`;
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/combined-summary?symbol=${symbol}&sector=${sector}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        const formattedSummary = data.user_friendly_summary.replace(/\n/g, '<br>');
        document.getElementById("combined-result").innerHTML = `
            <h2>Combined Analysis for: ${symbol}</h2>
            <h3>User-Friendly Summary:</h3>
            <p>${formattedSummary}</p>
            <h3>Final Score (1-10):</h3>
            <p>${data.final_score || 'N/A'}</p>
            <h3>Raw Data:</h3>
            <pre>${JSON.stringify(data.raw_data, null, 2)}</pre>
        `;
    } catch (error) {
        document.getElementById("combined-result").innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        console.error("Error fetching combined summary:", error);
    }
}

// Add event listener to button
document.querySelector("button").addEventListener("click", getCombinedSummary);
