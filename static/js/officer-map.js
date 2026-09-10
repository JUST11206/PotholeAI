let map;

let allPotholes = [];

let markers = [];

let officerLocationMarker = null;


map =
    L.map("map").setView(
        [28.9845, 77.7064],
        12
    );


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);



async function loadPotholes() {

    try {

        const response =
            await fetch(
                "/officer/api/potholes"
            );

        allPotholes =
            await response.json();

        displayPotholes();

    } catch (error) {

        console.error(
            "Officer map error:",
            error
        );

    }
}



function displayPotholes() {

    markers.forEach(
        marker => {

            map.removeLayer(marker);

        }
    );

    markers = [];


    const priority =
        document.getElementById(
            "priority-filter"
        ).value;


    const status =
        document.getElementById(
            "status-filter"
        ).value;


    const filtered =
        allPotholes.filter(
            pothole => {

                const priorityMatch =
                    priority === "all" ||
                    String(
                        pothole.priority
                    ).toLowerCase() === priority;


                const statusMatch =
                    status === "all" ||
                    String(
                        pothole.status
                    ).toLowerCase() === status;


                return (
                    priorityMatch &&
                    statusMatch
                );

            }
        );


    document.getElementById(
        "visible-count"
    ).innerText = filtered.length;


    filtered.forEach(
        pothole => {

            addMarker(pothole);

        }
    );
}



function addMarker(pothole) {

    const marker =
        L.circleMarker(
            [
                pothole.latitude,
                pothole.longitude
            ],
            {
                radius: 9,

                fillColor:
                    getPriorityColor(
                        pothole.priority
                    ),

                color: "#ffffff",

                weight: 2,

                fillOpacity: 0.9
            }
        ).addTo(map);


    marker.bindPopup(`

        <div>

            <h3>
                🚧 Pothole #${pothole.id}
            </h3>

            <p>
                <b>Priority:</b>
                ${pothole.priority}
            </p>

            <p>
                <b>Severity:</b>
                ${pothole.severity}
            </p>

            <p>
                <b>Score:</b>
                ${pothole.priority_score}
            </p>

            <p>
                <b>Confidence:</b>
                ${(pothole.confidence * 100).toFixed(1)}%
            </p>

            <p>
                <b>Status:</b>
                ${pothole.status}
            </p>

            <p>
                👥 <b>Verifications:</b>
                ${pothole.verification_count}
            </p>

            <a
                href="/officer/pothole/${pothole.id}"
            >
                View Details →
            </a>

        </div>

    `);


    markers.push(marker);
}



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



function locateOfficer() {

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


            if (officerLocationMarker) {

                map.removeLayer(
                    officerLocationMarker
                );

            }


            officerLocationMarker =
                L.marker(
                    [
                        latitude,
                        longitude
                    ]
                )
                .addTo(map)
                .bindPopup(
                    "📍 Officer Location"
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



// Filters

document
    .getElementById("priority-filter")
    .addEventListener(
        "change",
        displayPotholes
    );


document
    .getElementById("status-filter")
    .addEventListener(
        "change",
        displayPotholes
    );



// Load potholes

loadPotholes();