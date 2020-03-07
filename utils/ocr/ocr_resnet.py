from PIL import Image
import numpy
from torchvision import transforms
import torch
import torch.cuda as cuda
from utils.logo.cnn.resnet.resnet import resnet18


def preprocess_image(numpy_array):
    image = Image.fromarray(numpy_array).convert('RGB')
    transform = init_transforms()
    image = transform(image).unsqueeze(0)

    return image


def init_transforms():
    return transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])


def get_letter_from_index(index):
    category_map = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'
                    ]
    return category_map[index]


def predict(image_path):
    image = preprocess_image(image_path)

    net = resnet18()
    net.load_state_dict(torch.load('weights/epoch_3.pth'))
    with torch.no_grad():
        net.eval()
        if cuda.is_available():
            net = net.cuda()
        output = net(image)
        output = numpy.array(output)
        index = numpy.argmax(output)

        predicted = get_letter_from_index(index)
        print(predicted)
        return predicted


