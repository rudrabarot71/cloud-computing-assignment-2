Docker Hub Repository Link

Visit the following link to access the Docker Hub repository for the uploaded Docker image

https://hub.docker.com/r/rb715715/cs643_prog_2


Building and Uploading Docker Images

Step 1: Docker Installation

Ensure that Docker is installed on your machine by downloading it from the official Docker website.

Step 2: Create a Dockerfile

Create a Dockerfile in your project's root. Customize it for your application. Here's a simplified example for a Node.js application:
# Use an official Node.js runtime as a base image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy the application code to the container
COPY . .

# Expose a port (replace 3000 with your application's port)
EXPOSE 3000

# Command to run your application
CMD ["npm", "start"]


Step 3: Build the Docker Image
Open a terminal, navigate to the directory with the Dockerfile, and run:
docker build -t your-dockerhub-username/your-image-name:tag .
Replace placeholders with your Docker Hub username, desired image name, and tag.

Step 4: Docker Hub Login
Before pushing the Docker image, log in to your Docker Hub account:
docker login

Step 5: Push the Docker Image to Docker Hub
After logging in, push the Docker image:
docker push your-dockerhub-username/your-image-name:tag

Replace placeholders with your Docker Hub username, desired image name, and tag.

Step 6: Verify on Docker Hub
Open a web browser.

Visit Docker Hub.

Log in to your Docker Hub account.

Navigate to your repository to confirm the successful upload.

Example URL: https://hub.docker.com/r/your-dockerhub-username/your-image-name

Replace placeholders with your Docker Hub username and image name.

On the repository page, verify information about the uploaded Docker image, including its tag (e.g., latest).
