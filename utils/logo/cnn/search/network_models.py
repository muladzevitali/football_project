from utils.logo.cnn.resnet.resnet import (resnet18, resnet34, resnet50, resnet101, resnet152)

# Basic model architecture names
RESNET_18 = resnet18.__name__
RESNET_34 = resnet34.__name__
RESNET_50 = resnet50.__name__
RESNET_101 = resnet101.__name__
RESNET_152 = resnet152.__name__

# Basic model architectures
_BASE_MODELS = {RESNET_18: resnet18,
                RESNET_34: resnet34,
                RESNET_50: resnet50,
                RESNET_101: resnet101,
                RESNET_152: resnet152}


def init_model(model_architecture, pretrained=False):
    """Initializes network model by architecture name
        Args:
            model_architecture - model architecture name
            pretrained - load trained weights
        Returns:
            model - initialized network model
    """
    model_func = _BASE_MODELS.get(model_architecture, resnet18)
    model = model_func(pretrained=pretrained)

    return model
