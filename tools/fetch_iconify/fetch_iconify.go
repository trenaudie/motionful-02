/*
Package fetch_iconify - Iconify Icon Fetcher Tool

DESCRIPTION:
The Iconify Icon Fetcher is a comprehensive tool for downloading and converting icons from the Iconify
icon library (https://iconify.design) to PNG format. Iconify provides access to over 150,000 open
source icons from various popular icon sets including Material Design Icons, Font Awesome, Feather
Icons, Bootstrap Icons, and many more.

This tool serves as the main entry point for the fetch_iconify functionality, providing both CLI
and programmatic access to icon downloading capabilities. It integrates seamlessly with Motion Canvas
projects by saving icons to the standard assets directory where they can be imported for animations.

FEATURES:
• Comprehensive icon search across 150+ icon libraries
• Automatic SVG to PNG conversion with consistent 256x256 sizing
• Intelligent color normalization (converts currentColor to black)
• Automatic directory creation for output files
• Robust error handling for network and file system operations
• Optimized for Motion Canvas and web development workflows
• Clean, documented API for programmatic usage

USE CASES:
1. Motion Canvas Animation Assets: Download icons for use in programmatic animations
2. Web Development: Batch download icons for UI components and interfaces
3. Prototyping: Quick access to high-quality icons for mockups and prototypes
4. Asset Management: Organize and standardize icon libraries across projects
5. Batch Processing: Script-based icon collection and conversion workflows

ARCHITECTURE:
This tool follows a modular architecture with clear separation of concerns:
- Main Logic (this file): Core application flow and CLI interface
- Utils Package: Reusable functions for API interaction and image processing
- Tool Definitions: CLI wrapper with comprehensive documentation
- Testing: Integration tests validating end-to-end functionality

USAGE EXAMPLES:
CLI Usage:
  go run fetch_iconify.go cat          # Downloads a cat icon
  go run fetch_iconify.go home         # Downloads a home icon  
  go run fetch_iconify.go user-profile # Downloads a user profile icon

Programmatic Usage:
  import "./utils"
  iconName, _ := utils.SearchIcon("cat")
  svgData, _ := utils.DownloadIcon(iconName)
  utils.SvgToPNG(svgData, "output.png", 256, 256)

PARAMETERS:
- query (string): Search term for icon lookup (required)
  Examples: "cat", "home", "user", "settings", "download"

OUTPUT:
- PNG file saved to: ../../public/assets/pngs/<query>.png
- Image dimensions: 256x256 pixels
- Format: PNG with RGBA support for transparency
- Location: Integrated with Motion Canvas asset structure

DEPENDENCIES:
- github.com/srwiley/oksvg: High-quality SVG parsing and rendering
- github.com/srwiley/rasterx: Advanced rasterization engine
- Standard Go libraries: net/http, encoding/json, image/png, path/filepath

INTEGRATION NOTES:
Icons are saved to the public/assets/pngs directory where they can be imported
into Motion Canvas projects using the Img component:

  import catIcon from '/assets/pngs/cat.png';
  const cat = <Img src={catIcon} width={100} height={100} />;

ERROR HANDLING:
- Network connectivity issues with Iconify API
- Invalid or malformed SVG data from external sources
- File system permission errors during PNG creation
- Icon not found scenarios (returns appropriate error messages)
- Malformed icon names or API responses

PERFORMANCE:
- Single API call per icon with optimized query parameters
- Efficient SVG parsing using specialized libraries
- Direct file I/O without intermediate processing steps
- Memory-efficient streaming for large icon downloads
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
		fmt.Println("Usage: go run fetch_iconify.go <query>")
		fmt.Println("Example: go run fetch_iconify.go cat")
		os.Exit(1)
	}

	query := os.Args[1]
	
	// Search for icons matching the query using utils package
	iconName, err := utils.SearchIcon(query)
	if err != nil {
		fmt.Printf("Error searching for icon: %v\n", err)
		os.Exit(1)
	}

	if iconName == "" {
		fmt.Printf("No icon found for query: %s\n", query)
		os.Exit(1)
	}

	// Download the SVG data using utils package
	svgData, err := utils.DownloadIcon(iconName)
	if err != nil {
		fmt.Printf("Error downloading icon: %v\n", err)
		os.Exit(1)
	}

	// Convert SVG to PNG and save using utils package
	outputPath := filepath.Join("../../public/assets/pngs", query+".png")
	err = utils.SvgToPNG(svgData, outputPath, 256, 256)
	if err != nil {
		fmt.Printf("Error converting SVG to PNG: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Successfully downloaded and saved icon for '%s' to %s\n", query, outputPath)
}

