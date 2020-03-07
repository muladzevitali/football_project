from torch import nn
from torch.utils import model_zoo
from torchvision.models.resnet import (ResNet, Bottleneck, BasicBlock, model_urls)


class Flatten(nn.Module):
    """Flatten input tensor to vector"""

    def __init__(self):
        super(Flatten, self).__init__()

    def forward(self, x):
        return x.view(x.size(0), -1)


class ResNetModule(ResNet):
    """ResNet extension model"""

    def __init__(self, block, layers, channels=3, num_classes=1000):
        super(ResNetModule, self).__init__(block, layers, num_classes=num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.conv1 = nn.Conv2d(channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.flatten = Flatten()

    def features(self, input_tensor):
        """Extracts features from input tensor
          Args:
            input_tensor - input image tensor
          Returns:
            features_tensor - features tensor
        """
        x = self.conv1(input_tensor)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        # Residual layers
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        features_tensor = self.layer4(x)

        return features_tensor

    def pooled_features(self, input_tensor):
        """Extracts features from average pooling layer of input tensor
          Args:
            input_tensor - input image tensor
          Returns:
            features_tensor - features tensor
        """
        x = self.features(input_tensor)
        features_tensor = self.avgpool(x)

        return features_tensor

    def flatten_features(self, input_tensor):
        """Extracts features from average pooling layer of input tensor
          Args:
            input_tensor - input image tensor
          Returns:
            features_tensor - features tensor
        """
        x = self.pooled_features(input_tensor)
        features_tensor = self.flatten(x)

        return features_tensor

    def forward(self, input_tensor):
        x = self.flatten_features(input_tensor)
        output_tensor = self.fc(x)

        return output_tensor


def _init_layers(layers):
    """Sets default values to layers
        Args:
            layers - layers for ResNet module
        Returns:
            default value if layers are not defined
    """
    return [2, 2, 2, 2] if layers is None else layers


def _init_model(core_type=ResNetModule, block=BasicBlock, layers=None,
                model_key='resnet18', pretrained=False, **kwargs):
    """Initializes appropriated model
      Args:
        core_type - type for model core initialization
        block - block for layers initialization
        layers - model layers
        model_key - key for model URL dictionary
        pretrained - flag for trained weights
        kwargs - additional arguments
      Returns:
        model - network model with weights
    """

    model = core_type(block, _init_layers(layers), **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls[model_key]))

    return model


def _init_module(block=BasicBlock, layers=None, model_key='resnet18',
                 pretrained=False, **kwargs):
    """Initializes appropriated model
      Args:
        block - block for layers initialization
        layers - model layers
        pretrained - flag for trained weights
        kwargs - additional arguments
      Returns:
        network model with weights
    """
    return _init_model(core_type=ResNetModule, block=block, layers=layers,
                       model_key=model_key, pretrained=pretrained, **kwargs)


def resnet18(pretrained=False, **kwargs):
    """Constructs a ResNet-18 model.
      Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet data
        kwargs - additional named arguments
      Returns:
        network model width weights
    """
    return _init_module(block=BasicBlock, layers=[2, 2, 2, 2], model_key=resnet18.__name__,
                        pretrained=pretrained, **kwargs)


def resnet34(pretrained=False, **kwargs):
    """Constructs a ResNet-34 model.
      Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet data
        kwargs - additional named arguments
      Returns:
        network model with weights
    """
    return _init_module(block=BasicBlock, layers=[3, 4, 6, 3], model_key=resnet34.__name__,
                        pretrained=pretrained, **kwargs)


def resnet50(pretrained=False, **kwargs):
    """Constructs a ResNet-50 model.
      Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet data
        kwargs - additional named arguments
      Returns:
        network model with weights
    """
    return _init_module(block=Bottleneck, layers=[3, 4, 6, 3], model_key=resnet50.__name__,
                        pretrained=pretrained, **kwargs)


def resnet101(pretrained=False, **kwargs):
    """Constructs a ResNet-101 model.
      Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet data
        kwargs - additional named arguments
      Returns:
        network model with weights
    """
    return _init_module(block=Bottleneck, layers=[3, 4, 23, 3], model_key=resnet101.__name__,
                        pretrained=pretrained, **kwargs)


def resnet152(pretrained=False, **kwargs):
    """Constructs a ResNet-152 model.
      Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet data
        kwargs - additional named arguments
      Returns:
        network model with weights
    """
    return _init_module(block=Bottleneck, layers=[3, 8, 36, 3], model_key=resnet152.__name__,
                        pretrained=pretrained, **kwargs)
