from transformers import VisionEncoderDecoderModel, AutoTokenizer, AutoFeatureExtractor
from PIL import Image
import torch
from .base_agent import BaseAgent

class FormulaExtractionAgent(BaseAgent):
    def __init__(self, model_name="DGurgurov/im2latex", logger=None):
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/swin-base-patch4-window7-224-in22k")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.logger = logger

    def execute(self, document):
        if not hasattr(document, 'image_paths') or not document.image_paths:
            if self.logger:
                self.logger.info("No images found in document for formula extraction.")
            return []

        formula_results = []
        for image_path in document.image_paths:
            try:
                if self.logger:
                    self.logger.info(f"Processing image for formula extraction: {image_path}")

                # Load and preprocess image
                image = Image.open(image_path).convert("RGB")
                pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
                pixel_values = pixel_values.to(self.device)

                # Generate LaTeX code
                generated_ids = self.model.generate(pixel_values)
                latex_code = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)

                formula_results.append(latex_code)

            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error processing image {image_path}: {e}")
                continue

        return formula_results
