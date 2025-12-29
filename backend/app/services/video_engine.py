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
        """Assemble frames into video using imageio (no system FFmpeg needed)"""
        import imageio
        import glob
        
        # Get all frame files sorted
        frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
        
        if not frame_files:
            raise Exception("No frames found to assemble")
        
        # Read frames and create video
        writer = imageio.get_writer(output_path, fps=self.fps, codec='libx264', pixelformat='yuv420p')
        
        for frame_file in frame_files:
            frame = imageio.imread(frame_file)
            writer.append_data(frame)
        
        writer.close()

    def create_final_montage(self, typing_video_path: str, concept_title: str, output_path: str, duration: int):
        """
        Create final video with intro, typing effect, and outro
        """
        try:
            # Load typing video
            typing_clip = VideoFileClip(typing_video_path)
            
            # Speed up typing (2x faster)
            typing_clip = typing_clip.fx(lambda c: c.speedx(2.0))
            
            # Create intro (2 seconds)
            intro_bg = ColorClip(size=(self.width, self.height), color=(103, 58, 183), duration=2)
            intro_text = TextClip(
                concept_title,
                fontsize=70,
                color='white',
                font='Arial-Bold',
                size=(self.width - 100, None),
                method='caption'
            ).set_position('center').set_duration(2)
            intro = CompositeVideoClip([intro_bg, intro_text])
            
            # Create outro (2 seconds)
            outro_bg = ColorClip(size=(self.width, self.height), color=(103, 58, 183), duration=2)
            outro_text = TextClip(
                "Follow pour plus! 🔥",
                fontsize=60,
                color='white',
                font='Arial-Bold'
            ).set_position('center').set_duration(2)
            outro = CompositeVideoClip([outro_bg, outro_text])
            
            # Concatenate all clips
            final = concatenate_videoclips([intro, typing_clip, outro])
            
            # Write final video
            final.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,
                preset='medium'
            )
            
            # Cleanup
            typing_clip.close()
            intro.close()
            outro.close()
            final.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Erreur lors du montage: {str(e)}")

video_engine = VideoEngine()
