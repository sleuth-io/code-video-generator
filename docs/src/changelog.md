# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1](https://pypi.org/project/code-video-generator/0.3.1/) - 2020-11-17
### Added
- New sequence diagram generator using a simple dsl to generate animated diagrams
- Extracted code highlight actions into standalone objects and transitions for more control
- Simple box widgets and a connector for animating box diagrams
- Lots and lots more docs

### Changed
- Slight changes in behavior of `CodeScene` convenience methods
- Restructured internals to expose more consistent, public API

## [0.2.4](https://pypi.org/project/code-video-generator/0.2.4/) - 2020-11-09
### Added
- Standalone shell script `codevidgen.sh` that uses docker to install and run this project locally