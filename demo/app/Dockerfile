FROM ultralytics/ultralytics:latest

WORKDIR /app

# Copy your model and any additional files
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# Command to run when the container starts
CMD ["streamlit", "run", "main.py"]