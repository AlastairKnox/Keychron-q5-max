# v1.0.3 - Correct Fn+H

History is now on Fn+H, matching left butterfly+H. v1.0.2 accidentally placed the Fn binding on J. Boot migration adds the H default and removes the old History action on J while preserving deliberate remaps. All v1.0.2 functionality and the sleep fix are retained.

Build and host checks pass. The regression check now derives the H matrix position from the base layout, and checks saved-map migration and remap preservation. No flashing performed.
