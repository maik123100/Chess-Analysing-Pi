# Base image
FROM ubuntu:20.04 AS testimg

LABEL maintainer="Maik Wesselkock <wesselkock.maik@gmail.com>" \
      Author="Maik Wesselkock"\
      version="1.0" \
      description="Docker image for rasberry pi chess.com analysing service"


# Set up environment
ENV DEBIAN_FRONTEND=noninteractive

# Install test dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3.8-venv cron postgresql && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Default interactive command
CMD ["/bin/bash"]
