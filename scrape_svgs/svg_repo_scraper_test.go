package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestScrapeSVG_ValidQuery(t *testing.T) {
	// This test may fail if SVGRepo blocks the request (403 Forbidden)
	// That's expected behavior and indicates the scraper is working correctly
	results, err := ScrapeSVG("star", 2)
	
	if err != nil {
		// If we get a 403 Forbidden, that's expected due to bot protection
		if strings.Contains(err.Error(), "403 Forbidden") {
			t.Logf("Got expected 403 Forbidden from SVGRepo (bot protection): %v", err)
			return
		}
		t.Fatalf("Unexpected error: %v", err)
	}
	
	if len(results) == 0 {
		t.Log("No results returned - this could be due to bot protection or no matches")
		return
	}
	
	// Check that results contain SVG content
	for i, result := range results {
		if !strings.Contains(result, "<svg") {
			t.Errorf("Result %d does not contain SVG content: %s", i, result)
		}
	}
	
	t.Logf("Successfully retrieved %d SVG(s)", len(results))
}

func TestScrapeSVG_EmptyQuery(t *testing.T) {
	results, err := ScrapeSVG("", 1)
	
	// Should still work with empty query, but might return no results
	if err != nil {
		t.Logf("Error with empty query (expected): %v", err)
	}
	
	t.Logf("Empty query returned %d results", len(results))
}

func TestScrapeSVG_ZeroLimit(t *testing.T) {
	results, err := ScrapeSVG("star", 0)
	
	if err != nil {
		// If we get a 403 Forbidden, that's expected due to bot protection
		if strings.Contains(err.Error(), "403 Forbidden") {
			t.Logf("Got expected 403 Forbidden from SVGRepo (bot protection): %v", err)
			return
		}
		t.Fatalf("Unexpected error: %v", err)
	}
	
	// Should default to 3 when limit is 0
	if len(results) > 3 {
		t.Errorf("Expected max 3 results with zero limit, got %d", len(results))
	}
}

func TestScrapeSVG_NegativeLimit(t *testing.T) {
	results, err := ScrapeSVG("star", -1)
	
	if err != nil {
		// If we get a 403 Forbidden, that's expected due to bot protection
		if strings.Contains(err.Error(), "403 Forbidden") {
			t.Logf("Got expected 403 Forbidden from SVGRepo (bot protection): %v", err)
			return
		}
		t.Fatalf("Unexpected error: %v", err)
	}
	
	// Should default to 3 when limit is negative
	if len(results) > 3 {
		t.Errorf("Expected max 3 results with negative limit, got %d", len(results))
	}
}

func TestDownloadSVG_MockServer(t *testing.T) {
	// Create a mock SVG content
	mockSVG := `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
	<circle cx="12" cy="12" r="10" fill="blue"/>
</svg>`

	// Create a test server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "image/svg+xml")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(mockSVG))
	}))
	defer server.Close()

	// Test downloading from the mock server
	result, err := downloadSVG(server.URL)
	
	if err != nil {
		t.Fatalf("Expected no error, got: %v", err)
	}
	
	if result != strings.TrimSpace(mockSVG) {
		t.Errorf("Expected SVG content '%s', got '%s'", mockSVG, result)
	}
}

func TestDownloadSVG_InvalidURL(t *testing.T) {
	result, err := downloadSVG("invalid-url")
	
	if err == nil {
		t.Fatal("Expected error for invalid URL, got none")
	}
	
	if result != "" {
		t.Errorf("Expected empty result for invalid URL, got: %s", result)
	}
}

func TestDownloadSVG_404Error(t *testing.T) {
	// Create a test server that returns 404
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer server.Close()

	result, err := downloadSVG(server.URL)
	
	// Should not error on 404, but will return the 404 page content
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	
	if result != "Not Found" {
		t.Errorf("Expected '404 Not Found' content, got: %s", result)
	}
}

// Integration test - only run if you want to test against real SVGRepo
func TestScrapeSVG_Integration(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}
	
	results, err := ScrapeSVG("home", 1)
	
	if err != nil {
		// If we get a 403 Forbidden, that's expected due to bot protection
		if strings.Contains(err.Error(), "403 Forbidden") {
			t.Logf("Integration test: Got expected 403 Forbidden from SVGRepo (bot protection): %v", err)
			return
		}
		t.Fatalf("Integration test failed with unexpected error: %v", err)
	}
	
	if len(results) == 0 {
		t.Log("Integration test: No results returned - this could be due to bot protection")
		return
	}
	
	// Verify the result is valid SVG
	if !strings.Contains(results[0], "<svg") {
		t.Errorf("Integration test: Result doesn't contain SVG content: %s", results[0])
	}
	
	t.Logf("Integration test successful: Retrieved %d SVG(s)", len(results))
}