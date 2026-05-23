// ─── DOM Elements ───
const dropZone       = document.getElementById('dropZone');
const fileInput      = document.getElementById('fileInput');
const dropZoneContent = document.getElementById('dropZoneContent');
const previewContainer = document.getElementById('previewContainer');
const imagePreview   = document.getElementById('imagePreview');
const fileNameEl     = document.getElementById('fileName');
const predictBtn     = document.getElementById('predictBtn');
const btnText        = document.getElementById('btnText');
const btnLoading     = document.getElementById('btnLoading');
const uploadForm     = document.getElementById('uploadForm');

const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];
const MAX_SIZE_MB   = 10;

// ─── Click to open file dialog ───
dropZone.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-remove')) return;
    fileInput.click();
});

// ─── File selected via dialog ───
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleFile(fileInput.files[0]);
    }
});

// ─── Drag & Drop events ───
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
        // Sync with file input
        const dt = new DataTransfer();
        dt.items.add(files[0]);
        fileInput.files = dt.files;
    }
});

// ─── Handle and validate file ───
function handleFile(file) {
    // Validate type
    if (!ALLOWED_TYPES.includes(file.type)) {
        showError('❌ Invalid file type. Please upload a JPG or PNG image.');
        return;
    }

    // Validate size
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
        showError(`❌ File is too large. Maximum size is ${MAX_SIZE_MB}MB.`);
        return;
    }

    // Read and preview image
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        fileNameEl.textContent = `📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        showPreview();
    };
    reader.readAsDataURL(file);
}

function showPreview() {
    dropZoneContent.style.display = 'none';
    previewContainer.style.display = 'block';
    predictBtn.disabled = false;
}

function removeFile() {
    fileInput.value = '';
    imagePreview.src = '';
    fileNameEl.textContent = '';
    previewContainer.style.display = 'none';
    dropZoneContent.style.display = 'block';
    predictBtn.disabled = true;
}

// ─── Show loading state on form submit ───
if (uploadForm) {
    uploadForm.addEventListener('submit', (e) => {
        if (!fileInput.files.length) {
            e.preventDefault();
            showError('⚠️ Please select an X-ray image before submitting.');
            return;
        }
        // Show loading state
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        predictBtn.disabled = true;
    });
}

// ─── Helper: show inline error ───
function showError(message) {
    // Remove any existing inline error
    const existing = document.querySelector('.inline-error');
    if (existing) existing.remove();

    const div = document.createElement('div');
    div.className = 'flash-error inline-error';
    div.style.marginTop = '16px';
    div.textContent = message;

    const formActions = document.querySelector('.form-actions');
    if (formActions) {
        formActions.parentNode.insertBefore(div, formActions);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => { if (div.parentNode) div.remove(); }, 5000);
}

// ─── Auto-dismiss flash messages ───
document.querySelectorAll('.flash-error').forEach(el => {
    setTimeout(() => {
        el.style.transition = 'opacity 0.5s';
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 500);
    }, 5000);
});
