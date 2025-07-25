let model;
// Update the model URL to use Django's static files URL
const MODEL_URL = '/static/myapp/models/15_motives_tfjs/model.json';
const IMAGE_SIZE = 224; // Sesuaikan dengan ukuran input model Anda (224x224)
const IMAGE_CHANNELS = 3; // RGB

const imageUpload = document.getElementById('imageUpload');
const imageCanvas = document.getElementById('imageCanvas');
const ctx = imageCanvas.getContext('2d');
const predictButton = document.getElementById('predictButton');
const predictionResult = document.getElementById('predictionResult');

// Fungsi untuk memuat model
async function loadModel() {
    try {
        predictionResult.innerText = "Memuat model, harap tunggu...";
        model = await tf.loadGraphModel(MODEL_URL);
        predictButton.disabled = false; // Aktifkan tombol setelah model dimuat
        predictionResult.innerText = "Model berhasil dimuat! Unggah gambar untuk prediksi.";
        console.log('Model berhasil dimuat:', model);
    } catch (error) {
        console.error('Gagal memuat model:', error);
        predictionResult.innerText = `Gagal memuat model: ${error.message}`;
    }
}

// Fungsi untuk pra-pemrosesan gambar untuk inferensi
async function preprocessImage(imageData) {
    let tensor = tf.browser.fromPixels(imageData); // Mengonversi data gambar menjadi tensor

    // 1. Ubah ukuran gambar ke target_size (224x224)
    tensor = tensor.resizeNearestNeighbor([IMAGE_SIZE, IMAGE_SIZE]);

    // 2. Konversi tipe data piksel ke float32
    // Model TensorFlow/Keras umumnya mengharapkan input float.
    tensor = tensor.toFloat();

    // 3. Normalisasi (PENTING BERDASARKAN PEMROSESAN ASLI ANDA)
    // Karena 'rescale=1./255' dikomentari di ImageDataGenerator Anda,
    // kita TIDAK akan melakukan normalisasi .div(tf.scalar(255)) di sini.
    // Ini berarti model Anda kemungkinan mengharapkan nilai piksel dalam rentang [0, 255]
    // atau memiliki lapisan normalisasi internal.

    // Jika Anda menggunakan model pre-trained (misalnya VGG, ResNet, MobileNet) yang dilatih di ImageNet,
    // mereka sering memiliki kebutuhan pra-pemrosesan yang sangat spesifik
    // (misalnya normalisasi ke [-1, 1] atau pengurangan mean/std dev).
    // Jika itu kasusnya, Anda harus mengimplementasikannya di sini.
    // Contoh untuk MobileNetV2 (normalisasi ke [-1, 1]):
    // tensor = tensor.div(tf.scalar(127.5)).sub(tf.scalar(1.0));
    // Contoh untuk VGG/ResNet (pengurangan mean per channel):
    // tensor = tf.sub(tensor, tf.tensor([123.68, 116.779, 103.939]));

    // Untuk saat ini, asumsikan model Anda dilatih dengan input [0, 255] float,
    // karena 'rescale=1./255' dikomentari.
    // Jika Anda TIDAK melakukan normalisasi 1/255 di Python, maka TIDAK lakukan di sini.

    // 4. Tambahkan dimensi batch.
    // Model mengharapkan input dalam bentuk batch (misal: [batch_size, height, width, channels]).
    // Untuk satu gambar, ini akan menjadi [1, 224, 224, 3].
    tensor = tensor.expandDims();

    return tensor
}

// Fungsi untuk melakukan prediksi
async function predict() {
    if (!model) {
        alert('Model belum dimuat. Mohon tunggu.');
        return;
    }

    const imgData = ctx.getImageData(0, 0, IMAGE_SIZE, IMAGE_SIZE); // Ambil data gambar dari canvas

    if (imgData.data.length === 0) {
        predictionResult.innerText = "Tidak ada gambar yang dimuat. Unggah gambar terlebih dahulu.";
        return;
    }

    predictionResult.innerText = "Melakukan prediksi...";
    predictButton.disabled = true; // Nonaktifkan tombol saat prediksi berlangsung

    try {
        // Pra-pemrosesan gambar
        const inputTensor = await preprocessImage(imgData);
        console.log('Input Tensor shape:', inputTensor.shape);

        // Lakukan prediksi
        const predictions = model.predict(inputTensor);

        // Ambil hasil prediksi
        // Asumsi model Anda mengeluarkan 15 nilai (untuk 15 motives)
        const predictionArray = await predictions.data();

        // Pasca-pemrosesan: Misalnya, temukan kelas dengan probabilitas tertinggi
        let maxProb = 0;
        let predictedClassIndex = -1;
        for (let i = 0; i < predictionArray.length; i++) {
            if (predictionArray[i] > maxProb) {
                maxProb = predictionArray[i];
                predictedClassIndex = i;
            }
        }

        // Cek apakah prediksi cukup yakin
        if (maxProb < 0.4) {
            predictionResult.innerHTML = `
                Batik tidak dikenali atau bukan batik!
            `;
            // Bersihkan tensor untuk menghemat memori
            inputTensor.dispose();
            predictions.dispose();
            return;
        }

        // Jika Anda memiliki label untuk 15 motives, Anda bisa memetakannya di sini.
        const motiveLabels = ['Batik Bali', 'Batik Betawi', 'Batik Cendrawasih', 'Batik Dayak', 'Batik Geblek Renteng', 'Batik Ikat Celup', 'Batik Insang', 'Batik Kawung', 'Batik Lasem', 'Batik Megamendung', 'Batik Pala', 'Batik Parang', 'Batik Poleng', 'Batik Sekar Jagad', 'Batik Tambal'];

        const predictedLabel = motiveLabels[predictedClassIndex];

        predictionResult.innerHTML = `
            Prediksi Selesai!<br>
            Motif Paling Dominan: ${predictedLabel} dengan Probabilitas ${maxProb.toFixed(4)}
        `;

        // Bersihkan tensor untuk menghemat memori
        inputTensor.dispose();
        predictions.dispose();

    } catch (error) {
        console.error('Gagal melakukan prediksi:', error);
        predictionResult.innerText = `Gagal melakukan prediksi: ${error.message}`;
    } finally {
        predictButton.disabled = false; // Aktifkan kembali tombol
    }
}

// Event listener untuk saat gambar diunggah
imageUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                // Gambar akan diskala agar sesuai dengan ukuran canvas
                ctx.clearRect(0, 0, imageCanvas.width, imageCanvas.height);
                ctx.drawImage(img, 0, 0, imageCanvas.width, imageCanvas.height);
                predictionResult.innerText = "Gambar siap. Klik 'Prediksi' untuk memulai.";
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        predictionResult.innerText = "Tidak ada gambar yang dipilih.";
    }
});


// Muat model saat halaman pertama kali dimuat
window.onload = loadModel;
