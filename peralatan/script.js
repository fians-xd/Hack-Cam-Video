const videoElement = document.getElementById('video');

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        videoElement.srcObject = stream;
        const mediaRecorder = new MediaRecorder(stream);
        const recordedChunks = [];

        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = function() {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            recordedChunks.length = 0; // Bersihkan array chunks

            // Konversi video dari WebM ke MP4 menggunakan ffmpeg.wasm
            convertVideo(blob);
        };

        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000); // Berhenti merekam setelah 5 detik

        mediaRecorder.start();
    } catch (err) {
        console.error('Tidak dapat mengakses kamera:', err);
        alert('Mohon izinkan kamera untuk merekam video.');
    }
}

// Meminta izin kamera dari pengguna
navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(() => {
        // Pengguna memberikan izin
        startRecording();
    })
    .catch(err => {
        console.error('Tidak dapat mengakses kamera:', err);
        alert('Mohon izinkan kamera untuk merekam video.');
    });


async function convertVideo(inputBlob) {
    const formData = new FormData();
    formData.append('video', inputBlob, 'rekaman.webm');

    try {
        const saveResponse = await fetch('/konversi_save/save_video.php', {
            method: 'POST',
            body: formData,
        });

        if (!saveResponse.ok) {
            throw new Error('Gagal menyimpan video.');
        }

        const convertResponse = await fetch('/konversi_save/convert_video.php', {
            method: 'POST',
            body: formData,
        });

        const data = await convertResponse.json();
        alert(data.message); // Tampilkan pesan hasil dari server
    } catch (error) {
        console.error('Terjadi kesalahan:', error);
    }
}
