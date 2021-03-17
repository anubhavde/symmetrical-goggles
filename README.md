![Airborne Banner](https://i.imgur.com/5PC9G3k.jpg)

# Airborne Object Tracking Starter Kit

[![Discord](https://img.shields.io/discord/565639094860775436.svg)](https://discord.gg/BT9uegr)


This repository is the main Airborne Object Tracking challenge **submission template and starter kit**! 

Clone the repository to compete now!

**This repository contains**:
*  **Documentation** on how to submit your agent to the leaderboard
*  **The procedure** for best practices and how we evaluate your agent, etc.
*  **Starter code** for you to get started!


![](https://i.imgur.com/fscUnZp.png)

#  Competition Procedure

The main task of the competition is to detect a collision threat reliability. In this challenge you will train your agents locally and then upload them to AIcrowd (via git) to be evaluated. 

**The following is a high level description of how this round works**

![](https://i.imgur.com/t1GsPtu.png)


1. **Sign up** to join the competition [on the AIcrowd website.](https://www.aicrowd.com/challenges/airborne-object-tracking-challenge)
2. **Clone** this repo and start developing your submissions.
3. **Train** your models to detect objects using the `train_locally.sh`.
4. [**Submit**](#how-to-submit-a-model) your trained models to [AIcrowd Gitlab](https://gitlab.aicrowd.com) for evaluation [(full instructions below)](#how-to-submit-a-model).  The automated evaluation setup will evaluate the submissions against the test dataset, to compute and report the metrics on the leaderboard of the competition.

# How to Submit a Model!

## Setup



1.  **Clone the github repository** or press the "Use this Template" button on GitHub!

    ```
    git clone https://github.com/aicrowd/airborne_detection_starter_kit.git
    ```

2. **Install** competition specific dependencies!
    ```
    cd airborne_detection_starter_kit
    pip3 install -r requirements.txt
    ```

3. **Specify** your specific submission dependencies (PyTorch, Tensorflow, etc.)

    * (Optional) **Anaconda Environment**. If you would like to use anaconda to manage your environment, make sure at least version `4.5.11` is required to correctly populate `environment.yml` (By following instructions [here](https://www.anaconda.com/download)). Then:
        * **Create your new conda environment**

            ```sh
            conda create --name airborne_challenge
            conda activate airborne_challenge
            ```

      * **Your code specific dependencies**
        ```sh
        conda install <your-package>
        ```

    * **Pip Packages** If you are using specific Python packages **make sure to add them to** `requirements.txt`! Here's an example:
      ```
      # requirements.txt
      matplotlib
      tensorflow
      ```
    * **Apt Packages** If your training procedure or agent depends on specific Debian (Ubuntu, etc.) packages, add them to `apt.txt`.


## How do I specify my software runtime ?

As mentioned above, **the software runtime is specified in 3 places**: 
* `environment.yml` -- The _optional_ Anaconda environment specification. 
    As you add new requirements you can export your `conda` environment to this file!
    ```
    conda env export --no-build > environment.yml
    ```
* `requirements.txt` -- The `pip3` packages used by your agent to train. **Note that dependencies specified by `environment.yml` take precedence over `requirements.txt`.** As you add new pip3 packages to your training procedure either manually add them to `requirements.txt` or if your software runtime is simple, perform:
    ```
    # Put ALL of the current pip3 packages on your system in the submission
    pip3 freeze > requirements.txt
    ```


* `apt.txt` -- The Debian packages (via aptitude) used by your training procedure!


These files are used to construct both the **local and AIcrowd docker containers** in which your agent will train. 


## What should my code structure be like ?

Please follow the example structure shared in the starter kit for the code structure.
The different files and directories have following meaning:

```
.
├── aicrowd.json           # Submission meta information like your username
├── apt.txt                # Packages to be installed inside docker image
├── data                   # The downloaded dataset, the path to directory is also available as `DATASET_LOCATION` env variable
├── requirements.txt       # Python packages to be installed
├── test.py                # IMPORTANT: Your testing/inference phase code, must include main() method
├── train                  # Your trained model MUST be saved inside this directory, must include main() method
└── utility                # The utility scripts to provide smoother experience to you.
    ├── debug_build.sh
    ├── docker_run.sh
    ├── environ.sh
    └── verify_or_download_data.sh
```

Finally, **you must specify an AIcrowd submission JSON in `aicrowd.json` to be scored!** 

The `aicrowd.json` of each submission should contain the following content:

```json
{
  "challenge_id": "airborne-detection-challenge",
  "authors": ["your-aicrowd-username"],
  "description": "sample description about your awesome agent",
  "license": "MIT",
  "gpu": true
}
```

This JSON is used to map your submission to the said challenge, so please remember to use the correct `challenge_id` as specified above.

Please specify if your code will use a GPU or not for the evaluation of your model. If you specify `true` for the GPU, a **NVIDIA Tesla K80 GPU** will be provided and used for the evaluation.

### Dataset location

You **don't** need to upload the data set in submission and it will be provided in online submissions at `DATASET_LOCATION` path. For local training and evaluations, you can download it once in your system via `python /utility/verify_or_download_data.py` or place manually into `data/` folder.


## Training and Testing Code Entrypoint (where you write your code!)

The evaluator will use `test.py` as the entrypoint for testing stage, so please remember to include the files in your submission!

The inline documentation in these files will guide you in interfacing with evaluator properly.

## IMPORTANT: Saving Models during Training!

Before you submit make sure that your code does the following.

* **During training** (`train.py`) **save your models to the `train/` folder.**
* **During testing** (`test.py`) **load your model from the `train/` folder.**

## How to submit a trained agent!

To make a submission, you will have to create a **private** repository on [https://gitlab.aicrowd.com/](https://gitlab.aicrowd.com/).

You will have to add your SSH Keys to your GitLab account by following the instructions [here](https://docs.gitlab.com/ee/gitlab-basics/create-your-ssh-keys.html).
If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

Then you can create a submission by making a _tag push_ to your repository on [https://gitlab.aicrowd.com/](https://gitlab.aicrowd.com/).
**Any tag push (where the tag name begins with "submission-") to your private repository is considered as a submission**  
Then you can add the correct git remote, and finally submit by doing :

```
cd competition_submission_starter_template
# Add AIcrowd git remote endpoint
git remote add aicrowd git@gitlab.aicrowd.com:<YOUR_AICROWD_USER_NAME>/airborne_detection_starter_template.git
git push aicrowd master

# Create a tag for your submission and push
git tag -am "submission-v0.1" submission-v0.1
git push aicrowd master
git push aicrowd submission-v0.1

# Note : If the contents of your repository (latest commit hash) does not change,
# then pushing a new tag will **not** trigger a new evaluation.
```

You now should be able to see the details of your submission at :
[gitlab.aicrowd.com/<YOUR_AICROWD_USER_NAME>/airborne_detection_starter_template/issues](gitlab.aicrowd.com//<YOUR_AICROWD_USER_NAME>/airborne_detection_starter_template/issues)

**NOTE**: Remember to update your username in the link above :wink:

In the link above, you should start seeing something like this take shape (each of the steps can take a bit of time, so please be patient too :wink: ) :
![](https://i.imgur.com/FqScw4m.png)

and if everything works out correctly, then you should be able to see the final scores like this :
![](https://i.imgur.com/56Leaya.jpg)

**Best of Luck** :tada: :tada:

# Other Concepts

## Time constraints

You are expected to train your model online using the training phase docker container and output the trained model in `train/` directory.

You need to make sure that your model can predict for each sample within 10 seconds, otherwise the submission will be mark as failed. (_need revision on timeouts based on budget_)

## Local evaluation

TBA

# 📎 Important links


💪 &nbsp;Challenge Page: https://www.aicrowd.com/challenges/airborne-object-tracking-challenge

🗣️ &nbsp;Discussion Forum: https://www.aicrowd.com/challenges/airborne-object-tracking-challenge/discussion

🏆 &nbsp;Leaderboard: https://www.aicrowd.com/challenges/airborne-object-tracking-challenge/leaderboards
