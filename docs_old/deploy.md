# Deploy

```bash
git tag -a vx.x.x -m "vx.x.x"
git push --tags
python -m build --sdist && python -m build --wheel
twine check ./dist/*
twine upload ./dist/*
```
