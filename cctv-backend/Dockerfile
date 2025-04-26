# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY cctv-backend/package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the app source code
COPY cctv-backend/ .

# Expose the backend port
EXPOSE 5000

# Start the server
CMD ["node", "server.js"]
