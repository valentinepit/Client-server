def file_encoding_detect(_name):
    from chardet import detect
    with open(_name, 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    return encoding
