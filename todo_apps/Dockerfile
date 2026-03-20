#official python image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy remaining project filess
COPY . .

# Install dependencies
RUN pip install fastapi uvicorn sqlalchemy pymysql

# Expose API Port
EXPOSE 8000

# Command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]