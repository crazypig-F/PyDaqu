import os


def file_path():
    folder = {
        "mapping": {
            "parallel": {},
            "chamber": {},
            "stage": {}
        },
        "raw": {},
        "temp": {
            "phy": {
                "parallel": {},
                "chamber": {
                    "mean": {},
                    "std": {}
                },
                "stage": {
                    "mean": {},
                    "std": {}
                }
            },
            "microbe": {
                "parallel": {
                    "bacteria": {
                        "top": {},
                        "all": {}
                    },
                    "fungi": {
                        "top": {},
                        "all": {}
                    },
                    "merge": {
                        "top": {},
                        "all": {}
                    }
                },
                "chamber": {
                    "bacteria": {
                        "top": {},
                        "all": {}
                    },
                    "fungi": {
                        "top": {},
                        "all": {}
                    },
                    "merge": {
                        "top": {},
                        "all": {}
                    }
                },
                "stage": {
                    "bacteria": {
                        "top": {},
                        "all": {}
                    },
                    "fungi": {
                        "top": {},
                        "all": {}
                    },
                    "merge": {
                        "top": {},
                        "all": {}
                    }
                }
            },
            "amino": {
                "parallel": {},
                "chamber": {
                    "mean": {},
                    "std": {}
                },
                "stage": {
                    "mean": {},
                    "std": {}
                }
            },
            "alpha": {
                "parallel": {},
                "chamber": {
                    "mean": {},
                    "std": {}
                },
                "stage": {
                    "mean": {},
                    "std": {}
                }
            },
            "beta": {
                "bacteria": {},
                "fungi": {}
            },
            "abundance": {
                "bacteria": {},
                "fungi": {},
                "amino": {}
            },
            "corr": {
                "bac_fun": {},
                "micro_amino": {},
            },
            "core": {},
            "ml": {
                "process": {}
            },
            "溯源分析": {}
        }
    }
    return folder


def mkdir(dirs, root):
    for filename in dirs.keys():
        path = os.path.join(root, filename)
        if not os.path.exists(path):
            os.mkdir(path)
        sub_dirs = dirs[filename]
        if sub_dirs:
            mkdir(sub_dirs, path)


def main():
    data_path = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    mkdir(file_path(), data_path)


if __name__ == '__main__':
    main()
