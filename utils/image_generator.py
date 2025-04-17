import torch
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from dotenv import load_dotenv
import os
from huggingface_hub import login

# Load environment variables
load_dotenv()

# Authenticate with Hugging Face
login(os.getenv("HUGGINGFACE_TOKEN"))

# Load the Stable Diffusion model
model_name = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# Apply efficient scheduler for better results
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

# Move the model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)

def generate_image(prompt):
    """Generate an image using Stable Diffusion model."""
    with torch.autocast(device_type=device):
        # Generate image from the prompt
        #image = pipe(prompt, guidance_scale=10, num_inference_steps=10).images[0]
        image = pipe(prompt, guidance_scale=10, num_inference_steps=10, num_images_per_prompt=2).images[1]

        
    # Save the generated image
    image_path = "generated_image.png"
    image.save(image_path)
    
    return image_path

# Example usage
if __name__ == "__main__":
    prompt = "A futuristic cityscape at sunset, cyberpunk style"
    image_path = generate_image(prompt)
    print(f"Image saved at: {image_path}")
