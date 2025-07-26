package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

func main() {
	var query string
	var limit int
	var help bool

	flag.StringVar(&query, "query", "", "SVG search query (required)")
	flag.IntVar(&limit, "limit", 3, "Maximum number of SVGs to download (default: 3)")
	flag.BoolVar(&help, "help", false, "Show help message")
	flag.Parse()

	if help {
		fmt.Println("SVG Repo Scraper")
		fmt.Println("Usage: svg-scraper -query <search_term> [-limit <number>]")
		fmt.Println()
		flag.PrintDefaults()
		os.Exit(0)
	}

	if query == "" {
		fmt.Println("Error: query parameter is required")
		fmt.Println("Usage: svg-scraper -query <search_term> [-limit <number>]")
		fmt.Println("Use -help for more information")
		os.Exit(1)
	}

	fmt.Printf("Searching for SVGs with query: %s (limit: %d)\n", query, limit)

	svgContents, err := ScrapeSVG(query, limit)
	if err != nil {
		log.Fatalf("Error scraping SVGs: %v", err)
	}

	if len(svgContents) == 0 {
		fmt.Println("No SVGs found for the given query")
		return
	}

	fmt.Printf("Successfully downloaded %d SVG(s):\n", len(svgContents))
	for i, content := range svgContents {
		fmt.Printf("\n--- SVG %d ---\n", i+1)
		fmt.Println(content)
		fmt.Println("--- End SVG ---")
	}
}