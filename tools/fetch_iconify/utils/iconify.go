/*
Package utils provides utility functions for the fetch_iconify tool.

This package contains the core functionality for interacting with the Iconify API,
processing SVG data, and converting images to PNG format. These utilities are
designed to be reusable across different interfaces and implementations.
*/

package utils

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

// IconData represents the structure of icon metadata from Iconify API
type IconData struct {
	Body   string `json:"body"`
	Width  int    `json:"width"`
	Height int    `json:"height"`
}

// IconSet represents a collection of icons from Iconify API
type IconSet struct {
	Icons map[string]IconData `json:"icons"`
}

/*
SearchIcon searches for icons matching the given query using the Iconify API.

This function queries the Iconify search endpoint and returns the first matching
icon name. The search is performed against Iconify's comprehensive database of
over 150,000 icons from various icon libraries.

Parameters:
- query: Search term for icon lookup (e.g., "cat", "home", "user")

Returns:
- string: Icon name in format "prefix:name" (e.g., "mdi:cat", "fa:home")
- error: Any error that occurred during the search operation

The function performs a single API call with a limit of 1 result for efficiency.
*/
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

/*
DownloadIcon downloads SVG data for the specified icon from Iconify.

This function takes an icon name (in "prefix:name" format) and downloads the
corresponding SVG data from Iconify's direct SVG endpoint. The function also
performs preprocessing on the SVG to ensure consistent rendering:
- Replaces "currentColor" with "#000000" for PNG conversion
- Normalizes size attributes for consistent 256x256 output

Parameters:
- iconName: Icon identifier in format "prefix:name" (e.g., "mdi:cat")

Returns:
- string: Processed SVG content ready for conversion
- error: Any error that occurred during download or processing

The function validates the icon name format and handles HTTP errors appropriately.
*/
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

/*
SvgToPNG converts SVG data to PNG format and saves it to the specified path.

This function takes SVG content as a string and converts it to a PNG image with
the specified dimensions. It uses the oksvg library for SVG parsing and rasterx
for high-quality rasterization. The function automatically creates any necessary
parent directories for the output file.

Parameters:
- svgData: SVG content as a string
- outputPath: Full path where the PNG file should be saved
- width: Width of the output PNG in pixels
- height: Height of the output PNG in pixels

Returns:
- error: Any error that occurred during conversion or file operations

The function handles directory creation, SVG parsing, image rasterization, and
PNG encoding. It uses RGBA color space for full transparency support.
*/
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