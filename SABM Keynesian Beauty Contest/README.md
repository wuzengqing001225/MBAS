# SABM Keynesian Beauty Contest
SABM KBC ver. 24.06.18



## Overview

1. Settings:
    - The experiment was divided into 4 groups: 3 different reward rules (*amplified, independent, exclusive*) without explicit instruction, and a control group with explicit instruction.
    - Run 15 times per setting.

2. Each group was executed according to this procedure:
    1. The simuation was divided into 4 rounds
        (1) No dialogue, directly let agents output the decided number (as the first data point).
        (2) First round of dialogue, let agents output a number.
        (3) Continue to the second round of dialogue, let agents output a number.
        (4) Continue to the third round of dialogue, let agents output a number (as the fourth data point).
    2. Each output number will not be used as input for the next round of the agent's dialogue.
    This is to demonstrate the process of gradually learning, essentially showing breakpoints in a 3-round dialogue process to observe the agent's learning situation at each stage.

3. Presentation of results
    - The first chart should have 3 curves corresponding to 3 different reward rules. It shows the average variance of the numbers decided by the agents in each round over 15 runs. It is expected that the patterns in the curves for independent and amplify are similar, while the exclusive curve should be the opposite with a larger variance.
    - The second chart is a comparison between with explicit instruction and without explicit instruction. It is expected that the difference in explicit instruction is very small.

## Usage

1. Place your GPT API key json file `configAPIKey.json` in the root dir.
2. For backend, you may run the program via `mainKBC.py`.
    - For running multiple different setups, use `multipleSimulations()`. You may set `configSimulation["runs"]` to control the number of runs for each setting.
    - For running a single simulation, use `singleSimulation()`.
3. For direct use, please run `app.py` and see the results on your local `http://127.0.0.1:5000`.
4. You can configure the run parameters for a single simulation in `configEnv.py`. Note that if you modify `"runMode"` from `rule` to `LLM`, the LLMs API will be called.
5. Prompt
    - The basic elements of prompt are in `PromptModule.prompt.py`.
    - The combination of prompts used by agents are in `AgentModule.methodAgentPrompt.py`.

