// Simple SHA-256 implementation for client-side hashing
// Used for block tampering demo

async function sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

// Synchronous version using a simple fallback
function sha256Sync(str) {
    // For demo purposes, we'll use a deterministic hash
    // In a real app, you'd want to use a proper SHA-256 library
    // But for detecting tampering, any consistent hash function works

    let hash = 0;
    if (str.length === 0) return '0'.repeat(64);

    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }

    // Convert to positive hex and pad
    const hex = (Math.abs(hash) >>> 0).toString(16);
    return hex.padStart(64, '0');
}
