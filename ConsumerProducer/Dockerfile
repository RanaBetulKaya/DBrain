# Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ProducerConsumer.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install BeautifulSoup
RUN pip install beautifulsoup4

# Copy the rest of the application code
COPY . .

# Command to run the Kafka producer script
CMD ["python", "ProducerConsumer.py"]
