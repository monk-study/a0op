from kfp import dsl
from kfp.dsl import ContainerOp
from kubernetes.client.models import V1Volume, V1PersistentVolumeClaimVolumeSource, V1VolumeMount

@dsl.pipeline(
    name='torch-durr-pipeline',
    description='Pipeline that runs two notebooks from torch-durr workspace'
)
def notebook_pipeline():
    # First notebook task with volume mount
    notebook_task1 = ContainerOp(
        name="first-notebook",
        image='pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime',
        command=['ipython'],
        arguments=[
            '/home/jovyan/torch-durr-volume/package_install.ipynb'
        ]
    )
    
    # Add volume mount
    notebook_task1.add_volume(
        V1Volume(
            name='torch-durr-volume',
            persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
                claim_name='torch-durr-pvc'  # Replace with your PVC name
            )
        )
    ).add_volume_mount(
        V1VolumeMount(
            name='torch-durr-volume',
            mount_path='/home/jovyan/torch-durr-volume'
        )
    )
    
    # Second notebook task with volume mount
    notebook_task2 = ContainerOp(
        name="second-notebook",
        image='pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime',
        command=['ipython'],
        arguments=[
            '/home/jovyan/torch-durr-volume/notebook2.ipynb'
        ]
    ).after(notebook_task1)
    
    # Add volume mount to second task
    notebook_task2.add_volume(
        V1Volume(
            name='torch-durr-volume',
            persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
                claim_name='torch-durr-pvc'  # Replace with your PVC name
            )
        )
    ).add_volume_mount(
        V1VolumeMount(
            name='torch-durr-volume',
            mount_path='/home/jovyan/torch-durr-volume'
        )
    )

# Compile to YAML
from kfp import compiler
compiler.Compiler().compile(notebook_pipeline, 'torch_durr_pipeline.yaml')
