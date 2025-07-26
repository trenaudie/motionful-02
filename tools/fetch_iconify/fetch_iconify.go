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

type SearchResult struct {
	Icons []string `json:"icons"`
	Total int      `json:"total"`
}

type IconData struct {
	Body   string `json:"body"`
	Width  int    `json:"width"`
	Height int    `json:"height"`
}

type IconSet struct {
	Icons map[string]IconData `json:"icons"`
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run fetch_iconify.go <query>")
		os.Exit(1)
	}

	query := os.Args[1]
	
	// Search for icons matching the query
	iconName, err := searchIcon(query)
	if err != nil {
		fmt.Printf("Error searching for icon: %v\n", err)
		os.Exit(1)
	}

	if iconName == "" {
		fmt.Printf("No icon found for query: %s\n", query)
		os.Exit(1)
	}

	// Download the SVG data
	svgData, err := downloadIcon(iconName)
	if err != nil {
		fmt.Printf("Error downloading icon: %v\n", err)
		os.Exit(1)
	}

	// Convert SVG to PNG and save
	outputPath := filepath.Join("../../public/assets/pngs", query+".png")
	err = svgToPNG(svgData, outputPath, 256, 256)
	if err != nil {
		fmt.Printf("Error converting SVG to PNG: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Successfully downloaded and saved icon for '%s' to %s\n", query, outputPath)
}

func searchIcon(query string) (string, error) {
	url := fmt.Sprintf("https://api.iconify.design/search?query=%s&limit=1", query)
	
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	var result SearchResult
	err = json.Unmarshal(body, &result)
	if err != nil {
		return "", err
	}

	if len(result.Icons) == 0 {
		return "", nil
	}

	return result.Icons[0], nil
}

func downloadIcon(iconName string) (string, error) {
	// Split icon name to get prefix and icon
	parts := strings.Split(iconName, ":")
	if len(parts) != 2 {
		return "", fmt.Errorf("invalid icon name format: %s", iconName)
	}
	
	prefix := parts[0]
	icon := parts[1]
	
	// Use direct SVG endpoint
	url := fmt.Sprintf("https://api.iconify.design/%s/%s.svg", prefix, icon)
	
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	svgContent := string(body)
	// Replace currentColor with black for PNG rendering
	svgContent = strings.ReplaceAll(svgContent, "currentColor", "#000000")
	// Replace em units with pixels for proper sizing
	svgContent = strings.ReplaceAll(svgContent, `width="1em" height="1em"`, `width="256" height="256"`)

	return svgContent, nil
}

func svgToPNG(svgData, outputPath string, width, height int) error {
	// Ensure output directory exists
	dir := filepath.Dir(outputPath)
	err := os.MkdirAll(dir, 0755)
	if err != nil {
		return err
	}

	// Parse SVG
	svg, err := oksvg.ReadIconStream(strings.NewReader(svgData))
	if err != nil {
		return err
	}

	// Create an image
	img := image.NewRGBA(image.Rect(0, 0, width, height))
	
	// Create scanner and dasher
	scanner := rasterx.NewScannerGV(width, height, img, img.Bounds())
	dasher := rasterx.NewDasher(width, height, scanner)
	
	// Set the raster to use the drawing context
	svg.SetTarget(0, 0, float64(width), float64(height))
	svg.Draw(dasher, 1.0)

	// Save as PNG
	file, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer file.Close()

	return png.Encode(file, img)
}