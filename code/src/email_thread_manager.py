import re
from typing import List, Optional, Tuple
from models.email_model import Email
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util

class EmailThreadManager:
    """Manages email threads, detects last unreplied customer emails, and checks for duplicates."""

    def __init__(self):
        self.threads = {}  # {thread_id: List[Email]}
        self.similarity_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def add_email(self, email: Email):
        """Adds an email to its thread based on thread_id."""
        thread_id = email.thread_id
        if thread_id not in self.threads:
            self.threads[thread_id] = []
        self.threads[thread_id].append(email)

    def get_last_unreplied_customer_email(self, thread_id: str) -> Optional[Tuple[Email, List[Email]]]:
        """
        Returns the last unreplied customer email in a thread.
        Also returns past customer emails (excluding the last one) for duplicate detection.
        """
        if thread_id not in self.threads:
            return None, []

        emails = self.threads[thread_id]
        past_customer_emails = []  
        last_unreplied_email = None  

        # Iterate from newest to oldest
        for email in reversed(emails):
            if email.sender_role == "customer":
                if last_unreplied_email is None:
                    # First (newest) customer email found without a later support reply
                    if not any(e.sender_role == "support" for e in emails[emails.index(email) + 1:]):
                        last_unreplied_email = email
                else:
                    # Store older customer emails for duplicate detection
                    past_customer_emails.append(email)

        return last_unreplied_email, past_customer_emails

    def is_duplicate_request(self, new_request_body: str, past_customer_emails: List[Email]) -> bool:
        """Checks if the new email body is a duplicate of a previous customer request."""
        new_request_body = self._preprocess_text(new_request_body)

        for past_email in past_customer_emails:
            past_body = self._preprocess_text(past_email.body)

            # 1. **Exact match (quick check)**
            if new_request_body == past_body:
                return True  

            # 2. **Fuzzy Matching (for minor variations)**
            if fuzz.ratio(new_request_body, past_body) > 90:  # Threshold for similarity
                return True  

            # 3. **Semantic Similarity Matching**
            similarity_score = self._compute_semantic_similarity(new_request_body, past_body)
            if similarity_score > 0.85:  # High similarity threshold
                return True  

        return False  

    def _preprocess_text(self, text: str) -> str:
        """Removes extra spaces, converts to lowercase, and removes special characters."""
        return re.sub(r'\s+', ' ', text.strip().lower()).replace('\n', ' ').replace('\r', ' ')

    def _compute_semantic_similarity(self, text1: str, text2: str) -> float:
        """Computes semantic similarity using Sentence Transformers."""
        embeddings = self.similarity_model.encode([text1, text2], convert_to_tensor=True)
        return util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
