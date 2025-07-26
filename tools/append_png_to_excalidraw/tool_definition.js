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
const path = require('path');
const {appendPngToExcalidraw} = require('./tool_definition');

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