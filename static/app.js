// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const videoInput = document.getElementById('videoInput');
const uploadSection = document.getElementById('uploadSection');
const resultsSection = document.getElementById('resultsSection');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// State
let currentVideoId = null;

// Event Listeners
uploadArea.addEventListener('click', () => videoInput.click());
videoInput.addEventListener('change', handleFileSelect);
newAnalysisBtn.addEventListener('click', resetApp);

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#818cf8';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#6366f1';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#6366f1';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// File handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

async function handleFile(file) {
    // Validate file
    const validTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska', 'video/webm'];
    if (!validTypes.includes(file.type)) {
        alert('Invalid file type. Please upload a video file (MP4, AVI, MOV, MKV, WEBM)');
        return;
    }

    if (file.size > 100 * 1024 * 1024) {
        alert('File too large. Maximum size is 100MB');
        return;
    }

    // Show progress
    uploadArea.style.display = 'none';
    progressContainer.style.display = 'block';

    // Upload file
    const formData = new FormData();
    formData.append('video', file);

    try {
        progressText.textContent = 'Uploading video...';
        progressFill.style.width = '30%';

        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            throw new Error('Upload failed');
        }

        const uploadData = await uploadResponse.json();
        currentVideoId = uploadData.video_id;

        // Analyze video
        progressText.textContent = 'Analyzing emotions and generating recommendations...';
        progressFill.style.width = '60%';

        const analyzeResponse = await fetch(`/analyze/${currentVideoId}`);

        if (!analyzeResponse.ok) {
            throw new Error('Analysis failed');
        }

        const results = await analyzeResponse.json();

        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';

        // Display results
        setTimeout(() => {
            displayResults(results);
        }, 500);

    } catch (error) {
        alert('Error: ' + error.message);
        resetApp();
    }
}

function displayResults(data) {
    // Hide upload, show results
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'block';

    // Display emotions
    displayEmotions(data.emotions.combined);

    // Display recommendations
    displayRecommendations(data.classical_recommendations, 'classicalRecs');
    displayRecommendations(data.quantum_recommendations, 'quantumRecs');

    // Display quantum properties
    displayQuantumInfo(data.quantum_recommendations.quantum_properties);
}

function displayEmotions(emotions) {
    const grid = document.getElementById('emotionsGrid');
    grid.innerHTML = '';

    // Sort by value
    const sortedEmotions = Object.entries(emotions)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6); // Top 6 emotions

    sortedEmotions.forEach(([emotion, value]) => {
        const item = document.createElement('div');
        item.className = 'emotion-item';
        item.innerHTML = `
            <div class="emotion-name">${emotion}</div>
            <div class="emotion-value">${(value * 100).toFixed(1)}%</div>
        `;
        grid.appendChild(item);
    });
}

function displayRecommendations(recData, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    const recommendations = recData.recommendations || [];

    recommendations.forEach((rec, index) => {
        const item = document.createElement('div');
        item.className = 'rec-item';
        item.style.animationDelay = `${index * 0.1}s`;
        item.innerHTML = `
            <div class="rec-header">
                <div class="rec-dance">${rec.dance_style}</div>
                <div class="rec-score">${(rec.score * 100).toFixed(0)}%</div>
            </div>
            <div class="rec-reasoning">${rec.reasoning}</div>
        `;
        container.appendChild(item);
    });
}

function displayQuantumInfo(properties) {
    const container = document.getElementById('quantumInfo');
    container.innerHTML = '<h3 style="margin-bottom: 0.75rem; font-size: 1rem;">Quantum Properties</h3>';

    const props = [
        { label: 'Superposition Entropy', value: properties.superposition_entropy.toFixed(3) },
        { label: 'Entanglement Strength', value: properties.entanglement_strength.toFixed(2) },
        { label: 'Quantum Coherence', value: properties.coherence.toFixed(3) }
    ];

    props.forEach(prop => {
        const div = document.createElement('div');
        div.className = 'quantum-property';
        div.innerHTML = `
            <span>${prop.label}:</span>
            <strong>${prop.value}</strong>
        `;
        container.appendChild(div);
    });
}

function resetApp() {
    uploadSection.style.display = 'block';
    resultsSection.style.display = 'none';
    uploadArea.style.display = 'block';
    progressContainer.style.display = 'none';
    progressFill.style.width = '0%';
    videoInput.value = '';
    currentVideoId = null;
}
