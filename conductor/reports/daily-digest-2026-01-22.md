# Daily Digest - 2026-01-22

## Code Changes

- No code changes detected (repositories are private - requires direct access)

## Jira Updates

- **DOM2-6652**: Created - [BED] Implement AnonTestsSeedPlugin for Conductor (Assignee: Shachar Reshef, Priority: Minor)
  - Summary updated from "[BED] Create AnonPlugin" to "[BED] Implement AnonTestsSeedPlugin for Conductor"
  - Story Points set to 4
  - Assigned to Shachar Reshef

- **DOM2-6651**: Created - [BED] Implement AnonSeedService for Anonymous Tests Conduction (Assignee: Shachar Reshef, Priority: Minor)

- **DOM2-6587**: Status changed from `In Progress` → `Done` (Assignee: Matan Lasry)
  - Issue completed: [FED] - Cart anonymous monorepo

- **DOM2-6487**: Status changed from `In Progress` → `Done` (Assignee: Shachar Reshef)
  - Issue completed: [BED Design] Supporting Anon Tests Conduction in Conductor
  - Priority changed from `Minor` → `High` (on 2026-01-14)

## Slack Communications

- **Key discussions**: 20+ messages in channel #anon-cart

### Decisions

- **Decision**: Use `BrowserRouter` for back navigation from view cart to flow (plans/mailbox package picker steps) (by FED team)
- **Decision**: Keep `flowType` and `cartId` as separate parameters (still both needed) (by FED team)
- **Decision**: Align `cartIntent` naming to `cartEntryPoint` for last intent + default domains for empty cart (by FED team)
- **Decision**: Use recommendation service for both cases - Cart/miniCart and successPage with customParams providing cartEntryPoint and lineItems (by FED team)
- **Decision**: Both proposals for availability validation are valid - background execution preferred (by FED team)
  - Either trigger background `getCart(skipValidations:false)` (optimistic UI) or run `checkDomainAvailability` in background when domain is in cart

- **Status updates**:
  - FED design starts in D6
  - 20-minute syncs scheduled for Monday and Wednesday
  - Master doc updated

- **Blockers/Dependencies**:
  - Need to verify plans package picker in account level context (gavinr, shayg to verify in playground)
  - Need to map all errors for UX coverage (shahari, talso to provide error mapping)
  - Privacy with 100% discount requirement needs clarification (bard requesting clarification from talso)

## Open Action Items

- **Verify plans package picker can operate in account level context** (Owner: gavinr, shayg) [#anon-cart]
- **Map all errors available for UX coverage** (Owner: shahari, talso) [#anon-cart]
- **Clarify Privacy with 100% discount requirements and use cases** (Owner: talso) [#anon-cart]
- **Work on DOM2-6652**: [BED] Implement AnonTestsSeedPlugin for Conductor (Owner: Shachar Reshef) [Jira]
- **Work on DOM2-6651**: [BED] Implement AnonSeedService for Anonymous Tests Conduction (Owner: Shachar Reshef) [Jira]

## Context Updates

- Updated: conductor/reports/daily-digest-2026-01-22.md
- Updated: conductor/CHANGELOG.md (if sync ran)

## Summary

- Total changes: 4+ (Jira updates + Slack activity)
- Blockers: 3 (plans package picker verification, error mapping, privacy discount clarification)
- Decisions: 5 (FED design decisions, availability validation approach)
- Context files updated: 1-2
- Slack messages: 20+ in last 24 hours
- Open action items: 5
