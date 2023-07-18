def update_settings(key, value):
    with open(r'app data\settings.json', 'r') as f:
        settings = f.read()

    settings = eval(settings.replace("\n", ""))

    settings[key] = value

    with open(r'app data\settings.json', 'w') as f:
        f.write(str(settings).replace("'", '"'))


def read_settings():
    with open(r'app data\settings.json', 'r') as f:
        settings = f.read()

    settings = eval(settings.replace("\n", ""))

    theme = settings["theme"]
    speaker = settings["speaker"]
    stt = settings["stt"]

    return theme, speaker, stt
