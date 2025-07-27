#!/usr/bin/env python3
"""
GitHub Search API Tool

This tool provides functionality to search GitHub repositories and files
using the GitHub REST API v4.

Usage:
    python search_api.py "search query" [--token YOUR_TOKEN]
    
Environment Variables:
    GITHUB_TOKEN: Your GitHub personal access token (optional but recommended)
"""

import os
import sys
import argparse
import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from urllib.parse import quote


@dataclass
class SearchResult:
    """Represents a single search result from GitHub"""
    name: str
    path: str
    repository: str
    url: str
    html_url: str
    score: float
    content_snippet: Optional[str] = None


@dataclass
class RepositoryInfo:
    """Repository information"""
    name: str
    full_name: str
    owner: str
    description: Optional[str]
    stars: int
    language: Optional[str]
    url: str


class GitHubSearchAPI:
    """GitHub Search API client"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub API client
        
        Args:
            token: GitHub personal access token (optional but recommended)
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.session = requests.Session()
        
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            self.session.headers.update({
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def search_code(self, query: str, language: Optional[str] = None, 
                   repo: Optional[str] = None, per_page: int = 30) -> List[SearchResult]:
        """
        Search for code on GitHub
        
        Args:
            query: Search query string
            language: Filter by programming language
            repo: Filter by repository (format: owner/repo)
            per_page: Number of results per page (max 100)
            
        Returns:
            List of SearchResult objects
        """
        search_query = query
        
        if language:
            search_query += f" language:{language}"
        if repo:
            search_query += f" repo:{repo}"
            
        url = f"{self.BASE_URL}/search/code"
        params = {
            'q': search_query,
            'per_page': min(per_page, 100)
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                result = SearchResult(
                    name=item['name'],
                    path=item['path'],
                    repository=item['repository']['full_name'],
                    url=item['url'],
                    html_url=item['html_url'],
                    score=item['score']
                )
                results.append(result)
                
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching code: {e}")
            return []
    
    def search_repositories(self, query: str, language: Optional[str] = None,
                          sort: str = "stars", per_page: int = 30) -> List[RepositoryInfo]:
        """
        Search for repositories on GitHub
        
        Args:
            query: Search query string
            language: Filter by programming language
            sort: Sort by 'stars', 'forks', 'help-wanted-issues', 'updated'
            per_page: Number of results per page (max 100)
            
        Returns:
            List of RepositoryInfo objects
        """
        search_query = query
        
        if language:
            search_query += f" language:{language}"
            
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            'q': search_query,
            'sort': sort,
            'per_page': min(per_page, 100)
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                repo = RepositoryInfo(
                    name=item['name'],
                    full_name=item['full_name'],
                    owner=item['owner']['login'],
                    description=item.get('description'),
                    stars=item['stargazers_count'],
                    language=item.get('language'),
                    url=item['html_url']
                )
                results.append(repo)
                
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching repositories: {e}")
            return []
    
    def get_file_content(self, owner: str, repo: str, path: str) -> Optional[str]:
        """
        Get the content of a specific file from a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path in the repository
            
        Returns:
            File content as string, or None if not found
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('encoding') == 'base64':
                import base64
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            else:
                return data.get('content', '')
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching file content: {e}")
            return None
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        Get current rate limit status
        
        Returns:
            Dictionary with rate limit information
        """
        url = f"{self.BASE_URL}/rate_limit"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting rate limit: {e}")
            return {}


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Search GitHub using the API')
    parser.add_argument('query', help='Search query string')
    parser.add_argument('--token', help='GitHub personal access token')
    parser.add_argument('--language', help='Filter by programming language')
    parser.add_argument('--repo', help='Filter by repository (owner/repo)')
    parser.add_argument('--type', choices=['code', 'repositories'], default='code',
                       help='Search type: code or repositories')
    parser.add_argument('--per-page', type=int, default=10, 
                       help='Number of results per page (max 100)')
    parser.add_argument('--get-content', action='store_true',
                       help='Fetch content for code search results')
    parser.add_argument('--output', help='Save results to JSON file')
    
    args = parser.parse_args()
    
    # Initialize API client
    api = GitHubSearchAPI(token=args.token)
    
    # Prepare data for JSON output
    output_data = {
        'query': args.query,
        'search_type': args.type,
        'language': args.language,
        'repo': args.repo,
        'results': []
    }
    
    if args.type == 'code':
        print(f"Searching for code: {args.query}")
        results = api.search_code(
            query=args.query,
            language=args.language,
            repo=args.repo,
            per_page=args.per_page
        )
        
        print(f"\nFound {len(results)} results:")
        print("-" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.name}")
            print(f"   Repository: {result.repository}")
            print(f"   Path: {result.path}")
            print(f"   URL: {result.html_url}")
            print(f"   Score: {result.score:.2f}")
            
            # Convert result to dict for JSON output
            result_dict = asdict(result)
            
            if args.get_content:
                owner, repo = result.repository.split('/')
                content = api.get_file_content(owner, repo, result.path)
                if content:
                    lines = content.split('\n')
                    preview = '\n'.join(lines[:10])
                    print(f"   Content preview:\n{preview}")
                    if len(lines) > 10:
                        print(f"   ... ({len(lines) - 10} more lines)")
                    result_dict['content'] = content
            
            output_data['results'].append(result_dict)
            print("-" * 80)
    
    elif args.type == 'repositories':
        print(f"Searching for repositories: {args.query}")
        results = api.search_repositories(
            query=args.query,
            language=args.language,
            per_page=args.per_page
        )
        
        print(f"\nFound {len(results)} results:")
        print("-" * 80)
        
        for i, repo in enumerate(results, 1):
            print(f"{i}. {repo.full_name}")
            print(f"   Description: {repo.description or 'No description'}")
            print(f"   Language: {repo.language or 'N/A'}")
            print(f"   Stars: {repo.stars}")
            print(f"   URL: {repo.url}")
            
            # Convert repo to dict for JSON output
            output_data['results'].append(asdict(repo))
            print("-" * 80)
    
    # Show rate limit infoc
    rate_limit = api.get_rate_limit()
    if rate_limit:
        core = rate_limit.get('resources', {}).get('core', {})
        search = rate_limit.get('resources', {}).get('search', {})
        print(f"\nRate Limits:")
        print(f"  Core API: {core.get('remaining', 0)}/{core.get('limit', 0)} remaining")
        print(f"  Search API: {search.get('remaining', 0)}/{search.get('limit', 0)} remaining")
        
        # Add rate limit to output data
        output_data['rate_limits'] = {
            'core': core,
            'search': search
        }
    
    # Save to JSON file if specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"Error saving to file: {e}")


if __name__ == "__main__":
    # python search_api.py "graph motion canvas" --language TypeScript --per-page 5     
    main()