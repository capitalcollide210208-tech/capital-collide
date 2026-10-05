from abc import ABC, abstractmethod
from typing import Any, Dict

class VideoProvider(ABC):
    """
    Abstract Base Class for all Video Generation Providers.
    Ensures that Capital Collide is not tightly coupled to any one model.
    """

    @abstractmethod
    def submit_job(self, job_data: Dict[str, Any]) -> str:
        """Submits a shot generation job and returns a job_id."""
        pass

    @abstractmethod
    def get_status(self, job_id: str) -> str:
        """Returns the status of the job (PENDING, RUNNING, PASS, FAILED)."""
        pass

    @abstractmethod
    def get_result(self, job_id: str) -> str:
        """Returns the URL or path to the generated video file."""
        pass

    @abstractmethod
    def retry_shot(self, shot_id: str) -> bool:
        """Retries a failed shot generation."""
        pass

    @abstractmethod
    def cancel_job(self, job_id: str) -> bool:
        """Cancels an active job."""
        pass
