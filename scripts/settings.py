def update_settings(key, value):
    with open(r'app data\settings.js', 'r') as f:
        settings = f.read()

    settings = eval(settings.replace("\n", ""))

    settings[key] = value

    with open(r'app data\settings.js', 'w') as f:
        f.write(str(settings))


def read_settings():
    with open(r'app data\settings.js', 'r') as f:
        settings = f.read()

    settings = eval(settings.replace("\n", ""))

    theme = settings["theme"]
    speaker = settings["speaker"]
    stt = settings["stt"]

    return theme, speaker, stt