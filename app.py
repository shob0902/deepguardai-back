from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import torch
from torchvision import transforms, models
from flask_mail import Mail, Message
import requests
import io
import base64
import os
from diffusers import DiffusionPipeline

app = Flask(__name__, template_folder='templates')
CORS(app)


#Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shouryashobhit1@gmail.com'
app.config['MAIL_PASSWORD'] = 'wlgx vhnm ypwr rtft'
app.config['MAIL_DEFAULT_SENDER'] = 'shouryashobhit1@gmail.com'

mail = Mail(app)

# Stable Diffusion Model Configuration (lazy loading)
pipe = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_stable_diffusion():
    global pipe
    if pipe is None:
        print("Loading Stable Diffusion model...")
        pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", safety_checker=None)
        pipe = pipe.to(device)
        print("Stable Diffusion model loaded!")
    return pipe

#Route to handle contct form
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        msg = Message(
            subject=f"New Collaboration Request from {name}",
            recipients=['shouryashobhit1@gmail.com']
        )

        msg.body = f"""
        New Contact Form Submission

        Name: {name}
        Email: {email}
        Project Brief:
        {message}
        """

        mail.send(msg)

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Route to handle image generation using Stable Diffusion
@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        user_prompt = data.get('prompt')

        if not user_prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Use Stable Diffusion for image generation
        pipe = load_stable_diffusion()
        image = pipe(
            user_prompt,
            height=512,                     # Higher resolution for better quality
            width=512,
            guidance_scale=7.5,
            num_inference_steps=20,         # More steps for better quality
            generator=torch.Generator(device).manual_seed(0)  
        ).images[0]
        
        # Convert PIL image to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        image_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'image': f"data:image/png;base64,{image_base64}"
        })

    except Exception as e:
        return jsonify({'error': f'Stable Diffusion Generation Error: {str(e)}'}), 500

# Load model (with cloud download support)
def load_model():
    model_path = 'best_deepfake_resnet18.pth'
    
    # Download model if not exists (for cloud deployment)
    if not os.path.exists(model_path):
        try:
            print("Downloading model from cloud storage...")
            model_url = os.environ.get('MODEL_URL', 
                'https://github.com/shob0902/Deepfake-Detection-Model/raw/main/best_deepfake_resnet18.pth')
            response = requests.get(model_url, timeout=300)
            with open(model_path, 'wb') as f:
                f.write(response.content)
            print("Model downloaded successfully!")
        except Exception as e:
            print(f"Error downloading model: {e}")
            raise
    
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 2)
    
    checkpoint = torch.load(model_path, map_location="cpu")
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model

# Lazy load model
model = None

def get_model():
    global model
    if model is None:
        print("Loading deepfake detection model...")
        model = load_model()
        print("Deepfake detection model loaded!")
    return model

# Class names
class_names = ['Fake', 'Real']

# Image transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Serve HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Health check endpoint for Render
@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'deepfake-detection'}

# Handle prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    image = Image.open(file.stream).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        model = get_model()
        outputs = model(input_tensor)
        # raw scores (logits)
        logits = outputs.squeeze(0).tolist()
        # probabilities
        probs = torch.nn.functional.softmax(outputs, dim=1).squeeze(0).tolist()
        _, preds = torch.max(outputs, 1)
        predicted_index = preds.item()
        predicted_class = class_names[predicted_index]

    # Return prediction along with logits and probabilities for debugging
    return jsonify({
        'prediction': predicted_class,
        'predicted_index': predicted_index,
        'logits': [float(round(x, 6)) for x in logits],
        'probabilities': [float(round(x, 6)) for x in probs]
    })

if __name__ == '__main__':
    # Production configuration for Render
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print("DeepFake Detection & AI Image Generation Service")
    print("App is ready to receive requests!")
    
    # Start app immediately with minimal startup time
    app.run(debug=False, host='0.0.0.0', port=port)