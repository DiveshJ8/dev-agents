from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type
from pydantic import BaseModel, create_model


class BaseTool:
    """Encapsulates a callable tool with parameter schema and metadata."""

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        args_schema: Optional[Type[BaseModel]] = None,
    ):
        self.name = name
        self.description = description.strip()
        self.func = func
        self.args_schema = args_schema or self._generate_schema(func)

    def _generate_schema(self, func: Callable[..., Any]) -> Type[BaseModel]:
        sig = inspect.signature(func)
        fields: Dict[str, Any] = {}
        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue
            annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
            default = param.default if param.default != inspect.Parameter.empty else ...
            fields[param_name] = (annotation, default)

        return create_model(f"{self.name}Schema", **fields)

    def run(self, **kwargs: Any) -> Any:
        return self.func(**kwargs)

    def to_gemini_declaration(self) -> Dict[str, Any]:
        """Converts tool definition to Gemini function declaration format."""
        schema_dict = self.args_schema.model_json_schema()
        # Clean schema for Gemini compatibility
        props = schema_dict.get("properties", {})
        required = schema_dict.get("required", [])

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "OBJECT",
                "properties": props,
                "required": required,
            },
        }

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)


def tool(name: Optional[str] = None, description: Optional[str] = None) -> Callable[[Callable[..., Any]], BaseTool]:
    """Decorator to mark a function as an agent tool."""
    def decorator(fn: Callable[..., Any]) -> BaseTool:
        tool_name = name or fn.__name__
        tool_doc = description or (fn.__doc__ or "No description provided.")
        return BaseTool(name=tool_name, description=tool_doc, func=fn)
    return decorator
