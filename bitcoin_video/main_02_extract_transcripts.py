#!/usr/bin/env python3
"""
Extract transcripts with timestamps from videos in videos_raw directory.
Outputs structured JSON files to transcripts directory.
"""

import os
import json
from pathlib import Path
from openai import OpenAI
import tempfile
import subprocess
from dotenv import load_dotenv
load_dotenv("../.env")

def extract_audio_from_video(video_path, audio_path):
    """Extract audio from video file using ffmpeg."""
    try:
        cmd = [
            'ffmpeg', '-i', video_path, 
            '-vn', '-acodec', 'mp3', 
            '-y', audio_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio from {video_path}: {e}")
        return False

def transcribe_audio_with_timestamps(audio_path, client):
    """Transcribe audio file with word-level timestamps using OpenAI Whisper."""
    print(f"Transcribing audio...")
    try:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"]
            )
        print(f"Transcription successful")
        return transcription
    except Exception as e:
        print(f"Error transcribing {audio_path}: {e}")
        return None

def process_transcription(transcription_response, video_name):
    """Process transcription response into structured format."""
    if not transcription_response:
        print(f"No transcription response for {video_name}")
        return None
    
    # Extract segments with timestamps
    segments = []
    if hasattr(transcription_response, 'segments') and transcription_response.segments:
        for segment in transcription_response.segments:
            segments.append({
                "start_time": segment.start,
                "end_time": segment.end,
                "text": segment.text.strip()
            })
        print(f"Extracted {len(segments)} segments")
    
    # Extract word-level timestamps if available
    words = []
    if hasattr(transcription_response, 'words') and transcription_response.words:
        for word in transcription_response.words:
            words.append({
                "word": word.word,
                "start_time": word.start,
                "end_time": word.end
            })
        print(f"Extracted {len(words)} words with timestamps")
    
    full_text = getattr(transcription_response, 'text', '')
    
    return {
        "video_name": video_name,
        "full_text": full_text,
        "segments": segments,
        "words": words
    }

def main():
    """Main function to process all videos in videos_raw directory."""
    # Initialize OpenAI client
    client = OpenAI()
    
    # Set up directories
    videos_raw_dir = Path("videos_raw")
    transcripts_dir = Path("transcripts")
    
    # Ensure transcripts directory exists
    transcripts_dir.mkdir(exist_ok=True)
    
    # Supported video formats
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    
    # Process each video file
    results = {}
    
    # Process all video files
    video_files = [f for f in videos_raw_dir.iterdir() if f.suffix.lower() in video_extensions]
    print(f"Found {len(video_files)} video files to process")
    
    for video_nbr,  video_file in enumerate(video_files):
            
        print(f"Processing {video_file.name}...")
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        
        try:
            # Extract audio from video
            if not extract_audio_from_video(str(video_file), temp_audio_path):
                print(f"Failed to extract audio from {video_file.name}")
                continue
            
            # Transcribe audio with timestamps
            transcription = transcribe_audio_with_timestamps(temp_audio_path, client)
            
            if transcription is None:
                print(f"Failed to transcribe {video_file.name}")
                continue
            
            print(f"Transcription completed for {video_file.name}")
            
            # Process transcription
            processed_data = process_transcription(transcription, video_file.stem)
            
            if processed_data:
                results[video_file.stem] = processed_data
                
                # Save individual transcript file
                output_file = transcripts_dir / f"video_{video_nbr}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, indent=2, ensure_ascii=False)
                
                print(f"Saved transcript to {output_file}")
            
        finally:
            # Clean up temporary audio file
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
    
    # Save combined results
    if results:
        combined_file = transcripts_dir / "all_transcripts.json"
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Saved combined transcripts to {combined_file}")
        print(f"Processed {len(results)} videos successfully")
    else:
        print("No videos were processed successfully")

if __name__ == "__main__":
    main()