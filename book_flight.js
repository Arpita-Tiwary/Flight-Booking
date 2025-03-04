// Event listener for the flight search form submission
document.getElementById("flight-search-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const departure = document.getElementById("departure").value;
    const destination = document.getElementById("destination").value;
    const flightDate = document.getElementById("flight-date").value;

    // Fetch flights from the backend
    fetch(`http://127.0.0.1:8085/api/flights?departure=${departure}&destination=${destination}&date=${flightDate}`)
        .then(response => {
            if (!response.ok) {
                console.error('Response Error:', response.status, response.statusText);
                return response.text().then(text => { throw new Error(text) });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }
            displayFlights(data);
        })
        .catch(error => {
            console.error(error);
            alert("Error fetching flights: " + error.message);
        });
});

// Function to display the fetched flight data
function displayFlights(flights) {
    const flightsList = document.getElementById("flights-list");
    flightsList.innerHTML = ""; // Clear previous results

    if (flights.length > 0) {
        flights.forEach(flight => {
            const flightDiv = document.createElement("div");
            flightDiv.classList.add("flight-item");

            // Format flight duration
            let formattedDuration = flight.flight_duration;
            if (formattedDuration && formattedDuration.includes(':')) {
                const [hours, minutes] = formattedDuration.split(':');
                formattedDuration = `${hours}h ${minutes}m`;
            }

            flightDiv.innerHTML = `
                <p><strong>Airline:</strong> ${flight.airline}</p>
                <p><strong>Departure:</strong> ${flight.departure}</p>
                <p><strong>Destination:</strong> ${flight.destination}</p>
                <p><strong>Flight Date:</strong> ${flight.flight_date}</p>
                <p><strong>Departure Time:</strong> ${flight.departure_time || 'N/A'}</p>
                <p><strong>Duration:</strong> ${formattedDuration || 'N/A'}</p>
                <p><strong>Price: ₹</strong> ${flight.price}</p>
                <button class="book-btn" data-flight-id="${flight.id}">Book Flight</button>
            `;
            flightsList.appendChild(flightDiv);
        });

        // Add booking button event listeners
        document.querySelectorAll(".book-btn").forEach(button => {
            button.addEventListener("click", function() {
                const flightId = this.getAttribute("data-flight-id");
                document.getElementById("selected-flight-id").value = flightId;
                document.getElementById("booking-form").style.display = "block";
            });
        });
    } else {
        flightsList.innerHTML = "<p>No flights found for the selected criteria.</p>";
    }
}

// Event listener for booking form submission
document.getElementById("booking-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const bookingData = {
        flightId: document.getElementById("selected-flight-id").value,
        name: document.getElementById("user-name").value,
        email: document.getElementById("user-email").value,
        contact: document.getElementById("user-contact").value
    };

    fetch("http://127.0.0.1:8085/api/book", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text) });
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            alert("Success: " + data.message);
            document.getElementById("booking-form").reset();
            document.getElementById("booking-form").style.display = "none";
        } else if (data.error) {
            alert("Booking Error: " + data.error);
        }
    })
    .catch(error => {
        console.error('Booking error:', error);
        alert("Error booking flight: " + error.message);
    });
});