Prepare function exec

```sh
pip install pyyaml
```

Exec kustomize with plugin

```sh
kustomize build . --enable-alpha-plugins --enable-exec
```

Test function

```sh
cat test/input.yaml | ./kustomize_ingress_patch.py 
```