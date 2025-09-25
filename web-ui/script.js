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

// Generate sample CSV data
function generateSampleCSV() {
    return `Date,Narration,Category,Withdrawal_Amount,Deposit_Amount,Closing_Balance
15/07/2020,UPI payment to merchant,UPI Payments,150.00,0.00,25000.00
16/07/2020,Salary credit from company,Salary & Employment,0.00,25000.00,50000.00
17/07/2020,Foreign remittance from USA,Foreign Exchange,0.00,50000.00,100000.00
18/07/2020,ATM withdrawal,Card Payments,2000.00,0.00,98000.00
19/07/2020,Cheque payment 123456,Cheque Transactions,5000.00,0.00,93000.00
20/07/2020,Interest credit,Investment Income,0.00,500.00,93500.00
21/07/2020,Donation to charity,Charitable & Donations,1000.00,0.00,92500.00
22/07/2020,Electricity bill payment,Utilities,2500.00,0.00,90000.00
23/07/2020,Amazon purchase,Shopping & Retail,1500.00,0.00,88500.00
24/07/2020,Swiggy food order,Food & Dining,300.00,0.00,88200.00`;
}

// Generate sample summary
function generateSampleSummary() {
    return `# HDFC Bank Statement Analysis

## Summary
- **Total Transactions**: 3,602
- **Pages Processed**: 165/165 (100%)
- **Date Range**: 15/07/2020 to 12/08/2025
- **Extraction Time**: ~2 minutes

## Financial Summary
- **Total Withdrawals**: ₹57,764,839.23
- **Total Deposits**: ₹78,842,318.06
- **Net Amount**: ₹21,077,478.83

## Category Breakdown
- **Foreign Exchange**: ₹42,328,183.94 (36 transactions)
- **Salary & Employment**: ₹3,694,615.00 (14 transactions)
- **UPI Payments**: ₹2,968,026.45 (2,130 transactions)
- **Card Payments**: ₹3,286,773.73 (146 transactions)
- **Cheque Transactions**: ₹15,630,308.00 (26 transactions)

## Data Quality
- **Valid Dates**: 100%
- **Complete Transactions**: 100%
- **Categories Identified**: 22

---
*Generated by HDFC PDF to CSV Converter*
*Repository: https://github.com/vishwaraja/hdfc-pdf-converter*`;
}

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
