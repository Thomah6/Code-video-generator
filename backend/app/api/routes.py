from fastapi import APIRouter, HTTPException
from app.models.schemas import VideoConfig, JobResponse
from app.services.code_generator import code_generator
from app.services.validator import validator
from app.services.video_engine import video_engine
import uuid
import tempfile
import os
import shutil

router = APIRouter()

@router.post("/generate", response_model=JobResponse)
async def generate_video(config: VideoConfig):
    """Generate a new video"""
    job_id = str(uuid.uuid4())
    temp_dir = None
    
    try:
        # Step 1: Generate concept
        concept = code_generator.generate_concept(config.animation_type)
        
        # Step 2: Generate code
        code = code_generator.generate_code(concept, config.duration)
        
        # Step 3: Validate code
        is_valid_syntax, syntax_error = validator.validate_syntax(code)
        if not is_valid_syntax:
            raise HTTPException(status_code=400, detail=f"Code invalide: {syntax_error}")
        
        is_safe, safety_errors = validator.validate_safety(code)
        if not is_safe:
            raise HTTPException(status_code=400, detail=f"Code non sécurisé: {', '.join(safety_errors)}")
        
        # Step 4: Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix=f"vid_{job_id}_")
        frames_dir = os.path.join(temp_dir, "frames")
        os.makedirs(frames_dir)
        
        # Step 5: Create typing video
        video_engine.create_typing_frames(code, frames_dir)
        typing_video = os.path.join(temp_dir, "typing.mp4")
        video_engine.assemble_video(frames_dir, typing_video)
        
        # Step 6: Create final montage
        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        final_video = os.path.join(output_dir, f"{job_id}.mp4")
        video_engine.create_final_montage(
            typing_video_path=typing_video,
            concept_title=concept['title'],
            output_path=final_video,
            duration=config.duration
        )
        
        # Step 7: Cleanup temp files
        shutil.rmtree(temp_dir)
        
        return JobResponse(
            job_id=job_id,
            status="completed",
            message=f"Vidéo générée: {concept['title']}",
            video_url=f"http://localhost:8000/videos/{job_id}.mp4"
        )
    
    except Exception as e:
        # Cleanup on error
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}
