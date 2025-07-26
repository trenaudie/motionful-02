const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Converts a PNG file to Excalidraw file format
 * @param {string} filename - The filename or filepath of the PNG in public/assets/png
 * @returns {Object} - Excalidraw files object with the converted PNG
 */
function pngToJson(filename) {
    try {
        // Construct the full path to the PNG file
        const pngPath = path.join('public', 'assets', 'pngs', filename);
        
        // Check if file exists
        if (!fs.existsSync(pngPath)) {
            throw new Error(`PNG file not found: ${pngPath}`);
        }
        
        // Read the PNG file
        const pngBuffer = fs.readFileSync(pngPath);
        
        // Convert to base64
        const base64Data = pngBuffer.toString('base64');
        
        // Create the data URL
        const dataURL = `data:image/png;base64,${base64Data}`;
        
        // Generate SHA-256 hash for the file ID (using the buffer data)
        const hash = crypto.createHash('sha256');
        hash.update(pngBuffer);
        const fileId = hash.digest('hex');
        
        // Get current timestamp
        const timestamp = Date.now();
        
        // Create the Excalidraw file format
        const excalidrawFile = {
            mimeType: "image/png",
            id: fileId,
            dataURL: dataURL,
            created: timestamp,
            lastRetrieved: timestamp
        };
        
        // Return in the expected format
        return {
            files: {
                [fileId]: excalidrawFile
            }
        };
        
    } catch (error) {
        console.error('Error converting PNG to JSON:', error.message);
        throw error;
    }
}

// Export for use as a module
module.exports = { pngToJson };

// CLI usage
if (require.main === module) {
    const filename = process.argv[2];
    
    if (!filename) {
        console.error('Usage: node png_to_json.js <filename>');
        process.exit(1);
    }
    
    try {
        const result = pngToJson(filename);
        console.log(JSON.stringify(result, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}