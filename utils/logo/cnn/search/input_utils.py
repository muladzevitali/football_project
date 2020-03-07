from torchvision import transforms


def init_transforms():
    """Initializes transformations for network model inputs
        Returns:
            input tensor converter for fast froward call
    """
    return transforms.Compose([transforms.Resize((224, 224)),
                               transforms.ToTensor(),
                               transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                    std=[0.229, 0.224, 0.225])])
