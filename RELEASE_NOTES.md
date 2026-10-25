# Release notes — TaskFlow API v1.1.0

## Interface redesign
- Redesigned dashboard with a premium dark interface and acid-lime accent palette.
- Added responsive layout behavior for desktop, tablet, and mobile.
- Refined typography, summary cards, task list, status and priority labels, empty state, and create-task modal.
- Added subtle entrance, hover, orbit, and floating animations with reduced-motion support.
- Preserved FastAPI CRUD endpoints, dashboard form actions, search, status filtering, and task persistence.
- Updated API version and documented a safer Windows development command using `--reload-dir app`.

## Verification
Run `python -m pytest -v` after installing `requirements.txt`. The packaged release was tested with the project's automated suite before delivery.
