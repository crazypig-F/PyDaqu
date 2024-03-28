import os.path


def save_csv(sheet, save_path, index=True):
    path = "/".join(save_path.split("/")[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
    sheet.to_csv(save_path, index=index, encoding="utf_8_sig")
