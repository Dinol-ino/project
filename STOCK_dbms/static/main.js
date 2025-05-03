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
            const errorText = await res.text(); // ✅ Get full error response
            console.error("Server Error:", errorText);
            alert(`Error ${res.status}: ${errorText}`);
            throw new Error(`Error ${res.status}: ${errorText}`);
        }

        const data = await res.json();
        console.log("Data received:", data);

        if (!data || data.length === 0) {
            table.innerHTML = `<tr><td colspan="6">No data found for User ID ${userId}</td></tr>`;
        } else {
            // ✅ Optimized table rendering using `document.createElement()`
            const fragment = document.createDocumentFragment();
            
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

            data.forEach(row => {
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

            table.appendChild(fragment);
        }
    } catch (error) {
        console.error("Error fetching portfolio:", error);
        alert("Error fetching portfolio. Please try again.");
    } finally {
        spinner.style.display = "none"; // Hide loading spinner
    }
}