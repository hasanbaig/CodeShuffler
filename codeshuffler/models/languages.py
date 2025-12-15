EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".h": "cpp",
    ".hpp": "cpp",
    ".java": "java",
    ".js": "javascript",
    ".ts": "javascript",
}


def language_from_extension(ext: str) -> str:
    return EXTENSION_LANGUAGE_MAP.get(ext.lower(), "python")
