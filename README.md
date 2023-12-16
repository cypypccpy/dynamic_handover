# Dynamic Handover

<div align=center>
<img src="assets/image_folder/teaserv2.gif" border=0 width=75%>
</div>

## Table of Content
- [Table of Content](#table-of-content)
- [Overview](#overview)
- [Installation](#installation)
- [Training](#training)
- [Evaluation](#evaluation)
- [Acknowledgement](#acknowledgement)
- [Citations](#citations)
- [License](#license)

## Overview

This repository is the implementation code of the paper "Dynamic Handover: Throw and Catch with Bimanual Hands"([Paper](https://arxiv.org/abs/2309.05655), [Website](https://binghao-huang.github.io/dynamic_handover/), [Presentation](https://www.youtube.com/watch?v=rORbiw7dsqQ)) by Binghao Huang*, Yuanpei Chen*, Tianyu Wang, Yuzhe Qin, Yaodong Yang, Nikolay Atanasov, Xiaolong Wang. In this repo, we provide our full implementation code of simulation.

## Installation
* python 3.8
```
conda create -n rlgpu3 python=3.8
conda activate rlgpu3
```

* IsaacGym (tested with `Preview Release 3/4` and `Preview Release 4/4`). Follow the [instruction](https://developer.nvidia.com/isaac-gym) to download the package.
```
tar -xvf IsaacGym_Preview_4_Package.tar.gz
cd isaacgym/python
pip install -e .
(test installation) python examples/joint_monkey.py
```
* Dynamic Handover
```
git clone https://github.com/cypypccpy/dynamic_handover.git
cd dynamic_handover
pip install -r requirements.txt
pip install -e .
```
* Trained checkpoint. Download from [Link](https://drive.google.com/file/d/1rfi257wjXhYr_MuDuPbyXU-GesWme-cP/view?usp=sharing).


## Training

run this line in `dexteroushandenvs` folder:

```bash
python train.py --task=AllegroHandDynamicHandover --algo=mappo --num_envs=2048 --seed 22
```

To select an algorithm, pass `--algo=ppo/mappo`
as an argument. For example, if you want to use ppo algorithm, run this line in `dexteroushandenvs` folder:

```bash
python train.py --task=AllegroHandDynamicHandover --algo=ppo --num_envs=2048 --seed 22
```

The trained model will be saved to `logs` folder and the goal estimator will be saved to `traj_e` folder.

## Evaluation
To load a trained model and only perform inference (no training), pass `--play` as an argument, and pass `--model_dir` to specify the trained models which you want to load:

```bash
python train.py --task=AllegroHandDynamicHandover --algo=ppo --num_envs=20 --seed 22 --play --model_dir=<path_to_checkpoint_folder>
```

By default, the goal estimator will automatically load the `model.pt` in the `traj_e` folder. If you want to use our trained checkpoint and its corresponding goal estimator, unzip the downloaded file and manually place the `model.pt` in the `traj_e` folder and specify the `--model_dir` to the checkpoint folder.

## Acknowledgement

We thank the list of contributors from the [Bi-DexHands](https://github.com/PKU-MARL/DexterousHands).

## Citations
Please cite [Dynamic Handover](https://binghao-huang.github.io/dynamic_handover/) if you use this repository in your publications:
```
@article{huang2023dynamic,
  title={Dynamic handover: Throw and catch with bimanual hands},
  author={Huang, Binghao and Chen, Yuanpei and Wang, Tianyu and Qin, Yuzhe and Yang, Yaodong and Atanasov, Nikolay and Wang, Xiaolong},
  journal={arXiv preprint arXiv:2309.05655},
  year={2023}
}
```

## License
Licensed under the [MIT License](LICENSE)
