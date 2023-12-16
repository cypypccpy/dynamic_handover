# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ast import arg
from matplotlib.pyplot import get
import numpy as np
import random

from utils.config import set_np_formatting, set_seed, get_args, parse_sim_params, load_cfg
from utils.parse_task import parse_task
from utils.process_sarl import *
from utils.process_marl import process_MultiAgentRL, get_AgentIndex
import os

from rl_games.common import env_configurations, experiment, vecenv
from rl_games.common.algo_observer import AlgoObserver
from rl_games.torch_runner import Runner

import yaml

# from utils.rl_games_custom import
from rl_games.common.algo_observer import IsaacAlgoObserver

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"


if __name__ == '__main__':
    set_np_formatting()
    args = get_args(use_rlg_config=True)
    if args.checkpoint == "Base":
        args.checkpoint = ""

    if args.algo == "ppo":
        config_name = "cfg/{}/ppo_continuous.yaml".format(args.algo)
    elif args.algo == "lego":
        config_name = "cfg/{}/ppo_continuous.yaml".format(args.algo)
        if args.task in ["AllegroHandLegoGrasp", "AllegroHandLegoTest", "AllegroHandLegoTestPAI", "AllegroHandLegoTestOrient",
                         "AllegroHandLegoTestOrientGrasp", "AllegroHandLegoTestOrientGraspBelif", "AllegroHandLegoTestSpin", "AllegroHandLegoGraspInsertVValuePretrainMo",
                         "AllegroHandLegoTestPAInsertRotateSpin", "AllegroHandLegoTestPAISpin", "AllegroHandLegoTestSpinOnce", "AllegroHandLegoPAInsertOrientGrasp", "AllegroHandLegoPAInsertOrientGrasp", "AllegroHandLegoPAInsertOrientGraspOrientRL",
                         "AllegroHandLegoPAInsertOrientGraspOrientTSTAR"]:
            config_name = "cfg/{}/ppo_continuous_grasp.yaml".format(args.algo)
        if args.task in ["AllegroHandLegoInsert", "AllegroHandLegoInsertMo", "AllegroHandLegoTestPAInsert", "AllegroHandLegoTestPAInsertOrient"]:
            config_name = "cfg/{}/ppo_continuous_insert.yaml".format(args.algo)
        if args.task in ["AllegroHandLegoRetrieveGrasp", "AllegroHandLegoRetrieveGraspVValue", "AllegroHandLegoRetrieveGraspVValuePretrain", "AllegroHandLegoRetrieveGraspVValuePretrainMo"]:
            config_name = "cfg/{}/ppo_continuous_retrieve_grasp_v_value.yaml".format(args.algo)
    elif args.algo == "arctic":
        config_name = "cfg/{}/ppo_continuous_arctic.yaml".format(args.algo)


    elif args.algo == "ppo_lstm":
        config_name = "cfg/{}/ppo_continuous_lstm.yaml".format(args.algo)
    else:
        print("We don't support this config in RL-games now")

    args.task_type = "RLgames"
    print('Loading config: ', config_name)

    args.cfg_train = config_name
    cfg, cfg_train, logdir = load_cfg(args, use_rlg_config=True)
    sim_params = parse_sim_params(args, cfg, cfg_train)
    cfg_train["seed"] = args.seed
    cfg["env"]["numEnvs"] = args.num_envs
    cfg["env"]["test"] = args.play

    set_seed(cfg_train.get("seed", -1), cfg_train.get("torch_deterministic", False))

    agent_index = get_AgentIndex(cfg)
    task, env = parse_task(args, cfg, cfg_train, sim_params, agent_index)

    # override
    with open(config_name, 'r') as stream:
        rlgames_cfg = yaml.safe_load(stream)
        rlgames_cfg['params']['config']['name'] = args.task
        rlgames_cfg['params']['config']['num_actors'] = env.num_environments
        rlgames_cfg['params']['seed'] = cfg_train["seed"]
        rlgames_cfg['params']['config']['env_config']['seed'] = cfg_train["seed"]
        rlgames_cfg['params']['config']['vec_env'] = env
        rlgames_cfg['params']['config']['env_info'] = env.get_env_info()
        rlgames_cfg['params']['config']['device'] = args.rl_device

    vargs = vars(args)
    algo_observer = IsaacAlgoObserver()

    runner = Runner(algo_observer)
    # runner = Runner()
    runner.load(rlgames_cfg)
    runner.reset()
    runner.run(vargs)
