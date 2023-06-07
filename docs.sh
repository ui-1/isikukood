#!/bin/bash

cat > README.md << 'EOF'
# Isikukood

Small Estonian social security number library (I know they're not really SSNs but I don't have a better English name for them)

# Installation

Simply run the following:
```bash
pip install isikukood
```

EOF

pydoc-markdown -I isikukood/ -m functions -m isikukood -m assertions --render-toc >> README.md
sed -i 's/<a/---\n<a/' README.md
