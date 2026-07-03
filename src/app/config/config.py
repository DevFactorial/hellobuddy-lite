import configparser
from pathlib import Path

import configparser
from pathlib import Path

script_dir = Path(__file__).resolve().parent.parent.parent.parent

def read_config(config_filename: str = "config.ini") -> configparser.ConfigParser:
    # 1. Dynamically locate this running script's directory root
    
    # 2. Pin the config file relative to the script directory footprint
    config_path = script_dir / config_filename
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file missing at: {config_path}")
        
    # 3. Read the configuration properties
    print('reading config')
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def get_value_from_config(section: str, key: str, config_filename: str = "config.ini") -> str:
    config = read_config(config_filename)
    
    if section not in config:
        raise KeyError(f"Section '{section}' not found in configuration file.")
    
    if key not in config[section]:
        raise KeyError(f"Key '{key}' not found in section '{section}' of configuration file.")
    
    return config[section][key]

def get_absolute_path_from_config(config_key: str, config_filename: str = "config.ini") -> Path:
    config = read_config(config_filename)
    
    # Extract the target string path pattern
    raw_path_string = config.get("STORAGE", config_key) 
    
    # 4. Convert the string into a Cross-Platform Path object
    target_path = Path(raw_path_string)
    
    # 5. Check if the user specified a relative or absolute anchor string
    if not target_path.is_absolute():
        # If relative (like './reports/'), anchor it dynamically to your project folder root!
        absolute_target = (script_dir / target_path).resolve()
    else:
        # If already absolute (like '/var/tmp' or 'C:\Users\...'), just normalize the slash symbols
        absolute_target = target_path.resolve()
        
    return absolute_target

