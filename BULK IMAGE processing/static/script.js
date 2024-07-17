let detailedReport = [];
let currentPage = 1;
const itemsPerPage = 5;

function startProcessing() {
    fetch('/process_images', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        detailedReport = data.detailed_report;
        displaySummary(data.summary_report);
        displayPage(1);
        setupPagination(detailedReport.length);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displaySummary(summaryReport) {
    let summaryTable = `
    <h2>Summary Report:</h2>
    <table>
        <tr><th>Description</th><th>Value</th></tr>
        <tr><td>Total Images Found</td><td>${summaryReport.total_images}</td></tr>
        <tr><td>Total Processed</td><td>${summaryReport.total_processed}</td></tr>
        <tr><td>Total Time taken</td><td>${summaryReport.total_time}</td></tr>
        <tr><td>Total Remaining</td><td>${summaryReport.total_remaining}</td></tr>
        <tr><td>In Processing Queue</td><td>${summaryReport.in_processing_queue}</td></tr>
        <tr><td>Total Celery Workers</td><td>${summaryReport.total_celery_workers}</td></tr>
        <tr><td>Total Yolo Models Pre Loaded</td><td>${summaryReport.total_yolo_models}</td></tr>
    </table>
    `;
    document.getElementById('summary').innerHTML = summaryTable;
}

function displayPage(page) {
    currentPage = page;
    let start = (page - 1) * itemsPerPage;
    let end = start + itemsPerPage;
    let pageData = detailedReport.slice(start, end);

    let detailedTable = `
    <h2>Detailed Report:</h2>
    <table>
        <tr><th>S.No</th><th>Image Name</th><th>Job ID</th><th>Execution Time</th><th>View Original</th><th>View Processed</th><th>List of Objects</th><th>Status</th></tr>
    `;

    pageData.forEach((result, index) => {
        detailedTable += `
        <tr>
            <td>${start + index + 1}</td>
            <td>${result.image_name}</td>
            <td>${result.job_id}</td>
            <td>${result.execution_time_ms} ms</td>
            <td><a href="${result.view_original}" target="_blank">View Original</a></td>
            <td><a href="${result.view_processed}" target="_blank">View Processed</a></td>
            <td>${result.list_of_objects.join(', ')}</td>
            <td>${result.status}</td>
        </tr>
        `;
    });

    detailedTable += `</table>`;
    document.getElementById('reports').innerHTML = detailedTable;
}

function setupPagination(totalItems) {
    let totalPages = Math.ceil(totalItems / itemsPerPage);
    let paginationControls = '';

    for (let i = 1; i <= totalPages; i++) {
        paginationControls += `<button onclick="displayPage(${i})">${i}</button>`;
    }

    document.getElementById('pagination').innerHTML = paginationControls;
}

function uploadImages() {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const fileCount = document.getElementById('fileCount');

    imageUpload.click();

    imageUpload.addEventListener('change', (event) => {
        const files = event.target.files;
        if (files.length > 0) {
            if (files.length > 1) {
                imagePreview.style.display = 'none';
                fileCount.style.display = 'block';
                fileCount.textContent = `${files.length} files selected`;
            } else {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                    fileCount.style.display = 'none';
                };
                reader.readAsDataURL(files[0]);
            }
        }
    });
}
