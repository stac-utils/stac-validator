$graph:
- class: Workflow
  doc: Computes the inSAR closure phase from 3 Sentinel-1 SLCs acquisitions
  id: insar-clos-wf
  inputs:
    products:
      label: Sentinel-1 IW SLC products
      doc: Array of 3 Sentinel-1 IW SLC products
      default: s3://EODATA/Sentinel-1/SAR/SLC/2021/04/15/S1B_IW_SLC__1SDV_20210415T173631_20210415T173658_026480_032957_3A85.SAFE,s3://EODATA/Sentinel-1/SAR/SLC/2021/04/03/S1B_IW_SLC__1SDV_20210403T173630_20210403T173657_026305_0323C6_27E3.SAFE,s3://EODATA/Sentinel-1/SAR/SLC/2021/03/22/S1B_IW_SLC__1SDV_20210322T173630_20210322T173657_026130_031E3C_2B9F.SAFE
      type: Directory[]
    graph:
      doc: Path to SNAP graph
      label: SNAP graph
      type: string
      default: /script/coreg_ifg_SLC.xml
    box:
      label: Boundaries in pixels
      doc: The boundaries of the AOI in pixels (minX,minY,maxX,maxY).
      type: string
      default: '0,0,12000,6000'
  label: inSAR Closure Phase
  outputs:
  - id: closure_phase_output
    label: Outputs
    outputSource:
    - step_2/log_output
    type: Directory
  steps:
    step_1:
      in:
        products: products
        graph: graph
      out:
      - log_output
      run: '#closure_phase_step1'
    step_2:
      in:
        source: step_1/log_output
        box: box
      out:
      - log_output
      run: '#closure_phase_step2'
- baseCommand:
    - python3
    - "/script/main.py"
  arguments:
    - "--destination"
    - "."
  class: CommandLineTool
  id: closure_phase_step1
  inputs:
    products:
      inputBinding:
        prefix: --products
      type: Directory[]
    graph:
      inputBinding:
        prefix: --graph
      type: string
  outputs:
    log_output:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    DockerRequirement:
      dockerPull: nexus.spaceapplications.com/repository/docker-asb-public/cwl/osc-closure-phase-step1:2023-04-11a
- id: closure_phase_step2
  class: CommandLineTool
  baseCommand:
    - python3
    - "/script/ClosurePhase_step2.py"
  arguments:
    - "--destination"
    - "."
  inputs:
    source:
      doc: The source folder that contains the SLC and ifg sub-folders.
      type: Directory
      inputBinding:
        prefix: --source
    box:
      doc: The boundaries of the AOI in pixels (minX,minY,maxX,maxY).
      type: string
      default: '0,0,12000,6000'
      inputBinding:
        prefix: --box
  outputs:
    log_output:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    DockerRequirement:
      dockerPull: nexus.spaceapplications.com/repository/docker-asb-public/cwl/osc-closure-phase-step2:2023-04-18a
s:contributor:
  - s:name: Thibault Taillade
    s:email: thibault.taillade@example.com
    s:affiliation: ESA
s:logo: https://upload.wikimedia.org/wikipedia/commons/6/6e/ESA_logo_simple.svg
s:dateCreated: '2023-03-11'
s:keywords: FILTER:input-type:Sentinel-1 IW SLC, FILTER:coverage:Global
$namespaces:
  s: https://schema.org/
cwlVersion: v1.0
s:softwareVersion: 0.2.0
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
