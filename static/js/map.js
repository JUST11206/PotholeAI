let map;
let userMarker;


// ==========================================
// INITIALIZE MAP
// ==========================================

function initMap() {

    map = L.map("pothole-map").setView(
        [28.9845, 77.7064],
        13
    );


    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);


    loadPotholes();
}


// ==========================================
// LOAD POTHOLES
// ==========================================

async function loadPotholes() {

    try {

        const response = await fetch(
            "/api/pothole/all"
        );


        const result =
            await response.json();


        if (!result.success) {

            console.error(
                "Unable to load potholes"
            );

            return;
        }


        result.potholes.forEach(
            pothole => {

                addPotholeMarker(
                    pothole
                );

            }
        );


        // Automatically show all potholes
        if (result.potholes.length > 0) {

            const bounds =
                result.potholes.map(
                    pothole => [
                        pothole.latitude,
                        pothole.longitude
                    ]
                );


            map.fitBounds(
                bounds,
                {
                    padding: [30, 30]
                }
            );
        }


    } catch (error) {

        console.error(
            "Map API error:",
            error
        );

    }
}


// ==========================================
// ADD POTHOLE MARKER
// ==========================================

function addPotholeMarker(pothole) {

    const color =
        pothole.status === "resolved"
            ? "#16a34a"
            : getPriorityColor(
                pothole.priority
            );


    const marker =
        L.circleMarker(
            [
                pothole.latitude,
                pothole.longitude
            ],
            {
                radius: 9,
                fillColor: color,
                color: "#ffffff",
                weight: 2,
                opacity: 1,
                fillOpacity: 0.9
            }
        );


    marker.addTo(map);


    marker.bindPopup(`

        <div class="pothole-popup">

            <h3>
                🚧 Pothole #${pothole.id}
            </h3>


            <p>
                <strong>Severity:</strong>
                ${pothole.severity || "N/A"}
            </p>


            <p>
                <strong>Priority:</strong>
                ${pothole.priority || "N/A"}
            </p>


            <p>
                <strong>Score:</strong>
                ${pothole.priority_score ?? "N/A"}
            </p>


            <p>
                <strong>Status:</strong>
                ${
                    pothole.status === "reported"
                        ? "🟠 Reported"
                        : pothole.status === "under_review"
                        ? "🟡 Under Review"
                        : pothole.status === "in_progress"
                        ? "🔵 Repair In Progress"
                        : pothole.status === "resolved"
                        ? "🟢 Resolved"
                        : "⚪ Unknown"
                }
            </p>


            <p>
                👥 <strong id="verification-count-${pothole.id}">
                    ${pothole.verification_count || 0}
                </strong>
                citizen verification(s)
            </p>


            ${
                pothole.description
                ?
                `<p>
                    <strong>AI:</strong><br>
                    ${pothole.description}
                </p>`
                :
                ""
            }


            ${
                pothole.status !== "resolved"
                ?
                `<button
                    type="button"
                    onclick="verifyPothole(${pothole.id})"
                    style="
                        width:100%;
                        padding:10px;
                        margin-top:10px;
                        border:none;
                        border-radius:8px;
                        cursor:pointer;
                    "
                >
                    ✅ I Verify This Pothole
                </button>`
                :
                `<p>
                    🟢 <strong>Road issue resolved</strong>
                </p>`
            }

        </div>

    `);
}


// ==========================================
// VERIFY POTHOLE
// ==========================================

async function verifyPothole(potholeId) {

    try {

        const response = await fetch(
            `/api/pothole/${potholeId}/verify`,
            {
                method: "POST"
            }
        );


        const result =
            await response.json();


        if (response.status === 401) {

            alert(
                "Please login to verify this pothole."
            );

            return;
        }


        if (result.already_verified) {

            alert(
                "You have already verified this pothole."
            );

            return;
        }


        if (result.success) {

            alert(
                "✅ Pothole verified successfully!"
                + "\n\n"
                + "Verifications: "
                + result.verification_count
                + "\n"
                + "Priority Score: "
                + result.priority_score
                + "\n"
                + "Priority: "
                + result.priority
            );


            const countElement =
                document.getElementById(
                    `verification-count-${potholeId}`
                );


            if (countElement) {

                countElement.innerText =
                    result.verification_count;

            }


            return;
        }


        alert(
            result.message ||
            "Unable to verify pothole."
        );


    } catch (error) {

        console.error(
            "Verification error:",
            error
        );


        alert(
            "Server error while verifying pothole."
        );
    }
}


// ==========================================
// PRIORITY COLOR
// ==========================================

function getPriorityColor(priority) {

    switch (
        String(priority).toLowerCase()
    ) {

        case "critical":
            return "#dc2626";

        case "high":
            return "#f97316";

        case "medium":
            return "#eab308";

        case "low":
            return "#22c55e";

        default:
            return "#6b7280";
    }
}


// ==========================================
// USER LOCATION
// ==========================================

function locateUser() {

    if (!navigator.geolocation) {

        alert(
            "Geolocation is not supported."
        );

        return;
    }


    navigator.geolocation.getCurrentPosition(

        function(position) {

            const latitude =
                position.coords.latitude;


            const longitude =
                position.coords.longitude;


            map.setView(
                [
                    latitude,
                    longitude
                ],
                16
            );


            if (userMarker) {

                map.removeLayer(
                    userMarker
                );

            }


            userMarker =
                L.marker(
                    [
                        latitude,
                        longitude
                    ]
                )
                .addTo(map)
                .bindPopup(
                    "📍 You are here"
                )
                .openPopup();

        },


        function(error) {

            console.error(error);


            alert(
                "Unable to get your location."
            );

        },


        {
            enableHighAccuracy: true,
            timeout: 10000
        }

    );
}


// ==========================================
// START
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        initMap();

    }
);