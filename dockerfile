#Python base image
FROM python:3.10-slim

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

#Expose the port to run flask on(default is 5000)
EXPOSE 5000

#Write the command to run the application
CMD [ "python", "app.py" ]
