import re

def telegram_format(text):
    """
    Convert model output to clean Telegram HTML format,
    using proper Telegram-supported formatting
    """
    if not text:
        return text

    # Convert headers to bold text
    text = re.sub(r'^##\s*(.+)$', r'<b>\1</b>\n\n', text, flags=re.MULTILINE)
    text = re.sub(r'^###\s*(.+)$', r'<b>\1</b>\n', text, flags=re.MULTILINE)

    # Handle bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)

    # Handle italic text
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)

    # Convert bullet points
    text = re.sub(r'^\s*[-*+]\s(.+)$', r'• \1\n', text, flags=re.MULTILINE)

    # Format numbered lists
    text = re.sub(r'^\s*(\d+)\.\s(.+)$', r'\1. \2\n', text, flags=re.MULTILINE)

    # Handle code blocks
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(1).strip())
        return f"CODEBLOCK_{len(code_blocks)-1}_PLACEHOLDER"
    
    text = re.sub(r'```(.*?)```', save_code_block, text, flags=re.DOTALL)

    # Handle inline code
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    # Convert links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    # Restore code blocks
    for i, code in enumerate(code_blocks):
        text = text.replace(
            f"CODEBLOCK_{len(code_blocks)-1}_PLACEHOLDER",
            f'<pre>{code}</pre>\n'
        )

    # Clean up multiple consecutive newlines
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Add spacing after sections
    text = re.sub(r':(.*?)\n', r':\1\n\n', text)

    # Handle regular newlines
    text = text.replace('\r\n', '\n')

    # Final cleanup
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text
