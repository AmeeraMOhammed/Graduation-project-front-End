import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn

# Define the custom CNN model
class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(64 * 126 * 126, 128)
        self.fc2 = nn.Linear(128, 4)  # Adjust the number of output classes

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2, 2)
        x = torch.flatten(x, 1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load the pretrained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CustomCNN()
model.load_state_dict(torch.load("C:\\Users\\Dell\\Desktop\\facialparalysis\\faciafix\\accounts\\epoch10_mouth.pt", map_location=torch.device('cpu')))
model.to(device)
model.eval()

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
])

# Define the class to index mapping
class_mapping = {
    0: 'Mild mouth paralysis',
    2: 'Moderate mouth paralysis',
    1: 'Moderate severe mouth paralysis',
    3: 'Severe mouth paralysis'
}

def predict_image_mouth(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    return class_mapping[predicted.item()]

# Example usage
# if __name__ == "__main__":
#     image_path = "moderate_eyebrow.jpeg"
#     prediction = predict_image(image_path)
#     print("Predicted class:", prediction)
