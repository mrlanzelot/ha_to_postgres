import logging
import os
from logging.handlers import RotatingFileHandler


DEFAULT_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
DEFAULT_LOG_FILE = "ha_ingest.log"

_configured = False


def setup_logging(app_name: str = "ha_ingest", level: int | None = None, log_dir: str | None = None):
	"""Configure logging for the application.

	- Creates a `logs/` directory if missing
	- Adds a rotating file handler and a console handler
	"""
	global _configured
	if _configured:
		return

	log_dir = log_dir or DEFAULT_LOG_DIR
	os.makedirs(log_dir, exist_ok=True)

	# Basic logger setup
	if level is None:
		# Allow LOG_LEVEL to override default
		env_level = os.getenv("LOG_LEVEL", "INFO").upper()
		try:
			level = getattr(logging, env_level)
		except Exception:
			level = logging.INFO

	logger = logging.getLogger()
	logger.setLevel(level)

	# formatter
	fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
	formatter = logging.Formatter(fmt)

	# Console handler
	ch = logging.StreamHandler()
	ch.setLevel(level)
	ch.setFormatter(formatter)
	logger.addHandler(ch)

	# Rotating file handler
	file_path = os.path.join(log_dir, DEFAULT_LOG_FILE)
	fh = RotatingFileHandler(file_path, maxBytes=10_000_000, backupCount=5)
	fh.setLevel(level)
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	_configured = True


__all__ = ["setup_logging"]