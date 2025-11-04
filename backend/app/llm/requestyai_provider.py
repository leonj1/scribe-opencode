from .interface import LLMProvider

class RequestYaiProvider(LLMProvider):
    def transcribe_audio(self, audio_path: str) -> str:
        # Implementation to call RequestYAI API
        # This is a placeholder implementation
        return ""