#!/usr/bin/env python3
from functools import reduce
import os
import sys
import yaml

import logging

def main(args=sys.argv[1:]):
  resource_list = yaml.load(sys.stdin, Loader=yaml.FullLoader)

  certificate_arn = dict_get(resource_list, 'functionConfig.spec.certificate-arn')
  host_name = dict_get(resource_list, 'functionConfig.spec.host')

  ingresses = []
  for resource in dict_get(resource_list, 'items', []):
    if resource['apiVersion'] in ['extensions/v1beta1', 'networking.k8s.io/v1', 'networking.k8s.io/v1beta1'] and resource['kind'] == 'Ingress':
      # patch annnotation
      if certificate_arn:
        ann = dict_get(resource, 'metadata.annotations', {})
        ann['alb.ingress.kubernetes.io/certificate-arn'] = certificate_arn
      
      # patch host
      if host_name:
        for rule in dict_get(resource, 'spec.rules', []):
          rule['host'] = host_name

    ingresses.append(resource)
  sys.stdout.write(yaml.dump_all(ingresses))

def dict_get(dictionary, keys, default=None):
  return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

if __name__ == '__main__':
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  sys.stderr.reconfigure(encoding='utf-8')
  main()