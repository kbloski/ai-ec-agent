def build_llm_section(tag: str, content: str, purpose: str | None = None) -> str:
    opening_tag = f'<{tag} purpose="{purpose}">' if purpose else f"<{tag}>"
    return f"{opening_tag}\n{content}\n</{tag}>"
