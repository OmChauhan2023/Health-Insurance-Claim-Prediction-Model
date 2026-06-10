import numpy as np

def generate_ensemble_predictions(predictions_dict, weights_dict):
    """
    Generates a weighted average ensemble prediction.
    
    Args:
        predictions_dict: dict of format {'ModelName': numpy_array_of_predictions}
        weights_dict: dict of format {'ModelName': weight_float}
        
    Returns:
        numpy_array of weighted predictions
    """
    if set(predictions_dict.keys()) != set(weights_dict.keys()):
        raise ValueError("Keys in predictions_dict and weights_dict must match identically.")
        
    final_preds = np.zeros_like(list(predictions_dict.values())[0])
    
    for name in predictions_dict.keys():
        weight = weights_dict[name]
        preds = predictions_dict[name]
        final_preds += preds * weight
        
    return final_preds
