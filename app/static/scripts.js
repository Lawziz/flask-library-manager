function showAlert(message, type) {
        const container = document.getElementById('alert-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerText = message;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 4000); // Auto disappear after 4 seconds
    }

    // Fetch data from Flask API and redraw the tables dynamically
    async function loadDashboardData() {
        try {
            const response = await fetch('/api/data');
            const data = await response.json();

            // 1. Draw Books Table
            const booksBody = document.getElementById('booksTableBody');
            booksBody.innerHTML = data.books.map(book => `
                <tr>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.isbn}</td>
                    <td>
                        <span class="badge ${book.is_available ? 'available' : 'borrowed'}">
                            ${book.is_available ? 'Available' : 'Borrowed'}
                        </span>
                    </td>
                </tr>
            `).join('');

            // 2. Draw Members Table
            const membersBody = document.getElementById('membersTableBody');
            membersBody.innerHTML = data.members.map(member => `
                <tr>
                    <td>${member.name}</td>
                    <td><code>${member.member_id}</code></td>
                    <td>${member.borrowed_books.length > 0 ? member.borrowed_books.join(', ') : '<em>None</em>'}</td>
                </tr>
            `).join('');
        } catch (err) {
            console.error("Error loading dashboard data:", err);
        }
    }

    // Handle Form Submissions via JS Fetch API
    async function sendAction(url, bodyData, formToReset = null) {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });
        const result = await response.json();

        showAlert(result.message, result.success ? 'success' : 'danger');

        if (result.success) {
            if (formToReset) formToReset.reset();
            loadDashboardData(); // Refresh UI instantly without breaking layout or reloading
        }
    }

    // Event Listeners for Buttons/Forms
    document.getElementById('bookForm').addEventListener('submit', (e) => {
        e.preventDefault();
        sendAction('/api/add_book', {
            title: document.getElementById('bookTitle').value,
            author: document.getElementById('bookAuthor').value,
            isbn: document.getElementById('bookIsbn').value
        }, e.target);
    });

    document.getElementById('memberForm').addEventListener('submit', (e) => {
        e.preventDefault();
        sendAction('/api/add_member', {
            name: document.getElementById('memberName').value,
            member_id: document.getElementById('memberId').value
        }, e.target);
    });

    document.getElementById('btnBorrow').addEventListener('click', () => {
        sendAction('/api/borrow', {
            member_id: document.getElementById('opsMemberId').value,
            isbn: document.getElementById('opsIsbn').value
        }, document.getElementById('opsForm'));
    });

    document.getElementById('btnReturn').addEventListener('click', () => {
        sendAction('/api/return', {
            member_id: document.getElementById('opsMemberId').value,
            isbn: document.getElementById('opsIsbn').value
        }, document.getElementById('opsForm'));
    });

    // Initial paint on open
    window.onload = loadDashboardData;