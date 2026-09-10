let latitude = null;
let longitude = null;


function getLocation() {

    if (!navigator.geolocation) {

        alert(
            "Geolocation is not supported."
        );

        return;
    }

    navigator.geolocation.getCurrentPosition(

        function(position) {

            latitude =
                position.coords.latitude;

            longitude =
                position.coords.longitude;

            document.getElementById(
                "location"
            ).innerText =
                `📍 ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
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