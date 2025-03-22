import requests
from enum import Enum


class HuggingFaceModel(Enum):
    BART_LARGE_MNLI = "facebook/bart-large-mnli"
    MISTRAL_7B_INSTRUCT = "mistralai/Mistral-7B-Instruct-v0.1"


class HuggingFaceLLM:
    BASE_URL = "https://api-inference.huggingface.co/models/"

    def __init__(self, api_key: str):
        """
        Initialize the Hugging Face LLM client.
        :param api_key: Hugging Face API Key.
        """
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate_response(
        self,
        model: HuggingFaceModel,
        prompt: str,
        max_length: int = 200,
        temperature: float = 0.2,
    ):
        """
        Generate a response from the specified LLM using the provided prompt.
        :param model: The model to use for inference.
        :param prompt: Input text to prompt the model.
        :param max_length: Maximum length of the generated response.
        :param temperature: Sampling temperature for diversity.
        :return: Generated text response.
        """
        url = self.BASE_URL + model.value
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": max_length, "temperature": temperature},
        }

        response = requests.post(url, headers=self.headers, json=payload)

        try:
            response.raise_for_status()
            result = response.json()
            return result[0]["generated_text"] if isinstance(result, list) else result
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"
        except KeyError:
            return f"Unexpected response format: {response.text}"

    def zero_shot_classify(self, model: HuggingFaceModel, text: str, labels: list):
        """
        Perform zero-shot classification on the given text.
        :param model: The model to use for classification.
        :param text: The input text to classify.
        :param labels: A list of candidate labels.
        :return: Classification result with labels and scores.
        """
        url = self.BASE_URL + model.value
        payload = {"inputs": text, "parameters": {"candidate_labels": labels}}

        response = requests.post(url, headers=self.headers, json=payload)

        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"
        except KeyError:
            return f"Unexpected response format: {response.text}"
