from fastapi import APIRouter, HTTPException
from app.models.schemas import VideoConfig, JobResponse
from app.services.code_generator import code_generator
from app.services.validator import validator
from app.services.video_engine import video_engine
import uuid
import tempfile
import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", response_model=JobResponse)
async def generate_video(config: VideoConfig):
    """Generate a new video"""
    job_id = str(uuid.uuid4())
    temp_dir = None
    
    logger.info(f"🎬 Starting video generation - Job ID: {job_id}")
    logger.info(f"📋 Config: {config}")
    
    try:
        # Step 1: Generate concept
        logger.info("🤖 Step 1: Generating concept with Groq AI...")
        concept = code_generator.generate_concept(config.animation_type)
        logger.info(f"✅ Concept generated: {concept.get('title', 'Unknown')}")
        
        # Step 2: Generate code
        logger.info("💻 Step 2: Generating Python code...")
        code = code_generator.generate_code(concept, config.duration)
        logger.info(f"✅ Code generated ({len(code)} characters)")
        logger.info(f"📝 Code preview:\n{code[:200]}...")
        
        # Step 3: Validate code
        logger.info("🔍 Step 3: Validating code syntax...")
        is_valid_syntax, syntax_error = validator.validate_syntax(code)
        if not is_valid_syntax:
            logger.error(f"❌ Syntax error: {syntax_error}")
            raise HTTPException(status_code=400, detail=f"Code invalide: {syntax_error}")
        logger.info("✅ Syntax valid")
        
        logger.info("🔒 Step 4: Validating code safety...")
        is_safe, safety_errors = validator.validate_safety(code)
        if not is_safe:
            logger.error(f"❌ Safety errors: {safety_errors}")
            raise HTTPException(status_code=400, detail=f"Code non sécurisé: {', '.join(safety_errors)}")
        logger.info("✅ Code is safe")
        
        # Step 4: Create temporary directory
        logger.info("📁 Step 5: Creating temporary directory...")
        temp_dir = tempfile.mkdtemp(prefix=f"vid_{job_id}_")
        frames_dir = os.path.join(temp_dir, "frames")
        os.makedirs(frames_dir)
        logger.info(f"✅ Temp dir created: {temp_dir}")
        
        # Step 5: Create typing video
        logger.info("⌨️ Step 6: Creating typing effect frames...")
        video_engine.create_typing_frames(code, frames_dir)
        logger.info("✅ Typing frames created")
        
        logger.info("🎞️ Step 7: Assembling typing video with FFmpeg...")
        typing_video = os.path.join(temp_dir, "typing.mp4")
        video_engine.assemble_video(frames_dir, typing_video)
        logger.info("✅ Typing video assembled")
        
        # Step 6: Execute code and capture result
        logger.info("🎮 Step 8: Executing code and capturing result...")
        result_image = os.path.join(temp_dir, "result.png")
        video_engine.execute_and_capture(code, result_image, config.duration)
        logger.info("✅ Code executed and result captured")
        
        # Step 7: Create final montage
        logger.info("🎬 Step 9: Creating final montage...")
        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "videos")
        os.makedirs(output_dir, exist_ok=True)
        
        final_video = os.path.join(output_dir, f"{job_id}.mp4")
        video_engine.create_final_montage(
            typing_video_path=typing_video,
            result_image_path=result_image,
            output_path=final_video,
            duration=config.duration
        )
        logger.info(f"✅ Final video created: {final_video}")
        
        # Step 7: Cleanup temp files
        logger.info("🧹 Step 9: Cleaning up temporary files...")
        shutil.rmtree(temp_dir)
        logger.info("✅ Cleanup complete")
        
        logger.info(f"🎉 Video generation complete! Job ID: {job_id}")
        
        return JobResponse(
            job_id=job_id,
            status="completed",
            message=f"Vidéo générée: {concept['title']}",
            video_url=f"http://localhost:8000/videos/{job_id}.mp4"
        )
    
    except Exception as e:
        logger.error(f"❌ Error during generation: {str(e)}", exc_info=True)
        # Cleanup on error
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "ok"}
