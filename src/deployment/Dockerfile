
# Use a base image with CUDA support for GPU acceleration
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Create a non-root user
RUN groupadd -g 1000 appuser && \
    useradd -m -u 1000 -g appuser appuser

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Set environment variables
ENV MODEL_DIR=/app/models

# Create a directory for models with appropriate permissions
RUN mkdir -p $MODEL_DIR && chown -R appuser:appuser $MODEL_DIR

# Copy the rest of the application
COPY . .

# Switch to the non-root user
USER appuser

# Set default environment variables
ENV LLM_MODEL_TYPE=mock
ENV LOCAL_MODEL_PATH=$MODEL_DIR/llama-2-7b.gguf
ENV PORT=8000

# Download a default model if LLM_MODEL_TYPE is set to local
# This step is optional - you can also mount models as volumes
RUN if [ "$LLM_MODEL_TYPE" = "local" ] && [ ! -f "$LOCAL_MODEL_PATH" ]; then \
    mkdir -p $(dirname $LOCAL_MODEL_PATH) && \
    python3 -c "from huggingface_hub import hf_hub_download; hf_hub_download('TheBloke/Llama-2-7B-GGUF', 'llama-2-7b.Q4_K_M.gguf', local_dir='$MODEL_DIR', local_dir_use_symlinks=False)" && \
    mv $MODEL_DIR/llama-2-7b.Q4_K_M.gguf $LOCAL_MODEL_PATH; \
    fi

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "python.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
