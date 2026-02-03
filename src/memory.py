
from mem0 import Memory

# Mem0 requires configuration, possibly OpenAI key if using their default embedding, 
# or can use local qdrant/embedding.
# For simplicity, we assume default local usage or basic config.
# If Mem0 needs API keys, we hope they are in env or we use a local setup config.

class UserMemory:
    def __init__(self, user_id="default_user", memory_client=None):
        if memory_client:
            self.memory = memory_client
        else:
            config = {
                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "path": "./mem0_storage_v4",
                        "on_disk": True,
                        "embedding_model_dims": 1024,
                    }
                },
                "embedder": {
                    "provider": "huggingface",
                    "config": {
                        "model": "BAAI/bge-m3",
                        "model_kwargs": {"device": "cpu"}
                    }
                },
                "llm": {
                    "provider": "ollama",
                    "config": {
                        "model": "qwen2.5:14b",
                        "temperature": 0.1,
                        "max_tokens": 1500,
                        "ollama_base_url": "http://localhost:11434"
                    }
                }
            }
            self.memory = Memory.from_config(config) if hasattr(Memory, "from_config") else Memory()
            
        self.user_id = user_id

    def add_interaction(self, user_input, system_response):
        # We can store the interaction
        self.memory.add(f"User: {user_input}\nSystem: {system_response}", user_id=self.user_id)

    def get_context(self, query=None):
        """
        Retrieves context. 
        For a reliable 'User Profile' experience, we fetch ALL stored memories for this user
        and inject them. Similarity search often misses facts like 'Name' if the query doesn't match specific keywords.
        """
        try:
            # Fetch all memories (facts/profile) for this user
            results = self.memory.get_all(user_id=self.user_id)
        except Exception as e:
            print(f"Error fetching context: {e}")
            return ""

        if isinstance(results, dict):
            related_memories = results.get("results", [])
        elif isinstance(results, list):
            related_memories = results
        else:
            related_memories = []
            
        if not related_memories:
            return ""
        
        valid_texts = []
        for m in related_memories:
            # Handle standard mem0 dictionary structure
            if isinstance(m, dict):
                # Typically mem0 returns {'memory': 'Fact string', ...} or {'text': ...}
                text = m.get('memory') or m.get('text')
                if text:
                    valid_texts.append(text)
            elif isinstance(m, str):
                valid_texts.append(m)
            # Handle Qdrant objects just in case
            elif hasattr(m, 'payload'):
                valid_texts.append(m.payload.get('memory') or m.payload.get('text', ''))
        
        if not valid_texts:
            return ""

        # Deduplicate and Format
        valid_texts = list(set(valid_texts))
        context_parts = [f"- {t}" for t in valid_texts if t]
        
        return "Thông tin về người dùng (User Memory / Profile):\n" + "\n".join(context_parts)

    def get_all_memories(self):
        """Retrieve all memories for the current user to display in UI"""
        try:
            return self.memory.get_all(user_id=self.user_id)
        except Exception as e:
            print(f"Error fetching memories: {e}")
            return []
