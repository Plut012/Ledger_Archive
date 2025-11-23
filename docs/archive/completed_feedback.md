# Completed Feedback & Bug Fixes

Archive of resolved issues from the development process.

---

## 2025-11-23 - Session 1

### ✅ [BUG] Home page black screen on return
- **Priority**: High
- **Issue**: Returning to home showed black screen
- **Root Cause**: Boot sequence only ran once, subsequent visits showed empty containers
- **Fix**: Added logic to show interface immediately on return visits
- **Files**: `frontend/js/modules/home.js`

### ✅ [BUG] Tutorial progression broken
- **Priority**: High
- **Issue**: Genesis block click, mining, wallet generation, and broadcast didn't progress tutorial
- **Root Cause**: Modules weren't updating global validation variables (`window.selectedBlockIndex`, etc.)
- **Fix**: Added global state updates in all modules when actions complete
- **Files**:
  - `frontend/js/modules/chain-viewer.js` - Added `window.selectedBlockIndex` and `window.lastMinedBlock`
  - `frontend/js/modules/crypto-vault.js` - Added `window.walletAddress`
  - `frontend/js/modules/network-monitor.js` - Added `window.lastBroadcastPaths`

### ✅ [TWEAK] Remove learning guide from navigation
- **Priority**: Low
- **Change**: Tutorial now only accessible via "INITIATE REBIRTH" popup
- **Files**:
  - `frontend/index.html` - Removed from nav
  - `frontend/js/modules/home.js` - Removed quick action button

**Tests**: All 26 tests passing ✓

---

## 2025-11-23 - Session 2

### ✅ [BUG] Tutorial examine block loop
- **Priority**: High
- **Issue**: After examining genesis block, tutorial loops back to "examine block" task again
- **Root Cause**: `playDialogue()` was recursive and tried to handle interactions twice (once for initial dialogue, once for teaching points)
- **Fix**: Separated concerns - created `playActSequence()` to handle the full act flow, `playDialogue()` now only displays lines
- **Files**: `frontend/js/modules/learning-guide.js`

### ✅ [TWEAK] Group Axiom messages
- **Priority**: Medium
- **Issue**: Every message showed "> AXIOM:" prefix, making it cluttered
- **Change**:
  - Speaker name shows once at start of message group
  - Blank lines separate grouped messages for readability
  - Sounds only play on first message of group
- **Result**:
  ```
  > AXIOM:
  First message

  Second message

  Third message
  ```
- **Files**: `frontend/js/modules/learning-guide.js`

**Tests**: All 26 tests passing ✓

---

## Summary Statistics

**Total Issues Resolved**: 5
- Bugs: 3
- Tweaks: 2

**Files Modified**: 6
- `frontend/js/modules/home.js`
- `frontend/js/modules/chain-viewer.js`
- `frontend/js/modules/crypto-vault.js`
- `frontend/js/modules/network-monitor.js`
- `frontend/js/modules/learning-guide.js`
- `frontend/index.html`

**Test Coverage**: All 26 tests passing throughout
