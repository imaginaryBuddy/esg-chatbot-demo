FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install packages
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install streamlit==1.31.0

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
# CMD ["streamlit", "run", "app/demo.py"]

EXPOSE 8501


ENTRYPOINT ["streamlit", "run", "app/demo.py", "--server.port=8501", "--server.address=0.0.0.0"]

