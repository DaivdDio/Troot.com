<script>
    document.addEventListener('submit', async function(e) {

        // ADD JOB
        if (e.target.id === 'addJobForm') {
            e.preventDefault();

            const form = e.target;
            const button = document.getElementById('uploadBtn');
            const status = document.getElementById('uploadStatus');

            button.disabled = true;
            button.textContent = 'Uploading...';

            status.innerHTML = `
                <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                Uploading image...
            `;

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (data.success) {

                    status.innerHTML = `
                        <div class="alert alert-success py-2 mb-0">
                            Job uploaded successfully.
                        </div>
                    `;

                    form.reset();

                    setTimeout(() => {
                        location.reload();
                    }, 800);

                } else {

                    status.innerHTML = `
                        <div class="alert alert-danger py-2 mb-0">
                            ${data.error || 'Failed to upload job'}
                        </div>
                    `;

                    button.disabled = false;
                    button.textContent = 'Upload';
                }

            } catch (err) {

                status.innerHTML = `
                    <div class="alert alert-danger py-2 mb-0">
                        Upload failed.
                    </div>
                `;

                button.disabled = false;
                button.textContent = 'Upload';
            }

            return;
        }

        // DELETE JOB
        if (e.target.classList.contains('delete-job-form')) {
            e.preventDefault();

            if (!confirm('Are you sure you want to delete this job?')) {
                return;
            }

            const form = e.target;

            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                location.reload();
            } else {
                alert('Failed to delete job.');
            }
        }

        // EDIT JOB
        if (e.target.classList.contains('editJobForm')) {

            e.preventDefault();

            if (!confirm('Are you sure you want to save these changes?')) {
                return;
            }

            const form = e.target;

            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {

                // Remove edit query parameter and close form
                const url = new URL(window.location);

                url.searchParams.delete('edit');
                url.searchParams.set('view', 'grid');

                // keep pagination
                /*if (!url.searchParams.get('page')) {
                    url.searchParams.set('page', '{{ jobs.number }}');
                }*/

                window.location.href = url.toString();

            } else {
                alert('Failed to update job.');
            }

            return;
        }

        //------------------------------------------------------------------------------------------------------------

        // =====================================
        // ADD TREE
        // =====================================

        if (e.target.id === 'addTreeForm') {

            e.preventDefault();

            const form = e.target;
            const button = form.querySelector('button[type="submit"]');
            const status = document.getElementById('treeUploadStatus');

            button.disabled = true;
            button.textContent = 'Saving...';

            status.innerHTML = `
                <div class="spinner-border spinner-border-sm me-2"></div>
                Processing...
            `;

            try {

                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (data.success) {

                    status.innerHTML = `
                        <div class="alert alert-success py-2 mb-0">
                            ${data.message || 'Upload completed'}
                        </div>
                    `;

                    setTimeout(() => {
                        location.reload();
                    }, 1200);

                } else {

                    status.innerHTML = `
                        <div class="alert alert-danger py-2 mb-0">
                            ${data.error || 'Something went wrong'}
                        </div>
                    `;

                    button.disabled = false;
                    button.textContent = 'Save Tree';
                }

            } catch (err) {

                status.innerHTML = `
                    <div class="alert alert-danger py-2 mb-0">
                        Upload failed
                    </div>
                `;

                button.disabled = false;
                button.textContent = 'Save Tree';
            }

            return;
        }

        // =====================================
        // DELETE TREE
        // =====================================

        if (e.target.classList.contains('delete-tree-form')) {

            e.preventDefault();

            if (!confirm('Delete this tree?')) {
                return;
            }

            const form = e.target;

            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                location.reload();
            } else {
                alert('Failed to delete tree.');
            }

            return;
        }

        // =====================================
        // EDIT TREE
        // =====================================

        if (e.target.matches('.editTreeForm')) {

            e.preventDefault();

            const form = e.target;

            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {

                alert("Tree updated successfully");

                setTimeout(() => {
                    const url = new URL(window.location);
                    url.searchParams.delete('edit');
                    window.location.href = url.toString();
                }, 300);
            } else {
                alert('Failed to update tree.');
            }

            return;
        }

    });

    // =====================================
    // TREE CHECKBOX SELECTION
    // =====================================

    document.addEventListener('change', function(e) {

        if (!e.target.classList.contains('tree-checkbox')) {
            return;
        }

        const selected =
            document.querySelectorAll('.tree-checkbox:checked');

        const editBtn =
            document.getElementById('editSelectedTree');

        const deleteBtn =
            document.getElementById('deleteSelectedTrees');

        if (editBtn) {
            editBtn.disabled = selected.length !== 1;
        }

        if (deleteBtn) {
            deleteBtn.disabled = selected.length === 0;
        }

    });


    // =====================================
    // EDIT SELECTED TREE
    // =====================================

    const editSelectedBtn =
        document.getElementById('editSelectedTree');

    if (editSelectedBtn) {

        editSelectedBtn.addEventListener('click', function () {

            const selected = document.querySelector('.tree-checkbox:checked');

            if (!selected) {
                alert('Select a tree first.');
                return;
            }

            const treeId = selected.value;

            const url = new URL(window.location);

            url.searchParams.set('section', 'trees');
            url.searchParams.set('edit', treeId);

            // 🔥 IMPORTANT: preserve current view mode
            const currentView = url.searchParams.get('view') || 'list';
            url.searchParams.set('view', currentView);

            window.location.href = url.toString();
        });

    }


    // =====================================
    // DELETE SELECTED TREES
    // =====================================

    const deleteSelectedBtn =
        document.getElementById('deleteSelectedTrees');

    if (deleteSelectedBtn) {

        deleteSelectedBtn.addEventListener('click', async function() {

            const selected =
                document.querySelectorAll('.tree-checkbox:checked');

            if (!selected.length) {
                alert('Select at least one tree.');
                return;
            }

            if (!confirm(`Delete ${selected.length} tree(s)?`)) {
                return;
            }

            const ids =
                [...selected].map(cb => cb.value);

            function getCSRFToken() {
                return document.cookie
                    .split('; ')
                    .find(row => row.startsWith('csrftoken='))
                    ?.split('=')[1] || '';
            }
            try {
                const response = await fetch("{% url 'trees:delete_trees' %}", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: JSON.stringify({ ids })
                });

                if (!response.ok) {
                    const text = await response.text();
                    console.error("Server error response:", text);
                    throw new Error(`Server error: ${response.status}`);
                }

                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    throw new Error("Invalid response format");
                }

                const data = await response.json();

                if (data.success) {
                    alert(`${data.deleted} tree(s) deleted`);
                    location.reload();
                } else {
                    alert("Failed to delete trees");
                }

            } catch (err) {
                console.error(err);
                alert("Something went wrong. Please try again.");
            }

        });

    }

</script>