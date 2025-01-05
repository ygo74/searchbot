from typing import Any, Dict, Iterator, List, Mapping, Optional
import requests  # Assumes you use the requests library for HTTP calls
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk

class KernelMemoryLLM(LLM):
    """A custom LLM that interacts with Microsoft's Kernel Memory Service.

    Example:

        .. code-block:: python

            model = KernelMemoryLLM(api_endpoint="https://your-km-endpoint", api_key="your-api-key")
            result = model.invoke([HumanMessage(content="What is the capital of France?")])
            result = model.batch([[HumanMessage(content="Define photosynthesis")],
                                 [HumanMessage(content="Explain relativity")]])
    """

    api_endpoint: str
    api_key: str
    """Kernel Memory Service endpoint and authentication key."""

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the Kernel Memory Service with a prompt.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating (not supported in this basic example).
            run_manager: Callback manager for the run.
            **kwargs: Additional keyword arguments for API parameters.

        Returns:
            The model output as a string.
        """
        if stop is not None:
            raise ValueError("stop kwargs are not supported.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "question": prompt,
            # Additional parameters can be included as needed, such as temperature, max tokens, etc.
            **kwargs
        }

        response = requests.post(f"{self.api_endpoint}/ask", json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print(response.json())
        output = response.json().get("output", "")

        return output

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream results from the Kernel Memory Service.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating (not supported in this example).
            run_manager: Callback manager for the run.
            **kwargs: Additional keyword arguments for API parameters.

        Returns:
            An iterator of GenerationChunks.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "question": prompt,
            # Additional parameters for streaming if supported
            **kwargs
        }

        with requests.post(f"{self.api_endpoint}/ask", json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = GenerationChunk(text=line.decode("utf-8"))
                    if run_manager:
                        run_manager.on_llm_new_token(chunk.text, chunk=chunk)
                    yield chunk

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            "model_name": "KernelMemoryLLM",
            "api_endpoint": self.api_endpoint
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this LLM."""
        return "kernel_memory"


# ---------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------
model = KernelMemoryLLM(api_endpoint="http://localhost:9001", api_key="")
# result = model.invoke("quel est l'ordre des voeux pour les professeurs stagiaires du second degré si on suit le tableau des extensions et que je demande l'académie de lyon? Il faut trouver la première colonne qui commence par Lyon. Peux tu me donner la liste sous forme de bullet points?",index="impots")
result = model.invoke("Peux tu me faire un résumé des mutations interacadémiques des professeurs stagiaires du second degré",index="impots")
print(result)
