FROM mrdonbrown/code-video-generator-base:base-e0f61c1

WORKDIR /app

ARG VERSION

COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .
RUN echo "Version: $VERSION" > /app/PKG-INFO


RUN    pip install -qq pybind11 \
    && pip install -qq -e .

COPY code_video /app/code_video
COPY code_video_cli /app/code_video_cli

CMD ["codevidgen"]

