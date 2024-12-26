
1. First, create a notebook (`pipeline_components.ipynb`) that has all your KFP component code:
```python
# Cell 1 - Install required packages
!pip install kfp==1.8.22
!pip install xgboost

# Cell 2 - Import and component definitions
from kfp import components
chicago_taxi_dataset_op = components.load_component_from_file('chicago_taxi_dataset_op.yaml')
# ... rest of your component loading code
```

2. Then create a pipeline that uses NotebookOp to run this notebook:
```python
from kfp import dsl
from kfp.dsl import NotebookOp

@dsl.pipeline(
    name='notebook-xgboost-pipeline',
    description='Pipeline that runs XGBoost notebook'
)
def notebook_pipeline():
    notebook_task = NotebookOp(
        name="run-xgboost-notebook",
        notebook="pipeline_components.ipynb",
        # Specify the container image that has Jupyter and required packages
        image='gcr.io/deeplearning-platform-release/tf2-gpu.2-6:latest',  # You'll need to use an appropriate image
    )

# Compile to YAML
from kfp import compiler
compiler.Compiler().compile(notebook_pipeline, 'notebook_pipeline.yaml')
```

3. Upload the YAML through Kubeflow UI

This approach:
- Uses notebook where we need packages installed ✓
- Avoids direct kfp.Client() auth issues ✓
- Keeps the pipeline definition separate ✓
- Allows package installation in notebook ✓

The main things you'll need:
1. Make sure your notebook and YAML components are accessible to the pipeline
2. Use an appropriate container image that has the packages you need
3. Consider packaging requirements into a custom container image

