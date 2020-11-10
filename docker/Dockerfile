FROM mrdonbrown/code-video-generator-base:base-c0c4cfa

WORKDIR /app

ARG VERSION

COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .
RUN echo "Version: $VERSION" > /app/PKG-INFO


RUN    pip install -qq pybind11 \
    && pip install -qq -e .

COPY patches /app/patches

# Workaround until this is released: https://github.com/ManimCommunity/manim/pull/639
RUN cd /usr/local/lib/python3.8/site-packages && git apply /app/patches/639.diff

COPY code_video /app/code_video
COPY code_video_cli /app/code_video_cli

CMD ["codevidgen"]

