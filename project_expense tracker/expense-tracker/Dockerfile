# This image already contains Python and uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# the folder where the app runs inside the container
WORKDIR /project/app

# install the two packages with uv
RUN uv pip install --system pydantic python-dotenv

# start the app (our code comes from the project folder shared with -v in the docker run command)
CMD ["python", "main.py"]
