#!/usr/bin/env python3
from functools import reduce
import os
import sys
import yaml

import logging

def main(args=sys.argv[1:]):
  resource_list = yaml.load(sys.stdin, Loader=yaml.FullLoader)

  target_name   = dict_get(resource_list, 'functionConfig.metadata.name')
  annotations   = dict_get(resource_list, 'functionConfig.spec.annotations', {})

  hosts = []
  for host in dict_get(resource_list, 'functionConfig.spec.hosts', []):
    hosts.append({
      'name': dict_get(host, 'name'),
      'target': dict_get(host, 'target') })

  output = []
  for resource in dict_get(resource_list, 'items', []):
    if resource['apiVersion'] in ['extensions/v1beta1', 'networking.k8s.io/v1', 'networking.k8s.io/v1beta1']  \
        and resource['kind'] == 'Ingress'  \
        and dict_get(resource, 'metadata.name') == target_name:

      # patch annnotation
      if len(annotations) > 0:
        ann = dict_get(resource, 'metadata.annotations')
        if ann is not None:
          for key in annotations:
            ann[key] = annotations[key]
        else:
          resource['metadata']['annotations'] = annotations

      for host in hosts:
        host_name = dict_get(host, 'name')
        target = dict_get(host, 'target')

        # patch host
        for rule in dict_get(resource, 'spec.rules', []):
          if target is None or rule['host'] == target:
            rule['host'] = host_name
        
        #TODO patch tls

    output.append(resource)
  sys.stdout.write(yaml.dump_all(output))

def dict_get(dictionary, keys, default=None):
  return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

if __name__ == '__main__':
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  sys.stderr.reconfigure(encoding='utf-8')
  main()