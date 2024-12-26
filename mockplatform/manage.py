#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# 在你的应用目录下创建 management/commands/mycommand.py
 
from django.core.management.base import BaseCommand
 
class Command(BaseCommand):
    help = 'My custom manage.py command'
 
    def handle(self, *args, **options):
        # 你的命令逻辑
        self.stdout.write('Hello, World!')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mockplatform.settings')
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
