import openai

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key="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"  # Replace with your OpenAI API key
)

def get_translation(post: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text into English: {post}"
            }
        ]
    )
    return response.choices[0].message.content

def get_language(post: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Detect the language of the following text: {post}"
            }
        ]
    )
    return response.choices[0].message.content

def query_llm_robust(post: str) -> tuple[bool, str]:

    try:
        # Detect language
        detected_language = get_language(post)

        # Check if the language detection response is in the expected format
        if not isinstance(detected_language, str):
            raise ValueError("Unexpected language detection response format")

        # Check if English
        is_english = "english" in detected_language.lower()

        # Translate if not English
        if not is_english:
            translation = get_translation(post)

            # Check if the translation response is in the expected format
            if not isinstance(translation, str):
                raise ValueError("Unexpected translation response format")
        else:
            translation = post  # If English, keep the original post

        return (is_english, translation)

    except (ValueError, Exception) as e:
        # Handle unexpected responses or errors
        print(f"Error during LLM query: {e}")  # Log the error
        return (False, post)  # Default to assuming non-English and return original post


def translate_content(content: str) -> tuple[bool, str]:
    return query_llm_robust(content)
    # if content == "这是一条中文消息":
    #     return False, "This is a Chinese message"
    # if content == "Ceci est un message en français":
    #     return False, "This is a French message"
    # if content == "Esta es un mensaje en español":
    #     return False, "This is a Spanish message"
    # if content == "Esta é uma mensagem em português":
    #     return False, "This is a Portuguese message"
    # if content  == "これは日本語のメッセージです":
    #     return False, "This is a Japanese message"
    # if content == "이것은 한국어 메시지입니다":
    #     return False, "This is a Korean message"
    # if content == "Dies ist eine Nachricht auf Deutsch":
    #     return False, "This is a German message"
    # if content == "Questo è un messaggio in italiano":
    #     return False, "This is an Italian message"
    # if content == "Это сообщение на русском":
    #     return False, "This is a Russian message"
    # if content == "هذه رسالة باللغة العربية":
    #     return False, "This is an Arabic message"
    # if content == "यह हिंदी में संदेश है":
    #     return False, "This is a Hindi message"
    # if content == "นี่คือข้อความภาษาไทย":
    #     return False, "This is a Thai message"
    # if content == "Bu bir Türkçe mesajdır":
    #     return False, "This is a Turkish message"
    # if content == "Đây là một tin nhắn bằng tiếng Việt":
    #     return False, "This is a Vietnamese message"
    # if content == "Esto es un mensaje en catalán":
    #     return False, "This is a Catalan message"
    # if content == "This is an English message":
    #     return True, "This is an English message"
    # return True, content
