

FROM python:3.10
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file to the working directory
COPY requirements.txt .
# Install Python dependencies
RUN pip install -r requirements.txt
# Copy the application code to the working directory
COPY . .
# Collect static files
# RUN python manage.py collectstatic --no-input
# Apply database migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]