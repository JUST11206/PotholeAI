const CACHE_NAME =
    "pothole-pwa-v1";


const FILES_TO_CACHE = [

    "/",

    "/static/css/style.css",

    "/static/js/app.js",

    "/static/js/camera.js",

    "/static/js/gps.js",

    "/static/manifest.json"

];


self.addEventListener(
    "install",
    event => {

        event.waitUntil(

            caches.open(
                CACHE_NAME
            ).then(
                cache => {

                    return cache.addAll(
                        FILES_TO_CACHE
                    );

                }
            )

        );

    }
);


self.addEventListener(
    "fetch",
    event => {

        event.respondWith(

            caches.match(
                event.request
            ).then(
                cachedResponse => {

                    return (
                        cachedResponse ||
                        fetch(event.request)
                    );

                }
            )

        );

    }
);