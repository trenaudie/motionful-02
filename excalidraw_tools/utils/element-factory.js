const { generateRandomId, generateRandomSeed, generateIndex } = require('./id-generators');

/**
 * Factory for creating Excalidraw elements
 */

/**
 * Creates an image element object for Excalidraw
 * @param {string} fileId - The file ID from the converted PNG
 * @param {number} width - Image width
 * @param {number} height - Image height
 * @returns {Object} - Excalidraw image element object
 */
function createImageElement(fileId, width = 130, height = 170) {
    const timestamp = Date.now();
    const elementId = generateRandomId();
    
    return {
        id: elementId,
        type: "image",
        x: 400, // Central position
        y: 300, // Central position
        width: width,
        height: height,
        angle: 0,
        strokeColor: "transparent",
        backgroundColor: "transparent",
        fillStyle: "solid",
        strokeWidth: 2,
        strokeStyle: "solid",
        roughness: 1,
        opacity: 100,
        groupIds: [],
        frameId: null,
        index: generateIndex(),
        roundness: null,
        seed: generateRandomSeed(),
        version: 1,
        versionNonce: generateRandomSeed(),
        isDeleted: false,
        boundElements: null,
        updated: timestamp,
        link: null,
        locked: false,
        status: "saved",
        fileId: fileId,
        scale: [1, 1],
        crop: null
    };
}

module.exports = {
    createImageElement
};