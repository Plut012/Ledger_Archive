# Development Workflow

## Bug Fix & Feature Implementation Process

When you add feedback to `FEEDBACK.md`, here's the systematic workflow we'll follow:

### Phase 1: Understanding 🔍
1. **Read the issue** from FEEDBACK.md
2. **Ask clarifying questions** if anything is unclear:
   - What's the expected vs actual behavior?
   - Can you reproduce it consistently?
   - Are there any error messages?
   - Which module/component is affected?
3. **Reproduce the bug** (if applicable)
4. **Identify root cause** through code inspection

### Phase 2: Planning 📋
1. **Create a concise overview** of what needs to be done
2. **Use TodoWrite tool** to create a checklist with specific steps:
   ```
   - Read relevant files
   - Identify the bug location
   - Write/update tests
   - Implement fix
   - Verify fix works
   - Run test suite
   - Update documentation if needed
   ```
3. **Get your approval** on the plan before proceeding

### Phase 3: Implementation 🔧
1. **Work through the todo list** systematically
2. **Mark items as in_progress** then **completed** as we go
3. **Write code** following the project's simplicity philosophy
4. **Keep you updated** on progress

### Phase 4: Testing ✅
1. **Run existing tests**:
   ```bash
   uv run pytest -v
   ```
2. **Write new tests** if the bug wasn't caught by existing tests
3. **Manual verification**:
   - Test the specific bug scenario
   - Test related functionality
   - Check for regressions
4. **Report test results**

### Phase 5: Completion 🎉
1. **Summarize what was changed**
2. **Move issue** from "Open" → "Completed" in FEEDBACK.md
3. **Note any side effects** or additional changes
4. **Suggest improvements** if relevant
5. **Archive periodically**: Move completed items to `docs/archive/completed_feedback.md` to keep FEEDBACK.md clean

---

## Quick Reference

### Adding Feedback
```bash
# Open the feedback file
vim FEEDBACK.md  # or your preferred editor

# Add your issue under "Open Issues"
# Save and tell Claude to process it
```

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_crypto.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=backend
```

### Starting the Server
```bash
# Development mode (auto-reload)
uv run python backend/main.py

# Production mode
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## Benefits of This Workflow

✅ **Systematic** - No issues get lost or forgotten
✅ **Traceable** - Clear record of what was done
✅ **Safe** - Tests catch regressions
✅ **Collaborative** - You can batch multiple issues
✅ **Async** - Add issues anytime, process them later
✅ **Learning** - See the full problem-solving process

---

## Tips

- **Batch similar issues** together for efficiency
- **Prioritize** issues (HIGH/MEDIUM/LOW)
- **Be specific** in descriptions for faster resolution
- **Include screenshots** if it helps explain the issue
- **Note your environment** if relevant (browser, OS, etc.)
