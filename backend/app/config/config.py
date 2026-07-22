from backend.app.config.config_manager import _config_manager

# Bootstrap: initialize settings on import
settings = _config_manager.get()
config_manager = _config_manager