async function fetchPortfolio() {
    const userId = document.getElementById("userId").value.trim();
    console.log("User ID entered:", userId);

    const spinner = document.getElementById("loadingSpinner");
    const table = document.getElementById("portfolioTable");

    table.innerHTML = ""; // Clear table before new fetch
    spinner.style.display = "block"; // Show loading spinner

    if (!userId || isNaN(userId) || userId.length === 0) {
        alert("Please enter a valid User ID.");
        spinner.style.display = "none";
        return;
    }

    try {
        const res = await fetch(`/portfolio/${userId}`);
        console.log("Response status:", res.status);

        if (!res.ok) {
            if (res.status === 404) {
                alert(`No portfolio found for User ID ${userId}.`);
            } else {
                alert(`Error ${res.status}: Unable to fetch portfolio.`);
            }
            throw new Error(`Error ${res.status}: Server responded with an error.`);
        }
        const data = await res.json();
        console.log("Data received:", data);

        if (data.length === 0) {
            table.innerHTML = `<tr><td colspan="6">No data found for User ID ${userId}</td></tr>`;
        } else {
            table.innerHTML = `
                <tr>
                    <th>Portfolio</th>
                    <th>Symbol</th>
                    <th>Qty</th>
                    <th>Buy Price</th>
                    <th>Current Price</th>
                    <th>P/L</th>
                </tr>
            `;
            data.forEach(row => {
                table.innerHTML += `
                    <tr>
                        <td>${row.portfolio_name}</td>
                        <td>${row.symbol}</td>
                        <td>${row.quantity}</td>
                        <td>${row.avg_buy_price}</td>
                        <td>${row.current_price}</td>
                        <td>${row.profit_loss}</td>
                    </tr>
                `;
            });
        }
    } catch (error) {
        console.error("Error fetching portfolio:", error);
        alert("Error fetching portfolio. Please try again.");
    } finally {
        spinner.style.display = "none"; // Hide loading spinner
    }
}