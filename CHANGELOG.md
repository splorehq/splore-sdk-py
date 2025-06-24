# Changelog

All notable changes to this project will be documented in this file.

---
## [0.1.38] - 2025-06-23
### Improvements
- **Testability**: gevent monkey patching support added to improve testability
---
## [0.1.37] - 2025-05-25
### Improvements
- **Retry Mechanism**: Enhanced retry logic with exponential backoff and jitter to prevent resource contention and improve reliability
---

---
## [0.1.33] - 2025-05-16
### Improvements
- **decorators** documentations improved to showcase usage of decorators
---
## [0.1.29] - 2025-05-16
### new features
- **polling_with_timeout**: utility function added as decorator to poll any function.
- **retry_with_timeout**: utility function added as decorator to retry any function
- **retry_extraction_by_extraction_id**: extraction can be re-run or retried with older extraction_id
### improvements
- **logger**: logger is improved to increase tracability in case of multithreading as well.

---
## [0.1.28] - 2025-05-12
### Improvements
- **Repository Cleanup**: Removed unnecessary script files and streamlined the development workflow
- **Build System Improvements**: Enhanced publish script with proper virtual environment support
- **Testing Enhancements**: Consolidated test scripts for better maintainability

---
## [0.1.27] - 2025-05-12
### Improvements
- **Extended Python Support**: Added testing and compatibility for Python 3.13
- **Testing Framework Improvements**: Enhanced test suite to support all Python versions from 3.7 to 3.13
- **Dependency Management**: Fixed dependency conflicts for Python 3.7 compatibility
- **Build System**: Unified build system approach across Python versions

---
## [0.1.23] - 2025-05-07
### Bug fixes
- fixed package import issue
---
## [0.1.22] - 2025-04-15
### Improvements
- fixed broken imports
- added extraction demo for file indexing monitoring

---
## [0.1.21] - 2025-04-09
### Improvements
- improved documentation to showcase using markdown to html conversion
- added beta tag to search capability

---
## [0.1.20] - 2025-04-09
### New Features
- **Python 3.7 Support**: Added compatibility with Python 3.7
- **Markdown to HTML Conversion**: Easily convert Markdown responses to HTML
- **More Modular SDK Architecture**: Better organization of features for cleaner code
- **Search Capability**: Added support for web searches and search history (Beta - API signature may change)

---
## [0.1.18] - 2025-03-17
### improvements
- added example in doc for multiprocessing
- added file pointer to use least privilleged location
- added support for python 3.8n and above
- increase test coverage for stability

---
## [0.1.16] - 2025-02-26
### improvements
- fixed packages to support python 3.13 onwards


---
## [0.1.15] - 2025-02-26
### improvements
- progress bar issue fixed
- added file extension to temp file destination
- added examples for multi purpose file upload
- fixed documentation issues

---
## [0.1.14] - 2025-02-25
## [0.1.13] - 2025-02-25
## [0.1.12] - 2025-02-25
### improvements
- fixed metadata issue in file uploader
- added user_id[Optional parameter] to trace user activity
- changed api url for file upload

---
## [0.1.11] - 2025-02-21
## [0.1.10] - 2025-02-21
### imporvements
- added version to the package
- fixed package installation issue
---
## [0.1.8] - [0.1.9]- 2025-02-12
### imporvements
- package name renaming as per python naming convention

---
## [0.1.7] - 2025-02-12
### imporvements
- added project meta data for better visiblity and issue tracking

---
## [0.1.6] - 2025-02-12
### imporvements
- added changelog to track updates

---
## [0.1.5] - 2025-02-12
- **Beta Release**
### Initial Release
- Core SDK functionalities:
  - **File Upload**
  - **Agent Service**
  - **Extractions Service**
- Support for Python 3.7+.
- Added structured error handling.
- documented proper examples
- incorporated unit tests for stability

---
## [0.1.0] - 2024-01-01

### Added
- Initial release of Splore Python SDK
- Basic agent management functionality
- File upload and extraction capabilities
- AWS S3 integration

## [Unreleased]

### Planned
- Asynchronous support
- Additional file format support
- Enhanced error handling
- More detailed documentation

[0.1.18]: https://github.com/splorehq/splore-sdk-py/compare/v0.1.0...v0.1.18
[0.1.0]: https://github.com/splorehq/splore-sdk-py/releases/tag/v0.1.0

---

### Notes:
- Breaking changes, if any, will be highlighted in future versions.
- Follow our [GitHub Releases](https://github.com/splorehq/splore-sdk-py/releases) for updates.