FROM jupyter/pyspark-notebook

MAINTAINER Pierre Navaro <navaro@math.cnrs.fr>

USER root

COPY . ${HOME}

RUN chown -R ${NB_USER} ${HOME}

USER $NB_USER

RUN conda env update -n base --quiet -f environment.yml && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN python -m pip uninstall pyarrow --yes && \
    python -m pip install pyarrow
