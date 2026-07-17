import sys
import configparser
from pathlib import Path
from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, InitSettingsSource, PydanticBaseSettingsSource
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from pydantic import ValidationError

# A reusable type that converts empty strings ("") from the INI file into None
BlankToNone = Annotated[Optional[str], BeforeValidator(lambda v: None if v == "" else v)]

# Capture the exact directory where *this* script file lives
current_dir = Path(__file__).resolve().parent

# 1. Custom INI Source Parser
class IniConfigSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings], ini_file_path: str = "config.ini"):
        super().__init__(settings_cls)
        # Store just the filename string so we can combine it with our dynamic root path
        self.config_filename = ini_file_path

    def get_field_value(self, field_name: str, field_title: str, file_content: Any = None) -> Any:
        pass
    
    def read_config(self) -> configparser.ConfigParser:
        # Walk up the directory tree until we find the parent folder that contains the 'src' directory.
        # If this file lives inside 'src/config/settings.py', it will look at 'src/config' (no 'src' folder inside),
        # then move up to your project root (which *does* contain the 'src' folder).
        root_dir = current_dir
        if (current_dir / 'src').is_dir():
            root_dir = current_dir
        else:
            for parent in current_dir.parents:
                if (parent / 'src').is_dir():
                    root_dir = parent
                    break
        
        # Target your config file at the project root level
        config_path = root_dir / self.config_filename
        
        print(f"🔎 Looking for config at: {config_path}")
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file missing at: {config_path.absolute()}")
            
        print('📖 Reading config file...')
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    def __call__(self) -> Dict[str, Any]:
        # Let read_config locate the file and handle it
        config = self.read_config()
        
        settings_dict: Dict[str, Any] = {}
        for section in config.sections():
            # Nest everything under the section name in lowercase
            settings_dict[section.lower()] = dict(config.items(section))
                    
        return settings_dict


# 2. Section Sub-Models
class StorageSettings(BaseModel):
    app_data_path: str
    resume_file_path: BlankToNone = Field(default=None)


class EmailSettings(BaseModel):
    recipient: str


class SchedulerSettings(BaseModel):
    schedule_time: str = Field(default=None)


class ApiKeysSettings(BaseModel):
    serp_api_key: BlankToNone = Field(default=None)
    mailtrap_api_token: str
    reed_api_key: BlankToNone = Field(default=None)
    adzuna_app_key: BlankToNone = Field(default=None)
    adzuna_app_id: BlankToNone = Field(default=None)


class SearchSettings(BaseModel):
    search_query_serp:BlankToNone = Field(default=None) 
    search_query_reed:BlankToNone = Field(default=None) 
    search_query_adzuna:BlankToNone = Field(default=None) 
    search_query: str
    search_location: str
    search_country: str
    num_pages: int


# 3. Core Settings Class
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    storage: StorageSettings
    email: EmailSettings
    scheduler: SchedulerSettings
    api_keys: ApiKeysSettings
    search_settings: SearchSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: InitSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            IniConfigSettingsSource(settings_cls, ini_file_path="config.ini"),
        )


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    settings = None
    try:
        settings = AppSettings()
        print("✅ Settings loaded successfully!\n")
    except (ValidationError, FileNotFoundError) as e:
        print("\n❌ Configuration Error detected!")
        
        if isinstance(e, FileNotFoundError):
            print(e)
        else:
            print("Please check your 'config.ini' file or environment variables.\n")
            for error in e.errors():
                location = " -> ".join(str(p) for p in error["loc"])
                message = error["msg"]
                print(f"  • [{location}]: {message}")
        
        sys.exit(1)

    # safe printing if settings loaded properly
    print("--- Storage Configurations ---")
    print(f"Resume Path: {settings.storage.resume_file_path}")
    print(f"App Data Path: {settings.storage.app_data_path}")
    
    print("\n--- Scheduler Configurations ---")
    print(f"Time: {settings.scheduler.schedule_time}")
    
    print("\n--- Search Configurations ---")
    print(f"Pages to scan: {settings.search_settings.num_pages}")
    
    print("\n--- API Keys ---")
    print(f"Mailtrap Token: {settings.api_keys.mailtrap_api_token}")