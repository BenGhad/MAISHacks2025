import yaml
import os


def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config

#quick test
if __name__ == "__main__":
    config = load_config()
    print(config)