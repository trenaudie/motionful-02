# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Start development server**: `npm start` or `npm run serve`
- **Build project**: `npm run build` (runs TypeScript compilation followed by Vite build)
- **Install dependencies**: `npm install`


## Git Workflow & Development Environment

**Git Worktree Configuration**: See `GIT_WORKTREE_STATUS.md` for complete worktree setup, branch structure, and development workflow guidelines.

### Current Development Setup
- **Main worktree**: Primary Motion Canvas development (main branch)
- **Excalidraw worktree**: `dev-branches/excalidraw/` for Excalidraw tools development (excalidraw-tools branch)

## Tools that you can use 
On top of all the Core tools that you will be defined to you, you may also use the following tools, and view them for the documentation of the tool. 

- **Iconify Icon Fetcher**: Call `tools/fetch_iconify/tool_definitions/fetch_iconify.go` from the project root using go commands to download an SVG from Iconify and convert it to PNG, saving it to `public/assets/pngs/`. This is currently the only option for downloading external assets! So use it if the user wants a static image or SVG from the internet, or if you feel it would be useful for the current Canvas.

- **PNG to Excalidraw Tool**: Call `tools/append_png_to_excalidraw/append_png_to_excalidraw.js` from the project root to append a PNG saved locally to an Excalidraw file. The tool expects PNGs to be in `public/assets/pngs/` directory and can add them to any `.excalidraw` file in the `excalidraw_canvases/` directory.

- **Read** : This is one of the Core tools, but I must insist that you use it before trying the Write or Edit to a file, be it a code file or a json file. 

## Directory Structure

### Key Directories
- `public/assets/pngs/` - Storage location for PNG assets (used by tools and Motion Canvas)
- `excalidraw_canvases/` - Contains Excalidraw diagram files (.excalidraw format)
- `tools/` - Contains utility tools for the project:
  - `tools/fetch_iconify/` - Icon fetching and conversion tool
  - `tools/append_png_to_excalidraw/` - Tool for adding PNGs to Excalidraw files

### Tool Usage Examples
```bash
# Fetch an icon and convert to PNG
cd tools/fetch_iconify && go run tool_definitions/fetch_iconify.go "icon-name"

# Add PNG to Excalidraw file  
cd tools/append_png_to_excalidraw && node append_png_to_excalidraw.js "icon-name.png" "../../excalidraw_canvases/diagram.excalidraw"
``` 


## Guidelines for coding 
- Creates tests and plan before code
- Run one pass of the tests that MUST fail (do not create mock tests)
- The tests must be integrated, not unit tests, so make just one large test per instruction I give you. 
- 
