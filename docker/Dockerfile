FROM mrdonbrown/code-video-generator-base:base-3c091ed

WORKDIR /app

ARG VERSION

COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .
RUN echo "Version: $VERSION" > /app/PKG-INFO


RUN    pip install -qq pybind11 \
    && pip install -qq -r requirements.txt -e .

COPY code_video /app/code_video
COPY code_video_cli /app/code_video_cli

CMD ["codevidgen"]

