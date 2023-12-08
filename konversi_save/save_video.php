<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['video'])) {
    $video = $_FILES['video'];

    // Simpan video ke folder yang diinginkan (contoh menyimpan dalam folder "hasil")
    $targetDir = '../hasil/';
    $targetFile = $targetDir . basename($video['name']);

    if (move_uploaded_file($video['tmp_name'], $targetFile)) {
        $response = array('message' => 'Video berhasil disimpan.');
    } else {
        $response = array('message' => 'Gagal menyimpan video.');
    }

    echo json_encode($response);
}
?>
