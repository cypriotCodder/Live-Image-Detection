document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-upload');
    const fileLabel = document.getElementById('file-label');
    const detectBtn = document.getElementById('detect-btn');
    const originalImage = document.getElementById('original-image');
    const resultImage = document.getElementById('result-image');
    const loading = document.getElementById('loading');
    const detectionsList = document.getElementById('detections-list');
    const detectionItems = document.getElementById('detection-items');

    let selectedFile = null;

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            selectedFile = e.target.files[0];
            fileLabel.textContent = selectedFile.name;
            detectBtn.disabled = false;

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                originalImage.src = e.target.result;
                originalImage.style.display = 'block';
                // Reset result
                resultImage.style.display = 'none';
                detectionsList.style.display = 'none';
            };
            reader.readAsDataURL(selectedFile);
        }
    });

    detectBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Show loading state
        detectBtn.disabled = true;
        loading.style.display = 'block';
        resultImage.style.display = 'none';
        detectionsList.style.display = 'none';

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('/detect', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Display result image
            resultImage.src = data.image;
            resultImage.style.display = 'block';

            // Display detections
            detectionItems.innerHTML = '';
            if (data.detections && data.detections.length > 0) {
                data.detections.forEach(det => {
                    const li = document.createElement('li');
                    li.className = 'detection-item';
                    li.innerHTML = `
                        <span class="detection-label">${det.label}</span>
                        <span class="detection-conf">${(det.confidence * 100).toFixed(1)}%</span>
                    `;
                    detectionItems.appendChild(li);
                });
                detectionsList.style.display = 'block';
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during detection.');
        } finally {
            loading.style.display = 'none';
            detectBtn.disabled = false;
        }
    });

    // Tab Switching
    const tabs = document.querySelectorAll('.tab-btn');
    const sections = document.querySelectorAll('.section');
    const videoFeed = document.getElementById('video-feed');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and sections
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => {
                s.style.display = 'none';
                s.classList.remove('active');
            });

            // Add active class to clicked tab
            tab.classList.add('active');

            // Show corresponding section
            const tabName = tab.getAttribute('data-tab');
            const targetSection = document.getElementById(`${tabName}-section`);
            targetSection.style.display = 'block';
            targetSection.classList.add('active');

            // Handle Camera Feed
            if (tabName === 'camera') {
                videoFeed.src = "/video_feed";
            } else {
                videoFeed.src = "";
            }
        });
    });
});
