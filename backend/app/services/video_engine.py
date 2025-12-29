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

    def execute_and_capture(self, code: str, output_image: str, duration: int):
        """
        Execute Python code and capture the final frame as an image
        """
        import tempfile
        import subprocess
        import time
        
        # Modify code to save the final frame
        modified_code = self._modify_code_for_capture(code, output_image, duration)
        
        # Write to temp file
        code_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        code_file.write(modified_code)
        code_file.close()
        
        try:
            # Execute with timeout
            result = subprocess.run(
                ['python', code_file.name],
                capture_output=True,
                text=True,
                timeout=duration + 5
            )
            
            # Check if image was created
            if not os.path.exists(output_image):
                # If execution failed or no image, create a placeholder
                img = Image.new('RGB', (self.width, self.height), (50, 50, 50))
                draw = ImageDraw.Draw(img)
                draw.text((100, 900), "Execution completed", fill=(255, 255, 255))
                img.save(output_image)
                
        except subprocess.TimeoutExpired:
            # Create timeout image
            img = Image.new('RGB', (self.width, self.height), (50, 50, 50))
            draw = ImageDraw.Draw(img)
            draw.text((100, 900), "Execution timeout", fill=(255, 255, 255))
            img.save(output_image)
        except Exception as e:
            # Create error image
            img = Image.new('RGB', (self.width, self.height), (50, 50, 50))
            draw = ImageDraw.Draw(img)
            draw.text((100, 900), f"Error: {str(e)[:50]}", fill=(255, 255, 255))
            img.save(output_image)
        finally:
            # Cleanup
            if os.path.exists(code_file.name):
                os.remove(code_file.name)
    
    def _modify_code_for_capture(self, code: str, output_image: str, duration: int):
        """
        Modify code to save the final frame
        """
        # Add imports and save logic based on library used
        if 'matplotlib' in code:
            modified = code + f"\n\nimport time\ntime.sleep({duration})\nplt.savefig('{output_image}', dpi=100, bbox_inches='tight')\n"
        elif 'pygame' in code:
            modified = code.replace('pygame.quit()', f"pygame.image.save(screen, '{output_image}')\npygame.quit()")
        elif 'turtle' in code:
            modified = code + f"\n\nimport time\ntime.sleep({duration})\nts = turtle.getscreen()\nts.getcanvas().postscript(file='{output_image}.eps')\n"
        else:
            # Generic: just add a save at the end
            modified = code + f"\n\n# Auto-added: save output\nimport matplotlib.pyplot as plt\nplt.savefig('{output_image}')\n"
        
        return modified

    def create_final_montage(self, typing_video_path: str, result_image_path: str, output_path: str, duration: int):
        """
        Create final video: typing + static result image
        """
        from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
        
        try:
            # Load typing video
            typing_clip = VideoFileClip(typing_video_path)
            
            # Speed up typing (2x faster)
            typing_fast = typing_clip.fx(lambda c: c.speedx(2.0))
            
            # Create clip from result image (show for 5 seconds)
            result_clip = ImageClip(result_image_path).set_duration(5)
            
            # Concatenate
            final = concatenate_videoclips([typing_fast, result_clip])
            
            # Write final video
            final.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,
                logger=None
            )
            
            # Cleanup
            typing_clip.close()
            result_clip.close()
            final.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Erreur lors du montage: {str(e)}")

video_engine = VideoEngine()
