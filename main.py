import dotenv

dotenv.load_dotenv(
    dotenv_path="./.streamlit/secrets.toml",
    override=True,
)

import os
import warnings

os.environ["HYDRA_FULL_ERROR"] = "1"
warnings.filterwarnings("ignore")

from hydra import initialize, compose
from hydra.core.global_hydra import GlobalHydra
from langgraph.errors import GraphRecursionError

from src.pipelines.pipeline import load_workflow


def main(
    config_path: str,
    job_name: str,
    config_name: str,
) -> None:
    def initialize_hydra():
        if GlobalHydra().is_initialized():
            GlobalHydra().clear()
        initialize(
            config_path=config_path,
            job_name=job_name,
        )

    initialize_hydra()
    config = compose(config_name=config_name)
    return load_workflow(
        config,
        stream=False,
    )


if __name__ == "__main__":
    CONFIG_PATH = "configs/"
    JOB_NAME = "withpet"
    CONFIG_NAME = "home.yaml"
    app = main(
        config_path=CONFIG_PATH,
        job_name=JOB_NAME,
        config_name=CONFIG_NAME,
    )

    try:
        for chunk in app.stream(
            {"question": "대형견이 놀 수 있는 수영장이 있는 펜션"},
            {"recursion_limit": 10},
            stream_mode="updates",
        ):
            for step, state in chunk.items():
                print(f"[{step}]\n")
                for k, v in state.items():
                    if k not in ["schema", "formatted_data", "filtered_data"]:
                        print(f"{k}\n{v}")
            print("-" * 100)
    except GraphRecursionError:
        print("Recursion Error")
