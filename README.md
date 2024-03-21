# Wonder 3D

This is a windows installation tutoriol of wonder3D by Samoi AI.

## Installation

### Requirements
1. CUDA toolkit version = 11.8
Set up a fresh conda environment and input the commands below line by line : 
```
conda install python==3.10.0
```

1. Install torch and xformers by `pip` : 
```
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 xformers==0.0.23.post1 --index-url https://download.pytorch.org/whl/cu118
```

2. Install other packages : 
```
pip install -r requirement.txt
```

3. Install `tiny-cuda-nn` : 
```
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

### check points
Download check points:
```
https://connecthkuhk-my.sharepoint.com/:f:/g/personal/xxlong_connect_hku_hk/Ej7fMT1PwXtKvsELTvDuzuMBebQXEkmf2IwhSjBWtKAJiA
```
put this folder under Wonder3D/

### SAM model
Download the SAM model. Put it to the Wonder3D/sam_pt/ folder.
```
https://huggingface.co/spaces/abhishek/StableSAM/blob/main/sam_vit_h_4b8939.pth
```

## Windows
1. Add the path below to your `Path` environment variable : ( Note that the path will slightly differ depending on your Microsoft Visual studio location. )

```
C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.38.33130\bin\Hostx64\x64
```

2. Make sure your `CUDA_PATH` points to v11_8

3. [Build Tools for Visual Studio 2022]( https://visualstudio.microsoft.com/zh-hant/downloads/ )

4. If there are errors installing `tiny-cuda-nn`, use this command : ( Note that the path will slightly differ depending on your Microsoft Visual studio location. )

```
"\Program Files\Microsoft Visual Studio\2022\community\vc\Auxiliary\Build\vcvars32.bat" x64
```

5. If running oｎ Windows, there may be an error about triton package, which is not available in pip of windows, but we can go to
```
https://huggingface.co/r4ziel/xformers_pre_built/blob/main/triton-2.0.0-cp310-cp310-win_amd64.whl
```
download the file, then run:
```
pip install triton-2.0.0-cp310-cp310-win_amd64.whl
```

## useage
### adjuect iterate steps
under instant-nsr-pl/configs/neuralangelo-ortho-wmask.yaml, you can adjust the parameter:
```
max_steps:
```
