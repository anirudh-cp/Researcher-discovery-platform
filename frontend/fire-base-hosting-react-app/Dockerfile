# Use an official Node.js runtime as a parent image
FROM node:18 as build

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

ARG REACT_APP_API_URL

ENV REACT_APP_API_URL $REACT_APP_API_URL

# Build the React app
RUN npm run build

# Use an Nginx image to serve the static files
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

# Copy the build files to the Nginx web directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

# # Install serve globally
# RUN npm install -g serve

# # Build production-ready static files
# RUN npm run build

# # Expose port 5000 to the outside world
# EXPOSE 5000

# # Command to run the application with serve
# CMD ["serve", "-s", "build", "-l", "5000"]