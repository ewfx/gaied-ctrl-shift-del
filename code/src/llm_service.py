import requests
from enum import Enum
from time import sleep


class HuggingFaceModel(Enum):
    BART_LARGE_MNLI = "facebook/bart-large-mnli"
    MORITZ_LAURER_DEBERT = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
    MSFT_DEBERTA = "microsoft/deberta-v3-large"
    MISTRAL_7B_INSTRUCT = "mistralai/Mistral-7B-Instruct-v0.1"


class HuggingFaceLLM:
    BASE_URL = "https://api-inference.huggingface.co/models/"

    def __init__(self, api_key: str):
        """
        Initialize the Hugging Face LLM client.
        :param api_key: Hugging Face API Key.
        :raises ValueError: If the API key is not provided.
        """
        if not api_key:
            raise ValueError("API key is required for Hugging Face LLM access.")

        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _request_with_retries(self, url, payload, max_retries=3):
        """
        Make a request with retries in case of transient errors.
        """
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=self.headers, json=payload)
                if response.status_code == 401:  # Handle unauthorized errors
                    raise ValueError("Invalid API key. Authentication failed.")

                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    sleep(2**attempt)  # Exponential backoff
                    continue
                return f"Request failed after {max_retries} attempts: {str(e)}"

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

        response = self._request_with_retries(url, payload)

        if isinstance(response, str):  # Check if response is an error message
            return response

        try:
            result = response.json()
            return result[0]["generated_text"] if isinstance(result, list) else result
        except KeyError:
            return f"Unexpected response format: {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"

    def zero_shot_classify(
        self,
        model: HuggingFaceModel,
        text: str,
        labels: list,
        multi_label: bool = False,
    ):
        """
        Perform zero-shot classification on the given text.
        :param model: The model to use for classification.
        :param text: The input text to classify.
        :param labels: A list of candidate labels.
        :param multi_label: Whether to allow multiple labels to be assigned.
        :return: Classification result with labels and scores, or an error response.
        """
        url = self.BASE_URL + model.value
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": labels, "multi_label": multi_label},
        }

        response = self._request_with_retries(url, payload)

        if isinstance(response, str):  # Request failed after retries
            return {"error": response}

        try:
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except KeyError:
            return {"error": f"Unexpected response format: {response.text}"}
