1. Why is conversation history necessary?
So the LLM can interpret the context of previous prompted questions and respond contextually across multiple turns instead of treating each request as independent.
2. What happens if you remove the system prompt?
The responses will no longer follow the role specified in the system prompt, which may cause the model to give more generic answers instead of behaving like a CS teaching assistant.
3. How does context length affect performance and cost?
More context can lead to more detailed and specific responses, but it also increases token usage, which requires more computation and increases cost.
4. Why is in-memory storage not production safe?
In-memory storage is volatile, so when the application restarts, all stored session data is lost, which results in losing the contextual data for the LLM.
5. What would change if you used a database?
The chat history would be stored persistently, allowing users to resume the same chat as previously used. The LLM could continue responding with contextual data from past conversations even after the server restarts.