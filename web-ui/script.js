// Global variables
let uploadedFile = null;
let processingInterval = null;

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const processingSection = document.getElementById('processingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const progressFill = document.getElementById('progressFill');
const processingStatus = document.getElementById('processingStatus');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Download buttons
    document.getElementById('downloadCsv').addEventListener('click', () => downloadFile('csv'));
    document.getElementById('downloadExcel').addEventListener('click', () => downloadFile('excel'));
    document.getElementById('downloadSummary').addEventListener('click', () => downloadFile('summary'));
}

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File selection handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// File handling
function handleFile(file) {
    // Validate file type
    if (file.type !== 'application/pdf') {
        showError('Please select a valid PDF file.');
        return;
    }
    
    // Validate file size (50MB limit)
    if (file.size > 50 * 1024 * 1024) {
        showError('File size must be less than 50MB.');
        return;
    }
    
    uploadedFile = file;
    startProcessing();
}

// Real PDF processing
function startProcessing() {
    showProcessing();
    
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', uploadedFile);
    
    // Update progress
    processingStatus.textContent = 'Uploading PDF...';
    progressFill.style.width = '10%';
    
    // Upload and process the file
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update progress
            processingStatus.textContent = 'Processing complete!';
            progressFill.style.width = '100%';
            
            // Store session data
            window.sessionData = data;
            
            // Show results with real data
            setTimeout(() => {
                showResults(data.stats);
            }, 500);
        } else {
            showError(data.error || 'Processing failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Network error: ' + error.message);
    });
}

// Show processing section
function showProcessing() {
    hideAllSections();
    processingSection.style.display = 'block';
    processingSection.classList.add('fade-in');
}

// Show results section
function showResults(stats) {
    hideAllSections();
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Display real results data
    document.getElementById('transactionCount').textContent = stats.transaction_count.toLocaleString();
    document.getElementById('pageCount').textContent = stats.page_count.toLocaleString();
    document.getElementById('categoryCount').textContent = stats.category_count.toLocaleString();
}

// Show error section
function showError(message) {
    hideAllSections();
    errorSection.style.display = 'block';
    errorSection.classList.add('fade-in');
    document.getElementById('errorMessage').textContent = message;
}

// Hide all sections
function hideAllSections() {
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    processingSection.classList.remove('fade-in');
    resultsSection.classList.remove('fade-in');
    errorSection.classList.remove('fade-in');
}

// Download file function
function downloadFile(type) {
    if (!window.sessionData || !window.sessionData.session_id) {
        showError('No processed data available. Please upload and process a PDF first.');
        return;
    }
    
    // Download the actual processed file
    const sessionId = window.sessionData.session_id;
    const downloadUrl = `/download/${sessionId}/${type}`;
    
    // Create a temporary link and trigger download
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = ''; // Let the server determine the filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Demo data functions removed - only real processing now

// Reset form function
function resetForm() {
    uploadedFile = null;
    fileInput.value = '';
    hideAllSections();
    if (processingInterval) {
        clearInterval(processingInterval);
        processingInterval = null;
    }
    progressFill.style.width = '0%';
}

// Add some interactive features
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        resetForm();
    }
});

// Add file validation feedback
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const fileSize = (file.size / (1024 * 1024)).toFixed(2);
        console.log(`Selected file: ${file.name} (${fileSize} MB)`);
    }
});
