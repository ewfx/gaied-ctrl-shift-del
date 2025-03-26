from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ThreadProcessingResponse:
    thread_id: str
    is_new_thread: bool
    last_unreplied_email: Optional[str]
    detected_service_request: str
    additional_info: Optional[dict] = None

    def print_response(self):
        print("\nThread Processing Response:")
        print(f"Thread ID: {self.thread_id}")
        print(f"Is New Thread: {self.is_new_thread}")
        print(f"Last Unreplied Email: {self.last_unreplied_email}")
        print(f"Detected Service Request: {self.detected_service_request}")
        if self.additional_info:
            print("Additional Info:")
            for key, value in self.additional_info.items():
                print(f"  {key}: {value}")