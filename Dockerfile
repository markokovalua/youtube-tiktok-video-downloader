# Use a Python base image
FROM python:3.13-slim

# Set working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Install dependencies
RUN pip install fastapi uvicorn yt-dlp

# Expose port for FastAPI
EXPOSE 8081

# Copy the app code into the container
COPY ./app /app

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
