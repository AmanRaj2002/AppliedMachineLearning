# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# Note: Ensure 'pytest' and 'pytest-cov' are in your requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary application files
COPY app.py score.py ./
COPY test.py ./

# can use COPY . . to copy everything in the directory instead.
COPY . .

# Expose the port your Flask app runs on (default is usually 5000)
EXPOSE 5000

# Launch the app upon entry
CMD ["python", "app.py"]
