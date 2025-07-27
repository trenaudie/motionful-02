# Git Worktree Configuration Status

**Last Updated**: 2025-07-27

## Current Worktree Setup

### Main Worktree
- **Location**: `/Users/tanguy.renaudie/motionful-02/`
- **Branch**: `main` 
- **Commit**: `2e7f054` - Updated main branch with latest changes
- **Purpose**: Primary development environment for Motion Canvas project

### Development Worktrees

#### Understanding Claude Development
- **Location**: `/home/bits/motionful-02/dev-branches/understanding_claude/`
- **Branch**: `understanding_claude`
- **Commit**: `2e7f054` - Merged main branch content
- **Purpose**: Development branch for understanding Claude Code workflows
- **Key Features**:
  - Claude workflow scenes and animations
  - GitHub search tools
  - Motion Canvas integration examples

#### Excalidraw Tools Development
- **Location**: `/Users/tanguy.renaudie/motionful-02/dev-branches/excalidraw/`
- **Branch**: `excalidraw-tools`
- **Commit**: `9285671` - Add comprehensive test for append_png_to_excalidraw functionality
- **Purpose**: Isolated development of Excalidraw integration tools
- **Key Features**:
  - PNG to Excalidraw conversion utilities
  - Comprehensive test suite
  - Iconify integration via fetch_iconify tool
  - Clean utility function abstraction

## Branch Structure

```
main (2e7f054)
├── understanding_claude (2e7f054)
│   └── [Claude Code workflow development]
└── excalidraw-tools (9285671)
    └── [Feature development for Excalidraw tools]
```

## Workflow Guidelines

### For Understanding Claude Development
1. **Work in**: `/home/bits/motionful-02/dev-branches/understanding_claude/`
2. **Commit changes**: One feature at a time in understanding_claude branch
3. **Test changes**: Use Motion Canvas development server
4. **Switch contexts**: No need to stash - use separate directories

### For Excalidraw Development
1. **Work in**: `/Users/tanguy.renaudie/motionful-02/dev-branches/excalidraw/`
2. **Commit changes**: One feature at a time in excalidraw-tools branch
3. **Test changes**: Use `test_append_png.js` for validation
4. **Switch contexts**: No need to stash - use separate directories

### For Main Development  
1. **Work in**: `/Users/tanguy.renaudie/motionful-02/`
2. **Stay on**: `main` branch for general Motion Canvas work
3. **Merge features**: When feature branches are ready

## Available Commands

```bash
# List all worktrees
git worktree list

# Switch to understanding claude development
cd dev-branches/understanding_claude

# Switch to excalidraw development
cd dev-branches/excalidraw

# Return to main development
cd /Users/tanguy.renaudie/motionful-02

# Remove worktree (when done)
git worktree remove dev-branches/excalidraw
git branch -d excalidraw-tools
```

## Files and Structure

### Excalidraw Tools (`dev-branches/excalidraw/excalidraw_tools/`)
- `append_png_to_excalidraw.js` - Main tool with comprehensive documentation
- `test_append_png.js` - Test suite for PNG integration
- `utils/id-generators.js` - ID and random value generators
- `utils/element-factory.js` - Excalidraw element creation utilities
- `png_to_json.js` - PNG to Excalidraw format conversion
- `template.json` - Base Excalidraw template for testing

### Integration Points
- `tools/fetch_iconify/` - Go tool for downloading SVG icons as PNGs
- `public/assets/pngs/` - Generated PNG assets storage

## Merge Strategy

When excalidraw-tools development is complete:
```bash
git checkout main
git merge excalidraw-tools
# Optional: Clean up development branch
git branch -d excalidraw-tools
git worktree remove dev-branches/excalidraw
```