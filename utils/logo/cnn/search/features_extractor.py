import torch


def extract_embedding(model, preprocessors, img):
    """Extracts embedding from input image
        Args:
            model - network model
            preprocessors - input tensor preprocessors
            img - input image
        Returns:
            feat - features vector
    """
    var = preprocessors(img).unsqueeze(0)
    with torch.no_grad():
        features_vector = model.flatten_features(var)

    return features_vector
