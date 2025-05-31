# Using python3.12-slim
FROM python:3.12-slim

# Install system dependencies including OpenSSH client
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install bitssh
RUN pip install bitssh

# Command to run when container starts
CMD ["bitssh"]
