# DeepGuard AI - Backend

Flask-based backend API for DeepGuard AI deepfake detection system.

## Features

- **Deepfake Detection**: ResNet18-based CNN model for image classification
- **Image Generation**: Stable Diffusion integration for synthetic image creation
- **Contact Form**: Email notification system
- **Health Check**: Monitoring endpoint for deployment platforms

## API Endpoints

- `POST /predict` - Upload image for deepfake detection
- `POST /generate-image` - Generate images using Stable Diffusion
- `POST /contact` - Send contact form emails
- `GET /health` - Health check endpoint

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the application:
```bash
python app.py
```

## Environment Variables

- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` - Email configuration
- `MODEL_URL` - URL to download the deepfake detection model
- `PORT` - Application port (default: 5000)

## Deployment

### Docker
```bash
docker build -t deepguard-backend .
docker run -p 5000:5000 deepguard-backend
```

### Render/Heroku
- Connect repository to deployment platform
- Set environment variables in platform settings
- Platform will automatically detect Flask app

## Model

The backend uses a ResNet18 model fine-tuned for deepfake detection. The model is automatically downloaded on first startup.
