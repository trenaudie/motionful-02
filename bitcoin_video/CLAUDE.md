
# YouTube News Video Production Process

Complete workflow for creating YouTube news commentary videos from raw news sources (Fox News, CNBC, etc.) with structured storytelling and precise video clipping.

## Directory Structure

```
bitcoin_video/
├── videos_raw/           # Original raw video files
├── transcripts/          # JSON transcript files with timestamps
│   ├── video_1.json     # Tom Lee Fundstrat interview
│   ├── video_2.json     # Samson Mow Bitcoin maximalist interview  
│   ├── video_3.json     # CNBC crypto market coverage
│   └── all_transcripts.json
├── videos_clipped/       # Final clipped video segments
├── prompts/             # Reference prompts for AI assistance
│   ├── prompt_story.md  # Story creation guidelines
│   └── prompt_video_structure.md # Video structure format
├── storyline_script.md   # Complete narrative script
├── video_structure.yaml # Structured timeline with clips
└── CLAUDE.md           # This documentation
```

## Production Workflow

### Step 1: Extract Transcripts
- Use `extract_transcripts.py` to extract transcripts from videos in `videos_raw/`
- Output JSON files with timestamps to `transcripts/` directory
- Each JSON contains: video name, full text, and timestamped segments

### Step 2: Create Storyline Script
Using the content from `prompts/prompt_story.md`:
- Analyze all transcript files to identify key themes and moments
- Create a compelling YouTube news narrative in `storyline_script.md`
- Structure: Hook → Scene Setting → Story Development → Commentary → Closing
- Target runtime: 3-8 minutes
- Focus on connecting dots between different network coverage

**Example workflow:**
```bash
# Read transcripts
transcripts/video_1.json  # Tom Lee million-dollar prediction
transcripts/video_2.json  # Samson Mow bull run analysis
transcripts/video_3.json  # CNBC market coverage

# Output storyline
storyline_script.md  # Complete narrative script with clip references
```

### Step 3: Create Structured Video Timeline
Using the format from `prompts/prompt_video_structure.md`:
- Extract precise timestamps for each referenced moment
- Create YAML structure alternating between commentary and clips
- Output to `video_structure.yaml`

**Structure format:**
```yaml
- type: "commentary"
  text: "Your scripted commentary here"
- type: "clip" 
  source: "video_1.json"
  start: "00:06:24"
  end: "00:06:31"
  summary: "Tom Lee million-dollar prediction"
  visual_relevance: "high"
  filename: "clip_01_tom_lee_million_prediction.mp4"
```

### Step 4: Video Clipping and Production
- Use the `video_structure.yaml` to create clips in `videos_clipped/`
- Naming convention: `clip_XX_<descriptive_name>.mp4`
- Examples from Bitcoin video:
  - `clip_01_tom_lee_million_prediction.mp4`
  - `clip_02_samson_mow_bull_run.mp4`
  - `clip_03_cnbc_tesla_holdings.mp4`

### Step 5: Final Assembly
- Import clipped videos in sequence order
- Record voiceover for commentary sections
- Edit together raw footage clips with commentary
- Add transitions, graphics, and final polish

## Key Guidelines

### Editorial Approach
- Act as news commentator/pundit with original analysis
- Use raw footage only (exclude third-party commentary)
- Prioritize visually compelling moments
- Connect dots that mainstream media misses
- Maintain journalistic skepticism while being engaging

### Technical Requirements
- All timestamps must be precise for clean cuts
- Maintain original audio quality in clips
- Commentary sections recorded separately as voiceover
- Final video typically 6 minutes commentary + 2 minutes raw footage

### File Naming Standards
- Transcripts: `video_X.json` where X is sequential number
- Clips: `clip_XX_<short_description>.mp4` where XX is zero-padded sequence
- Scripts: `storyline_script.md` for narrative, `video_structure.yaml` for timeline

## AI Assistant Integration

This process works optimally with Claude Code for:
1. **Transcript Analysis**: Reading multiple JSON files and identifying key themes
2. **Storyline Creation**: Crafting compelling narratives from raw material  
3. **Timestamp Extraction**: Finding precise moments in transcripts
4. **Structure Generation**: Creating YAML timelines for video editors

The assistant should use TodoWrite for task tracking and follow the structured prompts in the `prompts/` directory for consistent output quality. 
