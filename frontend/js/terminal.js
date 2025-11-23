// Terminal UI utilities

const Terminal = {
    // Helper functions for terminal UI

    createBox(title, content) {
        return `
            <div class="terminal-box">
                <div class="box-title">${title}</div>
                <div class="box-content">${content}</div>
            </div>
        `;
    },

    createProgressBar(percentage, width = 10) {
        const filled = Math.floor((percentage / 100) * width);
        const empty = width - filled;
        return '█'.repeat(filled) + '░'.repeat(empty);
    },

    createTable(headers, rows) {
        let html = '<table class="data-table"><thead><tr>';
        headers.forEach(h => {
            html += `<th>${h}</th>`;
        });
        html += '</tr></thead><tbody>';

        rows.forEach(row => {
            html += '<tr>';
            row.forEach(cell => {
                html += `<td>${cell}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table>';
        return html;
    },

    truncateHash(hash, length = 12) {
        if (!hash || hash.length <= length) return hash;
        return hash.substring(0, length) + '...';
    },

    formatTimestamp(timestamp) {
        return timestamp.replace('T', ' ').split('.')[0];
    }
};
