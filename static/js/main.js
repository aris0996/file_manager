let currentPath = '';

function showNotification(msg, isError = false) {
    const notif = document.getElementById('notification');
    notif.textContent = msg;
    notif.style.background = isError ? '#f44336' : '#4caf50';
    notif.style.display = 'block';
    setTimeout(() => notif.style.display = 'none', 2000);
}

function updateBreadcrumb() {
    const breadcrumb = document.getElementById('breadcrumb');
    const parts = currentPath.split('/').filter(Boolean);
    breadcrumb.innerHTML = '<a href="#" data-path="">root</a>';
    let path = '';
    parts.forEach((part, idx) => {
        path += '/' + part;
        breadcrumb.innerHTML += ' / <a href="#" data-path="' + path.slice(1) + '">' + part + '</a>';
    });
    breadcrumb.querySelectorAll('a').forEach(a => {
        a.onclick = (e) => {
            e.preventDefault();
            currentPath = a.dataset.path;
            loadFiles();
        };
    });
}

function loadFiles() {
    fetch(`/api/list?path=${encodeURIComponent(currentPath)}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) return showNotification(data.error, true);
            const fileList = document.getElementById('file-list');
            fileList.innerHTML = '';
            data.folders.forEach(folder => {
                const div = document.createElement('div');
                div.className = 'folder';
                div.textContent = folder;
                div.onclick = () => {
                    currentPath = (currentPath ? currentPath + '/' : '') + folder;
                    loadFiles();
                };
                fileList.appendChild(div);
            });
            data.files.forEach(file => {
                const div = document.createElement('div');
                div.className = 'file';
                div.textContent = file;
                div.onclick = () => {
                    window.open(`/api/download?path=${encodeURIComponent(currentPath)}&filename=${encodeURIComponent(file)}`);
                };
                // Delete button
                const delBtn = document.createElement('button');
                delBtn.textContent = 'Delete';
                delBtn.onclick = (e) => {
                    e.stopPropagation();
                    fetch('/api/delete', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({path: currentPath, name: file})
                    }).then(r => r.json()).then(() => {
                        showNotification('File deleted');
                        loadFiles();
                    });
                };
                div.appendChild(delBtn);
                // Rename button
                const renBtn = document.createElement('button');
                renBtn.textContent = 'Rename';
                renBtn.onclick = (e) => {
                    e.stopPropagation();
                    const newName = prompt('Rename file:', file);
                    if (newName && newName !== file) {
                        fetch('/api/rename', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({path: currentPath, old_name: file, new_name: newName})
                        }).then(r => r.json()).then(() => {
                            showNotification('File renamed');
                            loadFiles();
                        });
                    }
                };
                div.appendChild(renBtn);
                fileList.appendChild(div);
            });
            updateBreadcrumb();
        });
}

document.getElementById('upload-btn').onclick = () => {
    const input = document.getElementById('file-upload');
    if (!input.files.length) return showNotification('No file selected', true);
    const formData = new FormData();
    formData.append('path', currentPath);
    for (const file of input.files) {
        formData.append('file', file);
        fetch('/api/upload', {method: 'POST', body: formData})
            .then(r => r.json())
            .then(() => {
                showNotification('File uploaded');
                loadFiles();
            });
    }
    input.value = '';
};

document.getElementById('new-folder-btn').onclick = () => {
    const name = prompt('Folder name:');
    if (!name) return;
    fetch('/api/upload', {
        method: 'POST',
        body: new FormData()
    }); // Dummy, should be implemented as needed
    // For now, create folder via upload endpoint (can be improved)
    fetch('/api/rename', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({path: currentPath, old_name: '', new_name: name})
    }).then(() => loadFiles());
};

window.onload = loadFiles; 