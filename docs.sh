pydoc-markdown -I isikukood/ -m functions -m isikukood -m assertions --render-toc > temp.md
sed -i 's/<a/---\n<a/' temp.md
