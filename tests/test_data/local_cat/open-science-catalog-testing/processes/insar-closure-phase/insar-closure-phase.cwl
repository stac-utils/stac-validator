$namespaces:
  s: https://schema.org/
cwlVersion: v1.0
s:softwareVersion: 0.1.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf

$graph:

- class: Workflow

  id: insar-closure-phase
  label: Insar closure phase
  doc: Insar closure phase

  requirements:
  - class: ScatterFeatureRequirement
  - class: InlineJavascriptRequirement
  - class: SubworkflowFeatureRequirement

  inputs:
    reference: 
      type: Directory
      label: Reference SLC dataset
    secondary:
      type: Directory[]
      label: Secondary SLC dataset  
    swath:
      type: string
      label: swath

  outputs: 
  - id: wf_outputs
    outputSource:
    - node_closure_phase/results
    type: Directory
  
  steps:

    node_graphista:
      in:
        reference: reference
        secondary: secondary
        swath: swath
      out:
      - results

      run: "#graphista"
      scatter: secondary
      scatterMethod: dotproduct

    node_closure_phase:
      in:
        input_reference: node_graphista/results
        swath: swath
      out:
      - results

      run: '#closure_phase'
      


- class: CommandLineTool

  id: graphista
  label: generates the interferogram for S1 SLC 

  requirements: 
    DockerRequirement:
      dockerPull: registry.hub.docker.com/terradue/graphista-empty:dev0.11.2
    ResourceRequirement:
      coresMax: 4
      ramMax: 36000
    InlineJavascriptRequirement: {}
    InitialWorkDirRequirement:
      listing:
        - entryname: custom.vmoptions
          entry: |-
            # Enter one VM parameter per line
            # Initial memory allocation
            -Xms16G
            # Maximum memory allocation
            -Xmx32G
            # Disable verifier
            -Xverify:none
            # Turns on point performance optimizations
            -XX:+AggressiveOpts
            # disable some drawing driver useless in server mode
            -Dsun.java2d.noddraw=true
            -Dsun.awt.nopixfmt=true
            -Dsun.java2d.dpiaware=false
            # larger tile size to reduce I/O and GC
            -Dsnap.jai.defaultTileSize=1024
            -Dsnap.dataio.reader.tileWidth=1024
            -Dsnap.dataio.reader.tileHeigh=1024
            # disable garbage collector overhead limit
            -XX:-UseGCOverheadLimit
        - entryname: run_me.sh
          entry: |-
            reference=$1

            cd /tmp
            
            graphista run --custom-recipe $HOME/processor.py "$@"
            exitcode=$?
            echo "Graphista exit code $exitcode"
            [ "$exitcode" != "0" ] && exit $exitcode

            cd -
            
            Stars copy -r 4 -rel -xa False -o ./ /tmp/catalog.json
            exitcode=$?
            echo "Stars exit code $exitcode"
            [ "$exitcode" != "0" ] && exit $exitcode

            rm -fr .cache .config .install4j run_me.sh custom.vmoptions || true
            exit $exitcode
        - entryname: processor.py
          entry:  
          
  baseCommand: ["/bin/bash", "run_me.sh"]
 
  arguments:
  - --reference
  - $( inputs.reference.path )
  - --secondary
  - $( inputs.secondary.path )
  - --params
  - ${ return "swath=" + inputs.swath; }
  
  inputs: 
    reference:
      type: Directory
    secondary: 
      type: Directory
    swath: 
      type: string

  outputs:
    results:
      type: Directory
      outputBinding:
        glob: .

- class: CommandLineTool

  id: closure_phase
  label: post processes the interferogram

  requirements: 
    DockerRequirement:
      dockerPull: registry.hub.docker.com/terradue/s1slc-closure-phase:0.1.0
    ResourceRequirement:
      coresMax: 2
      ramMax: 8000
    InlineJavascriptRequirement: {}
    
  baseCommand: closure-phase
  
  arguments:
  - valueFrom: |
      ${
        var input_reference=[];
        for (var i = 0; i < inputs.input_reference.length; i++) {
          input_reference.push("--input_reference");
          input_reference.push(inputs.input_reference[i].path);
        }
        return input_reference;
      }
  
  - valueFrom: ${ return ["--swath", inputs.swath]; }
  
  inputs:
    input_reference:
      type: Directory[]
    swath:
      type: string
  
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory