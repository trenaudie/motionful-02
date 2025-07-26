# Motionful-02

This project combines two powerful tools for visual content creation: **Motion Canvas** for programmatic animations and **Excalidraw** for interactive diagrams and drawings.

## Project Overview

### Motion Canvas
Motion Canvas is a TypeScript library for creating animations using code. This allows for precise, reproducible animations that can be version-controlled and easily modified.

### Excalidraw
Excalidraw provides hand-drawn style diagrams and interactive visual content that complements the programmatic animations.

## Key Folders

### 📊 `excalidraw_tool/`
Contains Excalidraw diagrams and related files:
- `.excalidraw` files - Interactive diagrams and drawings
- Supporting tools and configurations for Excalidraw integration

### 📝 `logs/`
Project logs and session recordings for development tracking and debugging.

### 🎬 `example_scenes/`
Motion Canvas animation examples organized by complexity:
- `scenes/` - Basic examples
- `scenes1/` - Simple demonstrations  
- `scenes2/` - Advanced examples including graphs and interactive content
- `scenes3/` - Feature-specific examples (tweening, transitions, media, LaTeX)

## Getting Started

### Motion Canvas Development
```bash
npm install          # Install dependencies
npm start           # Start development server
npm run build       # Build project
```

### Working with Excalidraw
Open `.excalidraw` files directly in the Excalidraw web application or use the provided tools in the `excalidraw/` folder.

## Project Structure
- `src/` - Active Motion Canvas scenes and project configuration
- `public/` - Static assets (images, etc.)
- Various developer tools and configurations support both platforms