if ("serviceWorker" in navigator) {

    window.addEventListener(
        "load",
        () => {

            navigator.serviceWorker.register(
                "/static/service-worker.js"
            )
            .then(() => {

                console.log(
                    "Service Worker registered"
                );

            })
            .catch(error => {

                console.error(
                    "Service Worker error:",
                    error
                );

            });

        }
    );
}