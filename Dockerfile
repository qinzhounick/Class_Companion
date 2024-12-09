# Use a lightweight Python image
FROM python:3.13.0

# Copy the project files into the container
#COPY ./app /app
COPY . /app
COPY /app/API_KEY.txt /app
WORKDIR /app

# Install system-level dependencies for PortAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8080


# Command to run the app with Uvicorn
#CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["sh", "-c", "cd app && uvicorn api:app --host 0.0.0.0 --port 8080"]
