# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Start development server**: `npm start` or `npm run serve`
- **Build project**: `npm run build` (runs TypeScript compilation followed by Vite build)
- **Install dependencies**: `npm install`

## Project Architecture

This is a Motion Canvas / Excalidraw project for creating programmatic animations. Motion Canvas is a TypeScript library for creating animations using code.

### Key Structure
- `src/project.ts` - Main project configuration file that defines which scenes to include
- `src/scenes/` - Active scene files that are imported into the project
- `example_scenes/` - Collection of example scenes organized into subdirectories:
  - `scenes/` - Basic examples
  - `scenes1/` - Simple scene demonstrations  
  - `scenes2/` - Advanced examples including graphs, snake game, MCP integration
  - `scenes3/` - Feature-specific examples (tweening, transitions, media, LaTeX, etc.)

### Scene Development
- Scenes are TypeScript React components using Motion Canvas's 2D API
- Each scene exports a generator function created with `makeScene2D()`
- Scenes use JSX syntax with Motion Canvas components (Circle, Rect, etc.)
- Animation logic uses generator functions with `yield*` statements
- Common patterns include:
  - `createRef<ComponentType>()` for component references
  - `view.add()` to add components to the scene
  - `all()` for parallel animations
  - Easing functions for smooth transitions

### Configuration
- `vite.config.ts` - Vite configuration with Motion Canvas plugin and FFmpeg support
- `tsconfig.json` - Extends Motion Canvas 2D TypeScript configuration
- `src/motion-canvas.d.ts` - TypeScript type definitions reference

### Example Scene Features
The example_scenes directory demonstrates various Motion Canvas capabilities:
- Basic shapes and animations (circles, rectangles)
- Complex animations with easing and transitions
- Graph visualizations and data plotting
- Snake game implementation
- LaTeX rendering
- Media integration (images, videos)
- Layout systems and positioning
- Node signals and reactive programming
- Logging and debugging techniques

## Guidelines for coding 
- Creates tests and plan before code
- Run one pass of the tests that MUST fail (do not create mock tests)
- The tests must be integrasted, not unit tests, so make just one large test per instruction I give you. 


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

