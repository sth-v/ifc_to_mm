#syntax=docker/dockerfile:1
FROM condaforge/mambaforge:latest
WORKDIR /mm
COPY --link . .
COPY prod.env .env
RUN mamba install -c conda-forge pythonocc-core
RUN python -m pip install ifcopenshell git+https://github.com/contextmachine/mmcore.git
ENTRYPOINT ["python", "v2.py"]

