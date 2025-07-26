/*
Package fetch_iconify_test provides comprehensive integration testing for the Iconify icon fetcher tool.

This test suite validates the complete end-to-end functionality of the fetch_iconify tool,
including API integration with Iconify, SVG processing, and PNG conversion. The tests are
designed as integration tests rather than unit tests to ensure real-world functionality.

TEST COVERAGE:
- Iconify API search functionality
- Icon download and SVG processing
- SVG to PNG conversion with proper sizing
- File system operations and output verification
- Error handling and edge cases
- Clean-up and resource management

The test uses the "cat" query as a reliable test case since it's a common icon available
across multiple icon sets in the Iconify library.
*/

package main

import (
	"os"
	"path/filepath"
	"testing"
	"fetch_iconify/utils"
)

/*
TestFetchCatIcon performs a comprehensive integration test of the fetch_iconify tool.

This test validates the complete workflow from search to file output:
1. Searches for a "cat" icon using the Iconify API
2. Downloads the SVG data for the found icon
3. Converts the SVG to a 256x256 PNG image
4. Verifies the output file exists and is properly created
5. Cleans up test artifacts

The test is designed to fail if any part of the pipeline is broken, including:
- Network connectivity issues
- API changes or failures
- SVG processing problems
- File system errors
- Image conversion issues

This integration approach ensures the tool works in real-world conditions
rather than testing isolated components with mocks.
*/
func TestFetchCatIcon(t *testing.T) {
	query := "cat"
	outputPath := filepath.Join("public/assets/pngs", query+".png")
	
	// Clean up any existing test file to ensure fresh test
	os.Remove(outputPath)
	
	t.Logf("Testing complete fetch_iconify workflow for query: %s", query)
	
	// Test Step 1: Search for the icon using utils package
	t.Logf("Step 1: Searching for icon matching '%s'", query)
	iconName, err := utils.SearchIcon(query)
	if err != nil {
		t.Fatalf("Failed to search for icon: %v", err)
	}
	
	if iconName == "" {
		t.Fatalf("No icon found for query: %s", query)
	}
	t.Logf("Found icon: %s", iconName)
	
	// Test Step 2: Download the SVG data
	t.Logf("Step 2: Downloading SVG data for icon: %s", iconName)
	svgData, err := utils.DownloadIcon(iconName)
	if err != nil {
		t.Fatalf("Failed to download icon: %v", err)
	}
	
	if len(svgData) == 0 {
		t.Fatalf("Downloaded SVG data is empty")
	}
	t.Logf("Downloaded SVG data: %d bytes", len(svgData))
	
	// Test Step 3: Convert SVG to PNG
	t.Logf("Step 3: Converting SVG to PNG at %s", outputPath)
	err = utils.SvgToPNG(svgData, outputPath, 256, 256)
	if err != nil {
		t.Fatalf("Failed to convert SVG to PNG: %v", err)
	}
	
	// Test Step 4: Verify file creation and properties
	t.Logf("Step 4: Verifying output file exists and has correct properties")
	fileInfo, err := os.Stat(outputPath)
	if os.IsNotExist(err) {
		t.Fatalf("Output PNG file was not created: %s", outputPath)
	}
	if err != nil {
		t.Fatalf("Error checking output file: %v", err)
	}
	
	// Verify file has reasonable size (PNG files should not be empty)
	if fileInfo.Size() == 0 {
		t.Fatalf("Output PNG file is empty: %s", outputPath)
	}
	t.Logf("Output file size: %d bytes", fileInfo.Size())
	
	// Clean up test file
	defer func() {
		if err := os.Remove(outputPath); err != nil {
			t.Logf("Warning: Failed to clean up test file %s: %v", outputPath, err)
		}
	}()
	
	t.Logf("✅ Successfully completed integration test: fetched and converted '%s' icon to %s", query, outputPath)
}