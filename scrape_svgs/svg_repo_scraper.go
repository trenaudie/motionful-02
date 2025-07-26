package main

import (
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"regexp"
	"strings"
	"time"
)

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func ScrapeSVG(query string, limit int) ([]string, error) {
	// Initialize random seed for delays
	rand.Seed(time.Now().UnixNano())
	
	if limit <= 0 {
		limit = 3
	}

	// Try SVGRepo first
	log.Printf("Attempting to fetch SVGs from SVGRepo...")
	svgContents, err := scrapeSVGRepo(query, limit)
	if err != nil {
		log.Printf("SVGRepo failed: %v", err)
		log.Printf("Falling back to alternative sources...")
		
		// Fallback to Heroicons
		return scrapeHeroicons(query, limit)
	}
	
	return svgContents, nil
}

func scrapeSVGRepo(query string, limit int) ([]string, error) {
	url := fmt.Sprintf("https://www.svgrepo.com/vectors/%s/", query)
	log.Printf("Starting scrapeSVGRepo for query: %s, limit: %d", query, limit)
	log.Printf("Target URL: %s", url)

	// Add random delay to appear more human-like
	delay := time.Duration(rand.Intn(2000)+500) * time.Millisecond
	log.Printf("Adding random delay: %v", delay)
	time.Sleep(delay)

	client := &http.Client{
		Timeout: 30 * time.Second,
	}
	log.Printf("Created HTTP client with 30 second timeout")
	
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Printf("ERROR: Failed to create HTTP request: %v", err)
		return nil, fmt.Errorf("failed to create request: %v", err)
	}
	log.Printf("Created HTTP GET request successfully")

	// Enhanced headers to appear more like a real browser
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
	req.Header.Set("Accept-Language", "en-US,en;q=0.9")
	req.Header.Set("Accept-Encoding", "gzip, deflate, br")
	req.Header.Set("DNT", "1")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Upgrade-Insecure-Requests", "1")
	req.Header.Set("Sec-Fetch-Dest", "document")
	req.Header.Set("Sec-Fetch-Mode", "navigate")
	req.Header.Set("Sec-Fetch-Site", "none")
	req.Header.Set("Sec-Fetch-User", "?1")
	req.Header.Set("Cache-Control", "max-age=0")
	log.Printf("Set browser-like headers for request")

	// Retry logic with exponential backoff
	var resp *http.Response
	maxRetries := 3
	log.Printf("Starting retry loop with max %d attempts", maxRetries)
	
	for attempt := 0; attempt < maxRetries; attempt++ {
		if attempt > 0 {
			backoffDelay := time.Duration(1<<uint(attempt)) * time.Second // 2^attempt seconds
			log.Printf("Retrying request in %v (attempt %d/%d)", backoffDelay, attempt+1, maxRetries)
			time.Sleep(backoffDelay)
		}

		log.Printf("Attempt %d: Making HTTP request to %s", attempt+1, url)
		
		var err error
		resp, err = client.Do(req)
		if err != nil {
			log.Printf("ERROR: Attempt %d failed to fetch SVGs from SVGRepo: %v", attempt+1, err)
			if attempt == maxRetries-1 {
				log.Printf("ERROR: All retry attempts exhausted. Final error: %v", err)
				return nil, fmt.Errorf("failed to fetch page after %d attempts: %v", maxRetries, err)
			}
			continue
		}

		log.Printf("Attempt %d: Received HTTP response with status: %s (%d)", attempt+1, resp.Status, resp.StatusCode)
		
		if resp.StatusCode == http.StatusOK {
			log.Printf("SUCCESS: Got HTTP 200 OK response on attempt %d", attempt+1)
			break
		} else {
			log.Printf("WARNING: Non-200 status code received: %s", resp.Status)
		}

		log.Printf("Attempt %d: SVGRepo returned status: %s", attempt+1, resp.Status)
		resp.Body.Close()

		if attempt == maxRetries-1 {
			log.Printf("ERROR: Final attempt failed with status: %s", resp.Status)
			return nil, fmt.Errorf("SVGRepo returned status: %s after %d attempts", resp.Status, maxRetries)
		}
	}
	defer resp.Body.Close()

	log.Printf("Reading response body...")
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("ERROR: Failed to read response body: %v", err)
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	html := string(body)
	log.Printf("Successfully read response body, length: %d bytes", len(html))

	log.Printf("Parsing HTML for SVG URLs using regex pattern...")
	svgURLRegex := regexp.MustCompile(`src="(https://www\.svgrepo\.com/show/\d+/[^"]+\.svg)"`)
	matches := svgURLRegex.FindAllStringSubmatch(html, limit)
	log.Printf("Found %d SVG URL matches in HTML (limit: %d)", len(matches), limit)

	if len(matches) == 0 {
		log.Printf("WARNING: No SVG URLs found in HTML response")
		log.Printf("HTML content preview (first 500 chars): %s", html[:min(500, len(html))])
	}

	var svgContents []string

	for i, match := range matches {
		log.Printf("Processing match %d of %d", i+1, len(matches))
		
		if len(match) < 2 {
			log.Printf("WARNING: Match %d has insufficient parts, skipping", i+1)
			continue
		}

		svgURL := match[1]
		log.Printf("Attempting to download SVG %d from URL: %s", i+1, svgURL)
		
		svgContent, err := downloadSVG(svgURL)
		
		if err != nil {
			log.Printf("ERROR: Failed to download SVG %d from %s: %v", i+1, svgURL, err)
			continue
		}

		log.Printf("SUCCESS: Downloaded SVG %d, content length: %d bytes", i+1, len(svgContent))
		svgContents = append(svgContents, svgContent)
	}

	log.Printf("Completed scrapeSVGRepo: returning %d SVG contents out of %d found URLs", len(svgContents), len(matches))
	return svgContents, nil
}

func downloadSVG(url string) (string, error) {
	log.Printf("Downloading SVG from URL: %s", url)

	// Add small random delay between individual SVG downloads
	delay := time.Duration(rand.Intn(1000)+200) * time.Millisecond
	time.Sleep(delay)

	client := &http.Client{
		Timeout: 15 * time.Second,
	}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", fmt.Errorf("failed to create request: %v", err)
	}

	// Enhanced headers for SVG downloads
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "image/svg+xml,image/*,*/*;q=0.8")
	req.Header.Set("Accept-Language", "en-US,en;q=0.9")
	req.Header.Set("Accept-Encoding", "gzip, deflate, br")
	req.Header.Set("Referer", "https://www.svgrepo.com/")
	req.Header.Set("DNT", "1")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Sec-Fetch-Dest", "image")
	req.Header.Set("Sec-Fetch-Mode", "no-cors")
	req.Header.Set("Sec-Fetch-Site", "same-origin")

	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to download SVG: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read SVG content: %v", err)
	}

	return strings.TrimSpace(string(body)), nil
}

func scrapeHeroicons(query string, limit int) ([]string, error) {
	log.Printf("Searching Heroicons for query: %s", query)
	
	// Heroicons mapping - common icon names
	heroiconsMap := map[string][]string{
		"star": {"star"},
		"heart": {"heart"},
		"home": {"home"},
		"user": {"user", "user-circle"},
		"search": {"magnifying-glass"},
		"menu": {"bars-3"},
		"close": {"x-mark"},
		"check": {"check", "check-circle"},
		"arrow": {"arrow-right", "arrow-left", "arrow-up", "arrow-down"},
		"plus": {"plus", "plus-circle"},
		"minus": {"minus", "minus-circle"},
		"edit": {"pencil", "pencil-square"},
		"delete": {"trash"},
		"info": {"information-circle", "exclamation-circle"},
		"settings": {"cog-6-tooth", "wrench-screwdriver"},
		"mail": {"envelope", "at-symbol"},
		"phone": {"phone", "device-phone-mobile"},
		"calendar": {"calendar-days", "clock"},
		"folder": {"folder", "folder-open"},
		"download": {"arrow-down-tray", "cloud-arrow-down"},
		"upload": {"arrow-up-tray", "cloud-arrow-up"},
		"lock": {"lock-closed", "lock-open"},
		"eye": {"eye", "eye-slash"},
	}
	
	// Find matching icons
	var iconNames []string
	query = strings.ToLower(query)
	
	if icons, exists := heroiconsMap[query]; exists {
		iconNames = icons
	} else {
		// Search for partial matches
		for key, icons := range heroiconsMap {
			if strings.Contains(key, query) || strings.Contains(query, key) {
				iconNames = append(iconNames, icons...)
			}
		}
	}
	
	if len(iconNames) == 0 {
		return nil, fmt.Errorf("no matching icons found for query: %s", query)
	}
	
	// Limit results
	if len(iconNames) > limit {
		iconNames = iconNames[:limit]
	}
	
	var svgContents []string
	
	for _, iconName := range iconNames {
		// Heroicons are available on GitHub
		url := fmt.Sprintf("https://raw.githubusercontent.com/tailwindlabs/heroicons/master/src/24/outline/%s.svg", iconName)
		
		svgContent, err := downloadSimpleSVG(url)
		if err != nil {
			log.Printf("Failed to download Heroicon %s from %s: %v", iconName, url, err)
			continue
		}
		
		if strings.Contains(svgContent, "<svg") {
			svgContents = append(svgContents, svgContent)
			log.Printf("Successfully downloaded Heroicon: %s", iconName)
		}
	}
	
	if len(svgContents) == 0 {
		return nil, fmt.Errorf("failed to download any Heroicons for query: %s", query)
	}
	
	return svgContents, nil
}

func downloadSimpleSVG(url string) (string, error) {
	log.Printf("Downloading SVG from URL: %s", url)

	client := &http.Client{
		Timeout: 10 * time.Second,
	}
	
	resp, err := client.Get(url)
	if err != nil {
		return "", fmt.Errorf("failed to download SVG: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("server returned status: %s", resp.Status)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read SVG content: %v", err)
	}

	return strings.TrimSpace(string(body)), nil
}
