# Use official Python runtime from Apify
FROM apify/actor-python:3.12

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Run the main entry point
CMD ["python", "src/main.py"]
