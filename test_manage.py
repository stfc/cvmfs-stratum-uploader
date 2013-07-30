#!/usr/bin/env python
import os
from manage import main

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_CONFIGURATION", "Test")
    os.environ.setdefault("REUSE_DB", "1")
    main()