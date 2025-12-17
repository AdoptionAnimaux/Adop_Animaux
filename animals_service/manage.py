#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animals_service.settings')

    # --- Consul Registration ---
    if "runserver" in sys.argv:
        try:
            # Add project root to sys.path to allow importing 'shared'
            current_path = os.path.dirname(os.path.abspath(__file__))
            sys.path.append(os.path.join(current_path, ".."))

            from shared.consul_client import register_service
            register_service(
                name="animals-service",
                port=8002,
                prefix="animals"
            )
        except Exception as e:
            print(f"⚠️ Warning: Could not register with Consul: {e}")
    # ---------------------------

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
