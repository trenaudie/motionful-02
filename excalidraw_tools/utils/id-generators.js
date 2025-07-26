/**
 * ID and random value generators for Excalidraw elements
 */

/**
 * Generates a random string for Excalidraw IDs
 * @param {number} length - Length of the random string
 * @returns {string} - Random string
 */
function generateRandomId(length = 20) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

/**
 * Generates a random seed for Excalidraw elements
 * @returns {number} - Random seed
 */
function generateRandomSeed() {
    return Math.floor(Math.random() * 2000000000) + 1000000000;
}

/**
 * Generates an index string for element ordering
 * @returns {string} - Index string
 */
function generateIndex() {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    return chars.charAt(Math.floor(Math.random() * chars.length)) + 
           chars.charAt(Math.floor(Math.random() * chars.length));
}

module.exports = {
    generateRandomId,
    generateRandomSeed,
    generateIndex
};