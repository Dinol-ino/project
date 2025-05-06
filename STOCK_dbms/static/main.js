async function fetchPortfolio() {
    const userId = document.getElementById("userId").value.trim();
    console.log("User ID entered:", userId);

    const spinner = document.getElementById("loadingSpinner");
    const table = document.getElementById("portfolioTable");

    // Clear table before new fetch
    table.innerHTML = "";
    spinner.style.display = "block"; // Show loading spinner

    // Validate user ID
    if (!userId || isNaN(userId) || userId.length === 0) {
        alert("Please enter a valid User ID.");
        spinner.style.display = "none";
        return;
    }

    try {
        // Fetch portfolio data from backend
        const res = await fetch(`/portfolio/${userId}`);
        console.log("Response status:", res.status);

        // Check if response is okay
        if (!res.ok) {
            const errorText = await res.text();
            console.error("Server Error:", errorText);
            alert(`Error ${res.status}: ${errorText}`);
            throw new Error(`Error ${res.status}: ${errorText}`);
        }

        // Parse the response data
        const data = await res.json();
        console.log("Data received:", data);

        // Check if no data was returned
        if (!data || data.portfolio_data.length === 0) {
            table.innerHTML = `<tr><td colspan="6">No data found for User ID ${userId}</td></tr>`;
        } else {
            // Create a document fragment to hold the table rows
            const fragment = document.createDocumentFragment();

            // Create the header row
            const headerRow = document.createElement("tr");
            headerRow.innerHTML = `
                <th>Portfolio</th>
                <th>Symbol</th>
                <th>Qty</th>
                <th>Buy Price</th>
                <th>Current Price</th>
                <th>P/L</th>
            `;
            fragment.appendChild(headerRow);

            // Loop through the portfolio data and create table rows
            data.portfolio_data.forEach(row => {
                console.log("Row data:", row);

                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${row.portfolio_name || "N/A"}</td>
                    <td>${row.symbol || "N/A"}</td>
                    <td>${row.quantity || "N/A"}</td>
                    <td>${row.avg_buy_price || "N/A"}</td>
                    <td>${row.current_price || "N/A"}</td>
                    <td>${row.profit_loss || "N/A"}</td>
                `;
                fragment.appendChild(tr);
            });

            // Append the rows to the table
            table.appendChild(fragment);

            // Update portfolio summary
            const summary = document.getElementById("portfolioSummary");
            summary.innerHTML = `
                <strong>Total Investment: </strong> ${data.total_investment}<br>
                <strong>Total Value: </strong> ${data.total_value}<br>
                <strong>Total P/L: </strong> ${data.total_profit_loss}
            `;
        }
    } catch (error) {
        console.error("Error fetching portfolio:", error);
        alert("Error fetching portfolio. Please try again.");
    } finally {
        spinner.style.display = "none"; // Hide spinner after request is complete
    }
}
