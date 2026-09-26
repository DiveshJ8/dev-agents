from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from dev_agents.core.message import Message, MessageRole, ToolCall
from dev_agents.llm.base import BaseLLMProvider, LLMResponse
from dev_agents.tools.base import BaseTool


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider using the modern `google-genai` SDK."""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.2,
        api_key: Optional[str] = None,
    ):
        super().__init__(model_name=model_name, temperature=temperature)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it in your environment, .env file, "
                "or pass api_key directly to GeminiProvider."
            )
        from google import genai
        self.client = genai.Client(api_key=self.api_key)

    def _convert_messages(self, messages: List[Message]) -> List[Any]:
        from google.genai import types
        contents = []
        for msg in messages:
            role = "user" if msg.role in (MessageRole.USER, MessageRole.TOOL) else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.content)],
                )
            )
        return contents

    def generate(
        self,
        messages: List[Message],
        tools: Optional[List[BaseTool]] = None,
        system_instruction: Optional[str] = None,
    ) -> LLMResponse:
        from google.genai import types

        contents = self._convert_messages(messages)
        tool_declarations = None
        if tools:
            tool_declarations = [t.func for t in tools]

        config = types.GenerateContentConfig(
            temperature=self.temperature,
            system_instruction=system_instruction,
            tools=tool_declarations if tool_declarations else None,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )

            tool_calls: List[ToolCall] = []
            content_text = ""

            if response.function_calls:
                for idx, call in enumerate(response.function_calls):
                    tool_calls.append(
                        ToolCall(
                            id=f"call_{idx}_{call.name}",
                            name=call.name,
                            arguments=dict(call.args or {}),
                        )
                    )

            if response.text:
                content_text = response.text

            return LLMResponse(
                content=content_text,
                tool_calls=tool_calls,
                model=self.model_name,
            )
        except Exception as e:
            return LLMResponse(
                content=f"Error communicating with Gemini API: {str(e)}",
                model=self.model_name,
            )
