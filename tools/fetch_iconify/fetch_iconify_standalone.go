/*
Package main provides a standalone tool for downloading and converting Iconify icons to PNG format.

TOOL: Iconify Icon Fetcher (Standalone)

DESCRIPTION:
This tool searches for icons from the Iconify icon library (https://iconify.design) and downloads them as PNG files.
Iconify provides access to over 150,000 open source icons from various icon sets including Material Design Icons,
Font Awesome, Feather Icons, and many more. The tool performs a search query, finds the best matching icon,
downloads the SVG data, and converts it to a 256x256 PNG file.

FEATURES:
- Search Iconify's extensive icon library with simple text queries
- Automatic SVG to PNG conversion with consistent 256x256 sizing
- Handles color normalization (converts currentColor to black)
- Creates output directories automatically
- Robust error handling for network and file operations
- Optimized for Motion Canvas integration
- Can be run from project root directory

USE CASES:
- Download icons for Motion Canvas animations and presentations
- Batch icon processing for UI/UX projects
- Asset preparation for web applications
- Icon library management and organization
- Quick icon prototyping and testing

USAGE:
CLI: go run tools/fetch_iconify/fetch_iconify_standalone.go <query>
Examples:
  go run tools/fetch_iconify/fetch_iconify_standalone.go cat
  go run tools/fetch_iconify/fetch_iconify_standalone.go home
  go run tools/fetch_iconify/fetch_iconify_standalone.go user-profile

PARAMETERS:
- query (string): Search term for icon lookup (e.g., "cat", "home", "user")

OUTPUT:
- PNG file saved to: public/assets/pngs/<query>.png
- File size: 256x256 pixels
- Format: PNG with transparent background where applicable

DEPENDENCIES:
- github.com/srwiley/oksvg: SVG parsing and rendering
- github.com/srwiley/rasterx: Rasterization engine
- Standard Go libraries: net/http, encoding/json, image/png

ERROR HANDLING:
- Network connectivity issues with Iconify API
- Invalid or malformed SVG data
- File system permission errors
- Icon not found scenarios

INTEGRATION:
This tool integrates with Motion Canvas projects by saving icons to the public/assets/pngs directory
where they can be imported using Motion Canvas's Img component for animations and presentations.
*/

package main

import (
	"encoding/json"
	"fmt"
	"image"
	"image/png"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"github.com/srwiley/oksvg"
	"github.com/srwiley/rasterx"
)

// SearchResult represents the response structure from Iconify's search API
type SearchResult struct {
	Icons []string `json:"icons"`
	Total int      `json:"total"`
}

// SearchIcon searches for icons matching the given query using the Iconify API.
func SearchIcon(query string) (string, error) {
	url := fmt.Sprintf("https://api.iconify.design/search?query=%s&limit=1", query)
	
	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("failed to make search request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("search API returned status %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read search response: %w", err)
	}

	var result SearchResult
	err = json.Unmarshal(body, &result)
	if err != nil {
		return "", fmt.Errorf("failed to parse search response: %w", err)
	}

	if len(result.Icons) == 0 {
		return "", nil // No icon found, but no error
	}

	return result.Icons[0], nil
}

// DownloadIcon downloads SVG data for the specified icon from Iconify.
func DownloadIcon(iconName string) (string, error) {
	// Split icon name to get prefix and icon
	parts := strings.Split(iconName, ":")
	if len(parts) != 2 {
		return "", fmt.Errorf("invalid icon name format: %s (expected prefix:name)", iconName)
	}
	
	prefix := parts[0]
	icon := parts[1]
	
	// Use direct SVG endpoint
	url := fmt.Sprintf("https://api.iconify.design/%s/%s.svg", prefix, icon)
	
	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("failed to download icon: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("icon download returned status %d for %s", resp.StatusCode, iconName)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read icon data: %w", err)
	}

	svgContent := string(body)
	
	// Preprocessing for consistent PNG rendering
	svgContent = strings.ReplaceAll(svgContent, "currentColor", "#000000")
	svgContent = strings.ReplaceAll(svgContent, `width="1em" height="1em"`, `width="256" height="256"`)

	return svgContent, nil
}

// SvgToPNG converts SVG data to PNG format and saves it to the specified path.
func SvgToPNG(svgData, outputPath string, width, height int) error {
	// Ensure output directory exists
	dir := filepath.Dir(outputPath)
	err := os.MkdirAll(dir, 0755)
	if err != nil {
		return fmt.Errorf("failed to create output directory: %w", err)
	}

	// Parse SVG
	svg, err := oksvg.ReadIconStream(strings.NewReader(svgData))
	if err != nil {
		return fmt.Errorf("failed to parse SVG data: %w", err)
	}

	// Create an RGBA image for full transparency support
	img := image.NewRGBA(image.Rect(0, 0, width, height))
	
	// Create scanner and dasher for high-quality rasterization
	scanner := rasterx.NewScannerGV(width, height, img, img.Bounds())
	dasher := rasterx.NewDasher(width, height, scanner)
	
	// Set the raster to use the drawing context
	svg.SetTarget(0, 0, float64(width), float64(height))
	svg.Draw(dasher, 1.0)

	// Save as PNG
	file, err := os.Create(outputPath)
	if err != nil {
		return fmt.Errorf("failed to create output file: %w", err)
	}
	defer file.Close()

	err = png.Encode(file, img)
	if err != nil {
		return fmt.Errorf("failed to encode PNG: %w", err)
	}

	return nil
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run tools/fetch_iconify/fetch_iconify_standalone.go <query>")
		fmt.Println("Example: go run tools/fetch_iconify/fetch_iconify_standalone.go cat")
		os.Exit(1)
	}

	query := os.Args[1]
	
	// Search for the icon
	iconName, err := SearchIcon(query)
	if err != nil {
		fmt.Printf("Error searching for icon: %v\n", err)
		os.Exit(1)
	}

	if iconName == "" {
		fmt.Printf("No icon found for query: %s\n", query)
		os.Exit(1)
	}

	// Download the SVG data
	svgData, err := DownloadIcon(iconName)
	if err != nil {
		fmt.Printf("Error downloading icon: %v\n", err)
		os.Exit(1)
	}

	// Create the output directory if it doesn't exist
	outputDir := "public/assets/pngs"
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		fmt.Printf("Error creating output directory: %v\n", err)
		os.Exit(1)
	}

	// Convert to PNG and save
	outputPath := filepath.Join(outputDir, query+".png")
	err = SvgToPNG(svgData, outputPath, 256, 256)
	if err != nil {
		fmt.Printf("Error converting SVG to PNG: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Successfully downloaded and saved icon for '%s' to %s\n", query, outputPath)
}