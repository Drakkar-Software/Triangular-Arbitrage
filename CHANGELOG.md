# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2024-10-24
### Updated
- remove non spot symbols from detection

## [1.2.0] - 2024-10-24
### Added
- cycle detection by @ruidazeng

## [1.1.1] - 2024-09-07
### Fixed
- main profit result display

## [1.1.0] - 2024-09-07
### Added
- networkx dependencies

## [1.0.6] - 2024-04-18
### Added
- Added `whitelisted_symbols` to `run_detection`

## [1.0.5] - 2024-01-09
### Fixed
- Fix `is_delisted_symbols` 1.0.4 new condition

## [1.0.4] - 2024-01-09
### Fixed
- Consider delisted symbol if `ticker_time` is None

## [1.0.3] - 2024-01-08
### Fixed
- Add `None` check before restoring `best_triplet`

## [1.0.2] - 2024-01-08
### Added
- `ignored_symbols` param to `run_detection`

## [1.0.1] - 2023-10-18
### Fixed
- Added MANIFEST.in to fix PYPI installation

## [1.0.0] - 2023-10-18
### Added
- Initial version
