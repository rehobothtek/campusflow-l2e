# CampusFlow AI learning log

## Fellow: Salifu Nathan

### Interaction #1 — Unique ticket IDs after reload

**Problem:** I needed to understand how CampusFlow can create a new unique ticket ID after previously saved tickets have been loaded.

**My initial understanding:** The program should scan the loaded ticket list, find the highest numeric ID, and add one. I identified malformed or manually edited JSON as a possible risk after restart.

**Prompt to AI:** I chose ticket IDs as my learning topic and asked how a program should create the next ID after loading saved records.

**Useful AI guidance:** Find the highest numeric part of the existing IDs and add one. This is safer than using the number of items in the list because a ticket may have been deleted.

**My independent experiment:** I used unrelated library-record codes: `B001`, `B009`, and `B003`. I predicted that selecting the highest number and adding one would produce `B010`.

**Verification source or result:** I ran the temporary Python experiment in VS Code. The output was `B010`, which matched my prediction.

**Decision:** Accepted. I will use the highest valid numeric ID plus one when implementing ticket IDs.

**Related file/commit:** Not yet applied to the CampusFlow code.

**What I can now explain without AI:** Because deletion breaks `len()` but not `max()`.


### Interaction #2 — Input normalization

**Problem:** I needed to understand how the program can accept valid case variations while storing categories consistently.

**My initial understanding:** I knew that `.lower()` and `.upper()` can change letter case, but I did not know what problems could happen if the program stored every variation exactly as the user typed it.

**Prompt to AI:** I chose input normalization as my learning topic and asked how valid inputs such as `network`, `Network`, and `NETWORK` should be handled consistently.

**Useful AI guidance:** Clean the input with `.strip()`, compare a lowercase version to valid choices, and store one consistent display version. This avoids inconsistent reports, filtering, and testing.

**My independent experiment:** I used unrelated colour values. I tested the input `"  BlUe  "`, predicted that cleaning it and looking it up in an allowed-colours dictionary would output `Blue`, then ran the experiment.

**Verification source or result:** I ran the temporary Python experiment in VS Code. The output was `Blue`, which matched my prediction.

**Decision:** Accepted. CampusFlow will compare cleaned lowercase category input but store a consistent category value such as `Network`.

**Related file/commit:** Not yet applied to the CampusFlow code.

**What I can now explain without AI:** It uses a cleaned lowercase value to compare and validate what the user typed, but stores `Network` so saved data and reports always use the same consistent spelling.