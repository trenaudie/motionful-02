# Comprehensive Tool Diagram Update Plan

## Overview
This plan outlines the comprehensive update of the `excalidraw_canvases/current.excalidraw` file to create a complete visual representation of all Claude Code tools, including core tools, specialized tools, and MCP (Model Context Protocol) tools.

## Current State Analysis
The current diagram contains:
- **User Input** box (blue) - Entry point
- **Claude CLI** box (green) - Main processing hub  
- **Anthropic API** box (purple) - External API connection
- **Tool Execution** box (red) - Core tool processing
- **TodoWrite** box (orange) - Task planning tool
- Various connecting arrows showing workflow
- Some existing PNG icons

## Proposed Comprehensive Update

### 1. Core Tools Section (Expand existing red section)
**Current**: Tool Execution (Read, Edit, Bash)
**Update to**: Comprehensive core tools representation

#### 1.1 Core File Operations
- **Position**: Below current Tool Execution box
- **Tools to represent**:
  - `Read` - File reading operations
  - `Edit` - Single file editing
  - `MultiEdit` - Batch file editing
  - `Write` - File creation/overwriting
  - `Glob` - Pattern-based file searching
  - `Grep` - Content-based file searching
  - `LS` - Directory listing
- **Icons to fetch**:
  - `file-text` (Read operations)
  - `edit` (Edit operations) 
  - `folder-search` (File operations)
- **Visual Design**:
  - Rectangle with red theme (#c92a2a background)
  - Subdivided sections for different operation types
  - Icons positioned next to relevant sections

#### 1.2 Development Tools  
- **Position**: Adjacent to file operations
- **Tools to represent**:
  - `Bash` - Command execution
  - `NotebookRead`/`NotebookEdit` - Jupyter operations
- **Icons to fetch**:
  - `terminal` (Bash operations)
  - `notebook` (Jupyter operations)
- **Visual Design**:
  - Separate rectangle with dark theme (#1e1e1e)
  - Connected to main tool execution flow

### 2. Specialized Tools Section (New orange section)
**Expansion of current TodoWrite area**

#### 2.1 Task Management Tools
- **Current**: TodoWrite (orange box)
- **Enhancement**: 
  - Keep existing TodoWrite box
  - Add detailed breakdown showing task states
  - Connect to `Task` agent tool
- **Icons to fetch**:
  - `tasks` (Task management)
  - `workflow` (Process management)

#### 2.2 Agent System
- **Position**: Adjacent to TodoWrite
- **Tools to represent**:
  - `Task` - Multi-step agent operations
  - `ExitPlanMode` - Planning workflow control
- **Icons to fetch**:
  - `robot` (Agent operations)
  - `plan` (Planning tools)
- **Visual Design**:
  - Yellow/amber theme (#ffa500)
  - Flowing connections showing agent workflow

### 3. Web & External Tools Section (New purple section)
**Position**: Right side of diagram, parallel to Anthropic API

#### 3.1 Web Operations
- **Tools to represent**:
  - `WebFetch` - URL content retrieval
  - `WebSearch` - Search operations
- **Icons to fetch**:
  - `globe` (Web operations)
  - `search` (Search operations)
- **Visual Design**:
  - Purple theme (#6741d9) matching Anthropic API
  - Connected to external data flow

### 4. MCP Tools Section (New teal section)
**Position**: Separate branch from main Claude CLI, positioned to the left

#### 4.1 IDE Integration Tools
- **Tools to represent**:
  - `mcp__ide__getDiagnostics` - VS Code diagnostics
  - `mcp__ide__executeCode` - Jupyter kernel execution
- **Icons to fetch**:
  - `code` (IDE operations)
  - `diagnostics` (Diagnostic tools)
  - `play-circle` (Code execution)
- **Visual Design**:
  - Teal theme (#0891b2)
  - Distinct visual separation showing MCP protocol
  - Connected via dedicated MCP bridge

#### 4.2 MCP Protocol Indicator
- **Purpose**: Show MCP as separate integration layer
- **Design**: 
  - Bridge-like connector from Claude CLI
  - "MCP Bridge" label
  - Distinctive styling to show protocol boundary

### 5. Visual Enhancements & Layout

#### 5.1 Icon Integration
**Icons to fetch and integrate**:
1. `file-text` - File reading operations
2. `edit` - File editing
3. `folder-search` - File searching  
4. `terminal` - Command line operations
5. `notebook` - Jupyter notebooks
6. `tasks` - Task management
7. `workflow` - Process workflows
8. `robot` - Agent operations
9. `plan` - Planning tools
10. `globe` - Web operations
11. `search` - Search functionality
12. `code` - Code/IDE operations
13. `diagnostics` - System diagnostics
14. `play-circle` - Execution operations
15. `bridge` - MCP protocol bridge

#### 5.2 Layout Structure
```
[User Input] → [Claude CLI] → [Anthropic API]
                     ↓              ↑
              [Core Tool Execution] → Response
                     ↓
              [Task Management]
                     ↓
              [Specialized Tools]

[MCP Bridge] ← [Claude CLI] → [Web Tools]
     ↓
[MCP Tools]
```

#### 5.3 Color Scheme
- **Blue** (#1971c2): User interaction layer
- **Green** (#2f9e44): Core Claude processing  
- **Purple** (#6741d9): External APIs & web
- **Red** (#c92a2a): Core tool execution
- **Orange** (#e67700): Task management & planning
- **Yellow** (#ffa500): Agent operations
- **Teal** (#0891b2): MCP integration layer
- **Dark** (#1e1e1e): System operations

### 6. Connection Flow Updates

#### 6.1 New Arrow Connections
1. **Core Tools** ↔ **Task Management**: Bidirectional workflow
2. **Claude CLI** → **MCP Bridge**: MCP protocol access
3. **MCP Bridge** → **MCP Tools**: MCP tool execution
4. **Claude CLI** → **Web Tools**: External data access
5. **Task Management** → **Agent System**: Advanced workflow control
6. **Specialized Tools** → **Core Tools**: Tool composition

#### 6.2 Data Flow Indicators
- **Request Flow**: Blue arrows (user → system)
- **Processing Flow**: Green arrows (internal processing)
- **External Flow**: Purple arrows (API/web calls)
- **Tool Execution**: Red arrows (tool operations)
- **Task Flow**: Orange arrows (planning/management)
- **MCP Flow**: Teal arrows (protocol operations)

## Implementation Steps

### Phase 1: Icon Collection
1. Fetch all 15 required icons using `tools/fetch_iconify/tool_definitions/fetch_iconify.go`
2. Convert to PNG format in `public/assets/pngs/`
3. Verify icon quality and consistency

### Phase 2: Layout Preparation  
1. Analyze current canvas dimensions and optimal positioning
2. Calculate rectangle positions for new sections
3. Design connection arrow paths
4. Plan text label positioning

### Phase 3: Core Tools Expansion
1. Expand existing Tool Execution section
2. Add new rectangles for file operations
3. Add development tools section
4. Integrate relevant icons
5. Update connecting arrows

### Phase 4: Specialized Tools Section
1. Enhance TodoWrite area
2. Add Agent System components  
3. Create task management visualizations
4. Add workflow connections

### Phase 5: MCP Integration
1. Create MCP Bridge element
2. Add MCP tools section
3. Implement MCP-specific styling
4. Connect to main workflow

### Phase 6: Web Tools Integration
1. Add web operations section
2. Position parallel to external API access
3. Create appropriate connections
4. Add web-specific icons

### Phase 7: Final Polish
1. Optimize arrow routing for clarity
2. Add section labels and descriptions
3. Ensure consistent theming
4. Test visual hierarchy and readability
5. Add legend/key if needed

## Expected Outcome
A comprehensive, visually appealing diagram that:
- Shows all 17+ Claude Code tools with proper categorization
- Illustrates the relationship between core tools, specialized tools, and MCP tools
- Provides clear visual hierarchy and workflow understanding
- Uses consistent color coding and iconography
- Serves as both documentation and architectural overview
- Enables users to understand tool capabilities at a glance

## Technical Implementation Notes
- Use `tools/append_png_to_excalidraw/append_png_to_excalidraw.js` for icon integration
- Maintain Excalidraw format compatibility
- Ensure proper element IDs and positioning
- Preserve existing elements while adding new ones
- Consider canvas scaling for complex diagram

## Timeline Estimate
- **Icon Collection**: 30 minutes
- **Layout Design**: 45 minutes  
- **Core Implementation**: 90 minutes
- **MCP Integration**: 60 minutes
- **Final Polish**: 30 minutes
- **Total**: ~4 hours for complete implementation

This comprehensive update will transform the current basic workflow diagram into a complete architectural overview of Claude Code's tool ecosystem.