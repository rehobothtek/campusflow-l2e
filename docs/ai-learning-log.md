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