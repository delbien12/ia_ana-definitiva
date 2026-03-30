def detect_code_request(text):
    keywords = ["codigo","programa","c++","python","java"]

    return any(k in text.lower() for k in keywords)