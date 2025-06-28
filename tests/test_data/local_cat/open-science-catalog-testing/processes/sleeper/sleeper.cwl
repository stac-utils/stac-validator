#!/usr/bin/env cwl-runner
$graph: 

- class: Workflow
  doc: Run a Python sleeper for between min and max seconds randomly
  id: python-sleeper
  inputs:
    min_sleep_seconds:
      doc: Min sleeping seconds
      label: Min sleeping seconds
      type: string
    max_sleep_seconds:
      doc: Max sleeping seconds
      label: Max sleeping seconds
      type: string
    ignored_product:
      doc: Ignored product
      label: Product
      type: Directory
  label: Python sleeper
  outputs: 
  - id: sleeper_output
    type: Directory
    outputSource:
    - sleeper/log_output

  steps:
    sleeper:
      in:
        min_sleep_seconds: min_sleep_seconds
        max_sleep_seconds: max_sleep_seconds
        ignored_product: ignored_product
      out:
      - log_output
      run: '#sleeper'

- class: CommandLineTool
  baseCommand: python3
  id: sleeper
  arguments: [/script/python-sleeper.py]
  requirements:
    DockerRequirement:
      # dockerPull: 10.6.1.135:5000/python-sleeper-cwl:latest
      dockerPull: nexus.spaceapplications.com/repository/docker-asb-procs/cwl/python-sleeper-cwl:latest
    EnvVarRequirement:
      envDef:
        INPUT_FOLDER: $(inputs.ignored_product["location"])
  inputs:
    min_sleep_seconds:
      type: string
      inputBinding:
        position: 1
    max_sleep_seconds:
      type: string
      inputBinding:
        position: 2
    ignored_product:
      type: Directory
      inputBinding:
        position: 3
  outputs:
    log_output:
      type: Directory
      outputBinding:
        glob: .

cwlVersion: v1.0

$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.0.2
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf