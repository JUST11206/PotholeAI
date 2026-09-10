let capturedImage = null;

async function startCamera() {

    const video = document.getElementById("camera");

    try {

        const stream =
            await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: "environment"
                },
                audio: false
            });

        video.srcObject = stream;

    } catch (error) {

        alert(
            "Camera permission denied."
        );

        console.error(error);
    }
}


function captureImage() {

    const video =
        document.getElementById("camera");

    const canvas =
        document.getElementById("canvas");

    const preview =
        document.getElementById("preview");

    canvas.width =
        video.videoWidth;

    canvas.height =
        video.videoHeight;

    const context =
        canvas.getContext("2d");

    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    capturedImage = canvas.toDataURL(
        "image/jpeg"
    );

    preview.src = capturedImage;

    preview.style.display = "block";
}
async function submitReport() {

    if (!capturedImage) {

        alert(
            "Capture a pothole image first."
        );

        return;
    }

    if (
        latitude === null ||
        longitude === null
    ) {

        alert(
            "Get your GPS location first."
        );

        return;
    }

    const response =
        await fetch(
            "/api/pothole/report",
            {
                method: "POST",
                body: createFormData()
            }
        );

    const result =
        await response.json();

    if (result.success) {

        alert(
            `Pothole reported!\nPriority: ${result.priority}\nScore: ${result.priority_score}`
        );

    } else {

        alert(
            result.message
        );
    }
}


function createFormData() {

    const formData =
        new FormData();

    const blob =
        dataURLToBlob(capturedImage);

    formData.append(
        "image",
        blob,
        "pothole.jpg"
    );

    formData.append(
        "latitude",
        latitude
    );

    formData.append(
        "longitude",
        longitude
    );

    return formData;
}

//add this 
function dataURLToBlob(dataURL) {

    const parts =
        dataURL.split(",");

    const mime =
        parts[0]
            .match(/:(.*?);/)[1];

    const binary =
        atob(parts[1]);

    const array =
        new Uint8Array(
            binary.length
        );

    for (
        let i = 0;
        i < binary.length;
        i++
    ) {

        array[i] =
            binary.charCodeAt(i);
    }

    return new Blob(
        [array],
        {
            type: mime
        }
    );
}