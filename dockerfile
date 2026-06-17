# Use a lightweight official Python runtime with OpenCV dependencies pre-installed or supported
FROM python:3.11-slim

# Install system dependencies required by OpenCV and PyMuPDF
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that your future Streamlit dashboard or FastAPI app will run on
EXPOSE 8501

# Default command to run your policy parser first to ensure configurations exist
CMD ["python", "src/policy_parser.py"]