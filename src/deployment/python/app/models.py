
from typing import List, Dict, Any, Optional
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMModel:
    """
    Interface to the underlying language model.
    Supports both API-based models and local models.
    """
    
    def __init__(self, model_name="gpt-3.5-turbo", model_type="mock"):
        """
        Initialize an LLM model.
        
        Args:
            model_name: Name or path of the model to use
            model_type: Type of model to use ("mock", "local", "api")
        """
        self.model_name = model_name
        self.model_type = model_type
        self.model = None
        
        # Initialize the appropriate model based on the type
        if model_type == "local":
            self._init_local_model()
        elif model_type == "api":
            self._init_api_model()
        # "mock" type doesn't need initialization
        
        logger.info(f"Initialized {model_type} model: {model_name}")
    
    def _init_local_model(self):
        """Initialize a local model based on the model name"""
        try:
            # Check if model name contains "llama" to use llama.cpp
            if "llama" in self.model_name.lower():
                from llama_cpp import Llama
                # Initialize llama.cpp model
                self.model = Llama(
                    model_path=self.model_name,
                    n_ctx=2048,  # Context size
                    n_threads=os.cpu_count() or 4  # Use available CPU threads
                )
                logger.info(f"Loaded Llama model from {self.model_name}")
            else:
                # Use Hugging Face Transformers for other models
                from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
                
                # Load the model with appropriate quantization if possible
                model_kwargs = {'device_map': 'auto', 'load_in_8bit': True}
                
                # Initialize the model and tokenizer
                tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                model = AutoModelForCausalLM.from_pretrained(
                    self.model_name, 
                    **model_kwargs
                )
                
                # Create a text generation pipeline
                self.model = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer
                )
                logger.info(f"Loaded Transformers model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading local model {self.model_name}: {str(e)}")
            # Fallback to mock model
            self.model_type = "mock"
    
    def _init_api_model(self):
        """Initialize an API client for remote models"""
        # In a real implementation, this would initialize an API client
        # Example for OpenAI:
        # from openai import OpenAI
        # self.model = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        pass
    
    def generate(self, 
                prompt: str, 
                context: Optional[str] = None, 
                conversation_history: Optional[List[Dict[str, str]]] = None,
                max_tokens: int = 1024) -> str:
        """
        Generate text based on the prompt, context, and conversation history.
        
        Args:
            prompt: The user's query
            context: Retrieved content from RAG
            conversation_history: Previous messages for context
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        # Format the full prompt with context and conversation history
        full_prompt = self._format_prompt(prompt, context, conversation_history)
        
        # Generate based on the model type
        if self.model_type == "local":
            return self._generate_local(full_prompt, max_tokens)
        elif self.model_type == "api":
            return self._generate_api(full_prompt, max_tokens)
        else:
            # Mock response for demonstration purposes
            return self._generate_mock(prompt)
    
    def _generate_local(self, full_prompt: str, max_tokens: int) -> str:
        """Generate text using a local model"""
        try:
            if "llama" in self.model_name.lower():
                # Generate with llama.cpp
                result = self.model(
                    full_prompt,
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                # Extract the generated text
                return result["choices"][0]["text"]
            else:
                # Generate with Hugging Face pipeline
                result = self.model(
                    full_prompt,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    do_sample=True
                )
                # Extract the generated text, skipping the input prompt
                generated_text = result[0]["generated_text"]
                return generated_text[len(full_prompt):].strip()
        except Exception as e:
            logger.error(f"Error generating with local model: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def _generate_api(self, full_prompt: str, max_tokens: int) -> str:
        """Generate text using an API model"""
        # In a real implementation, this would call the actual AI model API
        # Example for OpenAI:
        # response = self.model.chat.completions.create(
        #     model=self.model_name,
        #     messages=[{"role": "user", "content": full_prompt}],
        #     max_tokens=max_tokens
        # )
        # return response.choices[0].message.content
        return "API model response would appear here in a real implementation."
    
    def _generate_mock(self, prompt: str) -> str:
        """Generate a mock response for demonstration purposes"""
        # Simple rule-based mock responses
        lower_prompt = prompt.lower()
        if "rag" in lower_prompt:
            return "RAG (Retrieval Augmented Generation) is a technique that enhances AI generation by first retrieving relevant information from a knowledge base. It helps LLMs provide more factual and contextual responses."
        elif "guardrail" in lower_prompt:
            return "Guardrails are safety mechanisms that ensure AI outputs meet specific criteria like safety, relevance, and quality. They help prevent harmful, off-topic, or low-quality responses."
        elif "kubernetes" in lower_prompt:
            return "Kubernetes is an open-source platform for automating deployment, scaling, and management of containerized applications. It groups containers into logical units for easy management and discovery."
        elif "local model" in lower_prompt or "llama" in lower_prompt:
            return "Local LLMs like Llama can be run directly on your own hardware without requiring API calls to external services. This provides privacy benefits and can reduce operational costs."
        else:
            return f"I understand your query about {prompt[:30]}... Based on the retrieved information and my knowledge, I can provide a comprehensive explanation. [This would be a detailed response in a real implementation]"
    
    def _format_prompt(self, 
                     prompt: str, 
                     context: Optional[str], 
                     conversation_history: Optional[List[Dict[str, str]]]) -> str:
        """Format the complete prompt with all available information"""
        formatted_prompt = ""
        
        # Add conversation history if available
        if conversation_history:
            for message in conversation_history:
                role = message.get("role", "")
                content = message.get("content", "")
                formatted_prompt += f"{role}: {content}\n"
        
        # Add retrieved context if available
        if context:
            formatted_prompt += f"\nRelevant information:\n{context}\n\n"
        
        # Add the current prompt
        formatted_prompt += f"User: {prompt}\nAssistant: "
        
        return formatted_prompt

def get_llm_model(model_name: str = "default", model_type: str = "mock") -> LLMModel:
    """
    Factory function to create LLM model instances
    
    Args:
        model_name: Name or path of the model to use
        model_type: Type of model ("mock", "local", "api")
    
    Returns:
        An initialized LLM model
    """
    # Determine model type from environment if not specified
    if model_type == "default":
        model_type = os.environ.get("LLM_MODEL_TYPE", "mock")
    
    # Determine model name based on type if not specified
    if model_name == "default":
        if model_type == "local":
            model_name = os.environ.get("LOCAL_MODEL_PATH", "TheBloke/Llama-2-7B-GGUF")
        elif model_type == "api":
            model_name = os.environ.get("API_MODEL_NAME", "gpt-3.5-turbo")
        else:
            model_name = "mock-model"
    
    return LLMModel(model_name=model_name, model_type=model_type)
