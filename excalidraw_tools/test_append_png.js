#!/usr/bin/env node

/**
 * Test script for append_png_to_excalidraw functionality
 * This script tests adding a dog PNG to the template.json Excalidraw file
 */

const fs = require('fs');
const path = require('path');
const { appendPngToExcalidraw } = require('./append_png_to_excalidraw');

function runTest() {
    console.log('🧪 Testing append_png_to_excalidraw functionality...\n');
    
    const pngFilePath = 'dog.png'; // Relative to public/assets/pngs
    const templatePath = path.join(__dirname, 'template.json');
    const testOutputPath = path.join(__dirname, 'test-worktree', 'template_with_dog.json');
    
    try {
        // Step 1: Copy template.json to test output location
        console.log('📋 Step 1: Copying template.json to test location...');
        if (!fs.existsSync(templatePath)) {
            throw new Error(`Template file not found: ${templatePath}`);
        }
        
        // Ensure test-worktree directory exists
        const testDir = path.dirname(testOutputPath);
        if (!fs.existsSync(testDir)) {
            fs.mkdirSync(testDir, { recursive: true });
        }
        
        fs.copyFileSync(templatePath, testOutputPath);
        console.log(`✅ Template copied to: ${testOutputPath}\n`);
        
        // Step 2: Read original template to show before state
        console.log('📖 Step 2: Original template content:');
        const originalTemplate = JSON.parse(fs.readFileSync(testOutputPath, 'utf8'));
        console.log(`   Elements count: ${originalTemplate.elements.length}`);
        console.log(`   Files count: ${Object.keys(originalTemplate.files || {}).length}\n`);
        
        // Step 3: Append dog PNG to the template
        console.log('🐕 Step 3: Adding dog PNG to template...');
        const result = appendPngToExcalidraw(pngFilePath, testOutputPath, {
            width: 150,
            height: 150
        });
        
        console.log(`✅ PNG appended successfully!`);
        console.log(`   File ID: ${result.fileId}`);
        console.log(`   Element ID: ${result.elementId}\n`);
        
        // Step 4: Verify the result
        console.log('🔍 Step 4: Verifying updated template...');
        const updatedTemplate = JSON.parse(fs.readFileSync(testOutputPath, 'utf8'));
        console.log(`   Elements count: ${updatedTemplate.elements.length}`);
        console.log(`   Files count: ${Object.keys(updatedTemplate.files || {}).length}`);
        
        // Verify the image element was added
        const imageElements = updatedTemplate.elements.filter(el => el.type === 'image');
        if (imageElements.length === 1) {
            const imageElement = imageElements[0];
            console.log(`✅ Image element verified:`);
            console.log(`   Type: ${imageElement.type}`);
            console.log(`   Width: ${imageElement.width}`);
            console.log(`   Height: ${imageElement.height}`);
            console.log(`   Position: (${imageElement.x}, ${imageElement.y})`);
            console.log(`   File ID: ${imageElement.fileId}\n`);
        } else {
            throw new Error(`Expected 1 image element, found ${imageElements.length}`);
        }
        
        // Verify the file was added
        if (updatedTemplate.files && updatedTemplate.files[result.fileId]) {
            const fileObject = updatedTemplate.files[result.fileId];
            console.log(`✅ File object verified:`);
            console.log(`   MIME type: ${fileObject.mimeType}`);
            console.log(`   Data URL length: ${fileObject.dataURL.length} characters`);
            console.log(`   Created: ${new Date(fileObject.created).toISOString()}\n`);
        } else {
            throw new Error('File object not found in updated template');
        }
        
        console.log('🎉 Test completed successfully!');
        console.log(`📁 Updated template saved to: ${testOutputPath}`);
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        process.exit(1);
    }
}

// Run the test if this script is executed directly
if (require.main === module) {
    runTest();
}

module.exports = { runTest };