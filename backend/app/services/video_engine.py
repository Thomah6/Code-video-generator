import os
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, ColorClip
import numpy as np

class VideoEngine:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.fps = 30
        self.bg_color = (30, 30, 30)
        self.text_color = (212, 212, 212)
        self.font_size = 32
        # Default font for Windows
        self.font_path = "consola.ttf" 

    def create_typing_frames(self, code: str, output_dir: str):
        lines = code.split('\n')
        current_text = ""
        frame_idx = 0
        char_count = 0
        
        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except:
            font = ImageFont.load_default()

        for line in lines:
            for char in line:
                current_text += char
                char_count += 1
                
                # Only create a frame every 5 characters to speed up
                if char_count % 5 != 0:
                    continue
                
                # Create image
                img = Image.new('RGB', (self.width, self.height), self.bg_color)
                draw = ImageDraw.Draw(img)
                
                # Render text
                y = 100
                for l in current_text.split('\n'):
                    draw.text((50, y), l, font=font, fill=self.text_color)
                    y += self.font_size + 10
                
                # Save frame
                img.save(f"{output_dir}/frame_{frame_idx:05d}.png")
                frame_idx += 1
            current_text += "\n"
            
            # Always create a frame at end of line
            img = Image.new('RGB', (self.width, self.height), self.bg_color)
            draw = ImageDraw.Draw(img)
            y = 100
            for l in current_text.split('\n'):
                draw.text((50, y), l, font=font, fill=self.text_color)
                y += self.font_size + 10
            img.save(f"{output_dir}/frame_{frame_idx:05d}.png")
            frame_idx += 1

    def assemble_video(self, frames_dir: str, output_path: str):
        """Assemble frames into video using MoviePy (no system FFmpeg needed)"""
        from moviepy.editor import ImageSequenceClip
        import glob
        
        # Get all frame files sorted
        frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
        
        if not frame_files:
            raise Exception("No frames found to assemble")
        
        # Create video from image sequence
        clip = ImageSequenceClip(frame_files, fps=self.fps)
        clip.write_videofile(output_path, codec='libx264', audio=False, logger=None)
        clip.close()

    def create_final_montage(self, typing_video_path: str, concept_title: str, output_path: str, duration: int):
        """
        For now, just copy the typing video as final output
        (Intro/outro with text requires ImageMagick which isn't installed)
        """
        import shutil
        
        try:
            # Simply copy the typing video as the final output
            shutil.copy2(typing_video_path, output_path)
            return output_path
            
        except Exception as e:
            raise Exception(f"Erreur lors du montage: {str(e)}")

video_engine = VideoEngine()
