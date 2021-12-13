# Ingress patch example by Kustomize

## patchesJson6902
https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesjson6902/

```sh
kustomize build patchesStrategicMerge/
```

## patchesStrategicMerge
https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesstrategicmerge/

```sh
kustomize build patchesStrategicMerge/
```

## replacements
https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/

```sh
kustomize build replacements/
```

## transformers
https://kubectl.docs.kubernetes.io/guides/extending_kustomize/exec_krm_functions/

```sh
pip install pyyaml
kustomize build transformers/ --enable-alpha-plugins --enable-exec
```