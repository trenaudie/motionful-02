/*
Package fetch_iconify provides a tool for downloading and converting Iconify icons to PNG format.

TOOL: Iconify Icon Fetcher

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

USE CASES:
- Download icons for Motion Canvas animations and presentations
- Batch icon processing for UI/UX projects
- Asset preparation for web applications
- Icon library management and organization
- Quick icon prototyping and testing

USAGE:
CLI: go run tool_definitions/fetch_iconify.go <query>
Examples:
  go run tool_definitions/fetch_iconify.go cat
  go run tool_definitions/fetch_iconify.go home
  go run tool_definitions/fetch_iconify.go user-profile

PARAMETERS:
- query (string): Search term for icon lookup (e.g., "cat", "home", "user")

OUTPUT:
- PNG file saved to: ../../public/assets/pngs/<query>.png
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
	"fmt"
	"os"
	"path/filepath"
	"fetch_iconify/utils"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run tool_definitions/fetch_iconify.go <query>")
		fmt.Println("Example: go run tool_definitions/fetch_iconify.go cat")
		os.Exit(1)
	}

	query := os.Args[1]
	
	// Use the main logic from utils
	iconName, err := utils.SearchIcon(query)
	if err != nil {
		fmt.Printf("Error searching for icon: %v\n", err)
		os.Exit(1)
	}

	if iconName == "" {
		fmt.Printf("No icon found for query: %s\n", query)
		os.Exit(1)
	}

	svgData, err := utils.DownloadIcon(iconName)
	if err != nil {
		fmt.Printf("Error downloading icon: %v\n", err)
		os.Exit(1)
	}

	outputPath := filepath.Join("../../../public/assets/pngs", query+".png")
	err = utils.SvgToPNG(svgData, outputPath, 256, 256)
	if err != nil {
		fmt.Printf("Error converting SVG to PNG: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Successfully downloaded and saved icon for '%s' to %s\n", query, outputPath)
}