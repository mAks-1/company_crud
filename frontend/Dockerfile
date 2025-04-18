FROM node:18

WORKDIR /app

# First copy only package files for better caching
COPY package*.json ./
RUN npm install

# Then copy all other files
COPY . .

# Build the application
RUN npm run build

# Install serve globally
RUN npm install -g serve

# Serve from the correct directory
CMD ["serve", "-s", "build", "-l", "3000"]