# v1.0.1 - Linux mode after sleep

The Keychron wireless wake path forces a report of the rear OS switch, even if it did not move. Preserve Linux mode for that unchanged report; an explicit Fn+Space exit or actual switch movement still restores standard mode. Full restart continues to start in the rear-switch-selected standard layout.

Build and host regression tests passed. Physical sleep/wake verification remains required. No flashing was performed here. The v1.0.0 baseline is unchanged.
