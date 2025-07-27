# CLAUDE.md - Motion Canvas Development Guide

This file provides Motion Canvas specific guidance for developing animations and scenes in this project.

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

Coding Specific guidelines are in @coder.go
Examples are in the EXAMPLES.md dir

### Guildelines for how to plan out a scene
Follow the following process 
1. Build out a plan. You need to think about the objects to use, how they will be initialized, then relate to each other athe
2. Build out a spec. Your spec must loosely follow the specification in the @motion_canvas_mega_spec.md.
3. Save the plan to the claude_plans dirs using the format scene_<scene_name>_<datetime>.json
4. Code out the scene
