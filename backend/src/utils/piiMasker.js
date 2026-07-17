/**
 * Masks PII based on type.
 * @param {string} type - The type of PII (e.g., PHONE_NUMBER, EMAIL, CREDIT_CARD).
 * @param {string} text - The original text to mask.
 * @returns {string} - The masked text.
 */
function maskPII(type, text) {
    if (!text) return "";

    const visibleChars = 4;

    if (text.length <= visibleChars) {
        return "*".repeat(text.length);
    }

    if (type === 'EMAIL') {
        const [local, domain] = text.split('@');
        const maskedLocal = local.length > 2 ? local.substring(0, 2) + '*'.repeat(local.length - 2) : '*'.repeat(local.length);
        return `${maskedLocal}@${domain}`;
    }

    if (type === 'CREDIT_CARD' || type === 'PHONE_NUMBER' || type === 'AADHAAR' || type === 'SSN') {
        return '*'.repeat(text.length - visibleChars) + text.slice(-visibleChars);
    }

    // Default: mask everything except last few chars
    return '*'.repeat(text.length - visibleChars) + text.slice(-visibleChars);
}

module.exports = {
    maskPII
};
