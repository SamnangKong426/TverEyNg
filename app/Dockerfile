FROM ultralytics/ultralytics:latest

RUN apt-get update && apt-get install -y mpg123 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your model and any additional files
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# Command to run when the container starts
CMD ["streamlit", "run", "main.py"]