/**
 * Append PNG to Excalidraw Tool
 * 
 * A Node.js utility tool for appending PNG images to Excalidraw JSON files as image elements.
 * This tool converts PNG files to Excalidraw-compatible format and integrates them into existing
 * Excalidraw documents with proper positioning, scaling, and metadata.
 * 
 * Features:
 * - Converts PNG files to base64-encoded Excalidraw file objects
 * - Creates properly formatted image elements with randomized IDs and seeds
 * - Integrates images into existing Excalidraw JSON documents
 * - Supports customizable positioning and sizing options
 * - Maintains Excalidraw document structure and compatibility
 * 
 * Usage:
 * - Module: const { appendPngToExcalidraw } = require('./append_png_to_excalidraw');
 * - CLI: node append_png_to_excalidraw.js <png_file_path> <excalidraw_json_path>
 * 
 * Parameters:
 * - pngFilePath: Path to PNG file (relative to public/assets/pngs)
 * - excalidrawJsonPath: Path to target Excalidraw JSON file
 * - options: Optional object with width, height, x, y positioning parameters
 * 
 * Returns:
 * - Object with fileId, elementId, and success status
 * 
 * Dependencies:
 * - fs: File system operations
 * - path: Path manipulation utilities
 * - ./png_to_json: PNG to Excalidraw file format conversion
 * 
 * Example:
 * appendPngToExcalidraw('icon.png', './diagram.excalidraw', { width: 200, height: 150 });
 */
const fs = require('fs');
const { pngToJson } = require('./png_to_json');
const { createImageElement } = require('./utils/element-factory');

/**
 * Appends a PNG file to an Excalidraw JSON file
 * @param {string} pngFilePath - Path to the PNG file (relative to public/assets/pngs)
 * @param {string} excalidrawJsonPath - Path to the Excalidraw JSON file
 * @param {Object} options - Optional parameters for positioning and sizing
 */
function appendPngToExcalidraw(pngFilePath, excalidrawJsonPath, options = {}) {
    try {
        // Convert PNG to JSON format
        console.log('Converting PNG to JSON format...');
        const pngJsonData = pngToJson(pngFilePath);
        
        // Get the file ID and file object
        const fileId = Object.keys(pngJsonData.files)[0];
        const fileObject = pngJsonData.files[fileId];
        
        // Read the existing Excalidraw JSON file
        console.log('Reading existing Excalidraw file...');
        if (!fs.existsSync(excalidrawJsonPath)) {
            throw new Error(`Excalidraw file not found: ${excalidrawJsonPath}`);
        }
        
        const excalidrawData = JSON.parse(fs.readFileSync(excalidrawJsonPath, 'utf8'));
        
        // Ensure the necessary structure exists
        if (!excalidrawData.elements) {
            excalidrawData.elements = [];
        }
        if (!excalidrawData.files) {
            excalidrawData.files = {};
        }
        
        // Create the image element
        console.log('Creating image element...');
        const imageElement = createImageElement(
            fileId, 
            options.width || 130, 
            options.height || 170
        );
        
        // Add the file object to the files dictionary
        console.log('Adding file object to files dictionary...');
        excalidrawData.files[fileId] = fileObject;
        
        // Add the image element to the elements array
        console.log('Adding image element to elements array...');
        excalidrawData.elements.push(imageElement);
        
        // Update the appState if it exists
        if (excalidrawData.appState) {
            excalidrawData.appState.currentItemFontFamily = excalidrawData.appState.currentItemFontFamily || 1;
        }
        
        // Write the updated JSON back to the file
        console.log('Writing updated JSON back to file...');
        fs.writeFileSync(excalidrawJsonPath, JSON.stringify(excalidrawData, null, 2));
        
        console.log(`Successfully added ${pngFilePath} to ${excalidrawJsonPath}`);
        console.log(`File ID: ${fileId}`);
        console.log(`Element ID: ${imageElement.id}`);
        
        return {
            fileId: fileId,
            elementId: imageElement.id,
            success: true
        };
        
    } catch (error) {
        console.error('Error appending PNG to Excalidraw:', error.message);
        throw error;
    }
}

// Export for use as a module
module.exports = { appendPngToExcalidraw };

// CLI usage
if (require.main === module) {
    const pngFilePath = process.argv[2];
    const excalidrawJsonPath = process.argv[3];
    
    if (!pngFilePath || !excalidrawJsonPath) {
        console.error('Usage: node append_png_to_excalidraw.js <png_file_path> <excalidraw_json_path>');
        console.error('Example: node append_png_to_excalidraw.js dog.png ./thumbsub.excalidraw');
        process.exit(1);
    }
    
    try {
        const result = appendPngToExcalidraw(pngFilePath, excalidrawJsonPath);
        console.log('Result:', result);
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}