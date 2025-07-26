# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Start development server**: `npm start` or `npm run serve`
- **Build project**: `npm run build` (runs TypeScript compilation followed by Vite build)
- **Install dependencies**: `npm install`

## Project Architecture

This is a Motion Canvas project for creating programmatic animations. Motion Canvas is a TypeScript library for creating animations using code.

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