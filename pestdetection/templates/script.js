
// Reset preview and hide progress bar
function resetPreview() {
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('videoPreview').style.display = 'none';
    document.getElementById('processMedia').style.display = 'none';
    document.getElementById('closePreviewBtn').style.display = 'none';
    document.getElementById('progressBarContainer').style.display = 'none';
    document.getElementById('progressText').innerText = '0% Processing...';
    document.getElementById('drop-area').style.display = 'block'; // Show drop area when reset
}

// Handle image selection
document.getElementById('selectImage').addEventListener('click', function () {
    resetPreview();

    let input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = function (event) {
        let file = event.target.files[0];
        if (file) {
            handleFileSelection(file);
            document.getElementById('drop-area').style.display = 'none'; // Hide drop area after file is selected
        }
    };
    input.click();
});

// Handle video selection
document.getElementById('selectVideo').addEventListener('click', function () {
    resetPreview();

    let input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/*';
    input.onchange = function (event) {
        let file = event.target.files[0];
        if (file) {
            handleFileSelection(file);
            document.getElementById('drop-area').style.display = 'none'; // Hide drop area after file is selected
        }
    };
    input.click();
});

// Close the preview (reset everything)
document.getElementById('closePreviewBtn').addEventListener('click', function () {
    resetPreview();
    window.selectedMedia = null;  // Clear the selected media
});

// Redirect to /start_stream for webcam streaming
document.getElementById('startStream').addEventListener('click', function () {
    window.location.href = "/start_stream";
});

// Process media (image/video)
document.getElementById('processMedia').addEventListener('click', function () {
    if (window.selectedMedia) {
        document.getElementById('progressBarContainer').style.display = 'block';
        let formData = new FormData();
        formData.append("file", window.selectedMedia);

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);

        // Track upload progress
        xhr.upload.addEventListener('progress', function (event) {
            if (event.lengthComputable) {
                let percentComplete = (event.loaded / event.total) * 100;
                let dashoffset = 283 - (283 * (percentComplete / 100));
                document.querySelector('.front').style.strokeDashoffset = dashoffset;
                document.getElementById('progressText').innerText = Math.round(percentComplete) + '% Processing...';
            }
        });

        xhr.onload = function () {
            if (xhr.status === 200) {
                let data = JSON.parse(xhr.responseText);
                if (data.output_file) {
                    document.getElementById('progressBarContainer').style.display = 'none';
                    let outputMedia;
                    let outputUrl = '/static/output/' + data.output_file;
                    if (data.output_file.endsWith('.mp4')) {
                        outputMedia = document.createElement('video');
                        outputMedia.controls = true;
                        const source = document.createElement('source');
                        source.src = outputUrl;
                        source.type = 'video/mp4';
                        outputMedia.appendChild(source);
                    } else {
                        outputMedia = document.createElement('img');
                        outputMedia.src = outputUrl;
                        outputMedia.width = 640;
                    }

                    document.getElementById('popupMedia').innerHTML = '';
                    document.getElementById('popupMedia').appendChild(outputMedia);
                    document.getElementById('downloadBtn').onclick = function () {
                        const a = document.createElement('a');
                        a.href = outputUrl;
                        a.download = data.output_file;
                        a.click();
                    };
                    document.getElementById('popupContainer').style.display = 'block';
                    document.getElementById('overlay').style.display = 'block';
                }
            }
        };

        xhr.send(formData);
    }
});

// Close popup
document.getElementById('closePopupBtn').addEventListener('click', function () {
    document.getElementById('popupContainer').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
});

// Handle drag and drop for file input
const dropArea = document.getElementById('drop-area');

// Prevent default behavior when file is dragged over the area
dropArea.addEventListener('dragover', function (event) {
    event.preventDefault();
    dropArea.classList.add('dragover');
});

// Remove dragover style when file is dragged out
dropArea.addEventListener('dragleave', function (event) {
    dropArea.classList.remove('dragover');
});

// Handle drop event
dropArea.addEventListener('drop', function (event) {
    event.preventDefault();
    dropArea.classList.remove('dragover');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        handleFileSelection(file);
        dropArea.style.display = 'none';  // Hide drop area after file is dropped
    }
});

// Handle file selection (both from drag-and-drop and file input)
function handleFileSelection(file) {
    let reader = new FileReader();
    reader.onload = function (e) {
        if (file.type.startsWith('image')) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
        } else if (file.type.startsWith('video')) {
            let video = document.getElementById('videoPreview');
            video.src = e.target.result;
            video.style.display = 'block';
        }
        document.getElementById('processMedia').style.display = 'inline-block';
        document.getElementById('closePreviewBtn').style.display = 'inline-block';
    };
    reader.readAsDataURL(file);
    window.selectedMedia = file;
    document.getElementById('mediaPreviewContainer').style.display = 'block';
}
