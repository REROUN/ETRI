#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

"""
    source(autonn) 🚩 BASE_DIR
        ├── Dockerfile
        ├── manage.py
        ├── requirement.txt
        ├── autonn_core
        │       ├─ __init__.py
        │       ├─ admin.py
        │       ├─ apps.py
        │       ├─ models.py
        │       ├─ serializers.py
        │       ├─ urls.py
        │       ├─ views.py
        │       ├─ migrations
        │       │   └─ __init__.py
        │       ├─ datasets
        │       │   ├─ coco
        │       │   ├─ coco128
        │       │   ├─ imagenet
        │       │   └─ voc
        │       └─ tango 💃 'tango' modules
        │           ├─ common
        │           │   ├─ cfg
        │           │   └─ model
        │           ├─ main
        │           │   ├─ classify.py
        │           │   ├─ detect.py
        │           │   ├─ export.py
        │           │   ├─ finetune.py
        │           │   ├─ search.py
        │           │   ├─ test.py
        │           │   └─ train.py
        │           ├─ nas
        │           ├─ hpo
        │           ├─ viz
        │           │   ├─ binder.py
        │           │   ├─ graph.py
        │           │   ├─ layer_definition.py
        │           │   └─ node_edge.py
        │           └─ utils
        │               ├─ activations.py
        │               ├─ autoanchor.py
        │               ├─ autobatch.py
        │               ├─ datasets.py
        │               ├─ general.py
        │               ├─ loss.py
        │               ├─ metrics.py
        │               ├─ nms.py
        │               ├─ plots.py
        │               ├─ google_utils.py
        │               └─ torch_utils.py
        ├── config
        │       ├─ __init__.py
        │       ├─ settings.py
        │       ├─ urls.py
        │       ├─ asgi.py
        │       └─ wsgi.py
        └── visualization
                ├─ public
                ├─ src
                └─ package.json
"""

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
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
