"""
Model router module for ABSA pipeline
Routes text to appropriate model based on language
"""

import logging
from typing import Optional, Dict


class ModelRouter:
    """Route input to appropriate model"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize model router
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("ModelRouter")
        
        self.model_mapping = {
            "arabic": {
                "name": "UBC-NLP/MARBERT",
                "type": "marbert",
                "task": "text-classification",
                "description": "MARBERT for Arabic NLP tasks"
            },
            "multilingual": {
                "name": "xlm-roberta-base",
                "type": "xlm-r",
                "task": "text-classification",
                "description": "XLM-RoBERTa for multilingual tasks"
            }
        }
        
        self.loaded_models: Dict = {}
    
    def get_model_config(self, route: str) -> Dict:
        """
        Get model configuration for route
        
        Args:
            route: Route identifier (arabic, multilingual)
            
        Returns:
            Model configuration
        """
        if route not in self.model_mapping:
            self.logger.warning(f"Unknown route: {route}, using multilingual")
            route = "multilingual"
        
        return self.model_mapping[route]
    
    def route(self, language_code: str) -> str:
        """
        Route based on language
        
        Args:
            language_code: Language code
            
        Returns:
            Route identifier
        """
        if language_code.lower() in ["ar", "arabic"]:
            self.logger.debug(f"Routing {language_code} to arabic model")
            return "arabic"
        else:
            self.logger.debug(f"Routing {language_code} to multilingual model")
            return "multilingual"
    
    def load_model(self, route: str, device: str = "cpu"):
        """
        Load model for route
        
        Args:
            route: Route identifier
            device: Device to load model on (cpu, cuda, mps)
            
        Returns:
            Model and tokenizer tuple
        """
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            
            if route in self.loaded_models:
                self.logger.debug(f"Model already loaded for route: {route}")
                return self.loaded_models[route]
            
            config = self.get_model_config(route)
            model_name = config["name"]
            
            self.logger.info(f"Loading model: {model_name} for route: {route}")
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load model
            model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=3,  # positive, neutral, negative
                ignore_mismatched_sizes=True
            )
            
            # Move to device
            model = model.to(device)
            model.eval()
            
            # Cache the model
            self.loaded_models[route] = (model, tokenizer)
            
            self.logger.info(f"Successfully loaded {route} model")
            return model, tokenizer
            
        except Exception as e:
            self.logger.error(f"Error loading model for route {route}: {e}")
            raise
    
    def unload_model(self, route: str):
        """
        Unload model to free memory
        
        Args:
            route: Route identifier
        """
        if route in self.loaded_models:
            del self.loaded_models[route]
            self.logger.info(f"Unloaded model for route: {route}")
    
    def clear_cache(self):
        """Clear all cached models"""
        self.loaded_models.clear()
        self.logger.info("Cleared all cached models")
    
    def get_available_routes(self) -> list:
        """
        Get available routes
        
        Returns:
            List of route identifiers
        """
        return list(self.model_mapping.keys())
    
    def get_model_info(self, route: str) -> str:
        """
        Get human-readable model info
        
        Args:
            route: Route identifier
            
        Returns:
            Model information string
        """
        config = self.get_model_config(route)
        return f"{route.upper()}: {config['description']} ({config['name']})"
