FROM node:12.22.1-buster-slim

WORKDIR /app

# copy over package asap since this barely changes
ADD package.json package.json

# skip dev dependencies
RUN npm install --only=prod

# copy code files
ADD public public
ADD src src