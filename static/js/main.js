// Helper to show modals and send AJAX requests for create/rename/delete
// Assumes modals exist in the HTML (to be added in file_manager.html)

document.addEventListener('DOMContentLoaded', function() {
  // Rename
  document.querySelectorAll('.rename-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const path = this.dataset.path;
      const name = this.dataset.name;
      const newName = prompt('Rename to:', name);
      if (newName && newName !== name) {
        fetch('/rename', {
          method: 'POST',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: `path=${encodeURIComponent(path)}&new_name=${encodeURIComponent(newName)}`
        }).then(() => location.reload());
      }
    });
  });
  // Delete
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const path = this.dataset.path;
      if (confirm('Delete ' + this.dataset.name + '?')) {
        fetch('/delete', {
          method: 'POST',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: `path=${encodeURIComponent(path)}`
        }).then(() => location.reload());
      }
    });
  });
  // Create (modal)
  const createBtn = document.querySelector('[data-bs-target="#createModal"]');
  if (createBtn) {
    createBtn.addEventListener('click', function() {
      const modal = document.getElementById('createModal');
      if (modal) {
        modal.querySelector('form').reset();
      }
    });
  }
  const createForm = document.getElementById('createForm');
  if (createForm) {
    createForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const data = new FormData(createForm);
      fetch('/create', {
        method: 'POST',
        body: new URLSearchParams([...data])
      }).then(() => location.reload());
    });
  }
}); 