---
title: Fix jules-cli skill documentation bugs
labels: documentation, bug, skill-testing
---

# Fix jules-cli Skill Documentation Bugs

## Summary

The jules-cli skill (`~/.claude/skills/jules-cli/SKILL.md`) was tested using 5 subagent scenarios covering retrieval, application, and gap analysis. The test revealed **critical documentation bugs** where the skill extensively documents features that don't exist in the actual CLI implementation.

**Test Date:** 2026-02-27
**Test Report:** See `jules-skill-test-report.md` in this repo
**Overall Grade:** C+ (would be A- with bugs fixed)

---

## Critical Issues

### 🔴 Issue #1: JSON Format Not Supported

**Severity:** Critical - Documentation Bug
**Impact:** All JSON-based workflows in the skill are unusable

**Problem:**
The skill extensively documents a `--format json` option with jq integration examples, but the actual `jules` CLI doesn't support this flag.

**Evidence from Testing:**
```bash
# Skill says this works:
jules sources list --format json | jq '.id'

# But agent discovered:
jules sources list | awk '{print $3}' | grep -E '^[0-9]+$'
```

**Affected Sections in SKILL.md:**
- Line 41-46: Sources list format options
- Line 62-68: Sessions list format options
- Line 72-75: Session get format options
- Line 87-92: Activities list format options
- Line 120-143: Output Format Selection table
- Line 169-189: Workflow 1 examples
- Line 192-202: Workflow 2 examples
- Line 204-216: Workflow 3 examples
- Line 230: Best Practices #1

**Fix Steps:**
1. [x] Verify actual CLI capabilities: `jules --help` and `jules sources --help` (Verified: `--format` is a global flag, must come before subcommand)
2. [x] Correct all `--format json` references (Updated in `docs/SKILL.md`)
3. [x] Document actual output format (Added global flag position warning)
4. [x] Update jq examples to use correct syntax and added text parsing alternatives
5. [x] Update all workflow examples in `docs/SKILL.md`

---

### ⚠️ Issue #2: CSO Description Violates Best Practices

**Severity:** Medium - Claude Search Optimization
**Impact:** Skill may not be discovered optimally

**Problem:**
The skill's YAML description summarizes the workflow instead of focusing on triggering conditions. According to skill authoring best practices, descriptions should answer "Should I read this skill right now?" not "What does this skill do?"

**Current (580 characters, summarizes workflow):**
```yaml
description: Use this skill whenever the user wants to interact with the Jules REST API or mentions Jules-related tasks like listing sources, creating sessions, managing activities, or sending agent messages. This skill provides access to all jules-cli functionality including sources management, session lifecycle (create, list, get, approve), activity tracking, agent messaging, and configuration. Always use this skill when the user asks about Jules API operations, needs to work with sources/sessions/activities, or wants to configure the Jules CLI tool.
```

**Recommended (280 characters, focuses on triggers):**
```yaml
description: Use when the user mentions jules-cli, Jules REST API, or needs to perform Jules operations like listing sources, creating sessions, managing activities, sending agent messages, or configuring API credentials. Trigger symptoms: asks about jules commands, Jules API interactions, session management, or authentication issues with jules-cli.
```

**Fix Steps:**
1. [x] Rewrite description to focus on triggering conditions (Updated in `docs/SKILL.md`)
2. [x] Keep under 500 characters (Reduced to ~300 chars)
3. [x] Include specific error messages and symptoms for searchability (Added)

---

### ⚠️ Issue #3: Discoverability Gap

**Severity:** Medium - Skill Accessibility
**Impact:** 1 out of 3 test agents failed to find the skill

**Problem:**
User-installed skills in `~/.claude/skills/` are not consistently found. One test agent searched the codebase instead and found a blog post about jules-cli, missing the actual skill documentation.

**Possible Causes:**
- Skill not in system prompt / available skills list
- Agents prioritize codebase search over skills directory
- No MCP server registration for user skills

**Fix Steps:**
1. [x] Improved discoverability by adding keywords and specific error messages to `docs/SKILL.md`
2. [x] Added "wrong flag position" troubleshooting to guide agents when they fail
3. [x] Documented version compatibility and common error symptoms

---

## Test Results Summary

| Test Type | Pass Rate | Status |
|-----------|-----------|--------|
| Retrieval Tests | 67% (2/3) | ⚠️ One agent couldn't find skill |
| Application Tests | 100% (2/2) | ✅ But revealed critical bug |
| Gap Analysis | — | 🔴 Found major documentation issue |

### What Was Tested

**Retrieval Tests:**
- ✅ Basic command discovery (found skill, correct answer)
- ✅ Parameter usage (found skill, correct syntax)
- ❌ Error troubleshooting (searched codebase, missed skill)

**Application Tests:**
- ✅ Multi-step workflow (successful, but JSON examples don't work)
- ⚠️ JSON parsing (revealed `--format json` doesn't exist)

---

## Recommended Actions

### Immediate (Critical)

1. **[HIGH PRIORITY]** Verify actual CLI capabilities and update skill
   - Run `jules --help` to see all available flags
   - Run `jules sources --help`, `jules sessions --help`, etc.
   - Document what's actually supported
   - Remove/update all incorrect examples

2. **[HIGH PRIORITY]** Update skill file at `~/.claude/skills/jules-cli/SKILL.md`
   - Remove or correct `--format json` references
   - Update workflow examples with working commands
   - Add text parsing examples using awk/grep

### Medium Priority

3. **Improve CSO description** - Rewrite to follow best practices
4. **Enhance discoverability** - Consider plugin structure
5. **Document version** - Add jules-cli version compatibility info

### Low Priority

6. **Add real-world examples** from actual usage
7. **Expand troubleshooting** with more error scenarios
8. **Add verification tests** for documented commands

---

## Resources

- **Test Report:** `jules-skill-test-report.md` (10 KB, detailed analysis)
- **Skill File:** `~/.claude/skills/jules-cli/SKILL.md`
- **Test Prompts:** `/tmp/jules-skill-test-prompts.md` (if available)

---

## Related Documentation

See `jules-skill-test-report.md` for:
- Complete test scenario details with agent responses
- Meta-commentary from each test
- CSO analysis with rationale
- All recommendations with implementation guidance

---

## Acceptance Criteria

This issue is complete when:

1. [x] All `--format json` references are verified or corrected in `docs/SKILL.md`
2. [x] Workflow examples use only supported CLI flags and correct positioning
3. [x] CSO description is rewritten to focus on triggers
4. [x] All documented commands are tested against actual CLI
5. [x] Skill is re-tested and achieves A grade (✅ **COMPLETE** - See `jules-skill-retest-report.md`)

---

**Blocked by:** Nothing
**Blocking:** Users trying to use jules-cli with incorrect documentation
**Effort estimate:** 2-3 hours (verification + updates + re-testing)
