# Development Workflow

Development practices, quality gates, and team workflows for the SF Purchase Flow project.

## Development Methodology

### Context-Driven Development
This project follows the [Context-Driven Development](https://github.com/wshobson/agents) methodology:

1. **Context Phase**: Establish or verify project context artifacts
2. **Specification Phase**: Define requirements and acceptance criteria
3. **Planning Phase**: Break specifications into actionable tasks
4. **Implementation Phase**: Execute tasks following established patterns

### Brownfield Project Approach
- Extract context from existing codebase patterns
- Reconcile existing patterns with desired patterns
- Document technical debt and modernization plans
- Preserve working patterns while establishing standards

## Git Workflow

### Branch Strategy
- **main/master**: Production-ready code
- **feature/**: Feature branches for new functionality
- **fix/**: Bug fix branches
- **refactor/**: Refactoring branches

### Commit Conventions
Follow conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

Example: `feat(cart): add anonymous cart support`

### Pull Request Process
1. Create feature branch from main
2. Implement changes following context artifacts
3. Update relevant context documents if needed
4. Create PR with clear description
5. Request review from relevant team members
6. Address feedback
7. Merge after approval

## Code Review Requirements

### Review Checklist
- [ ] Code follows established patterns
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Context artifacts are updated if needed
- [ ] No breaking changes (or documented)
- [ ] Error handling is appropriate
- [ ] Performance considerations addressed

### Review Focus Areas
- **Backend**: Service architecture, polymorphism patterns, validation logic
- **Frontend**: Component structure, user experience, error handling
- **Integration**: API contracts, service communication, error propagation

## Testing Requirements

### Test Coverage Targets
- **Unit Tests**: 80%+ coverage for business logic
- **Integration Tests**: Critical paths covered
- **E2E Tests**: Key user flows covered

### Testing Frameworks
- **Backend**: TBD (to be populated from repo analysis)
- **Frontend**: TBD (to be populated from repo analysis)
- **E2E**: TBD (to be populated from repo analysis)

### Anonymous Flow Testing
- Test anonymous cart creation and management
- Test anonymous to authenticated transition
- Test anonymous cart expiration
- Test anonymous discount application

## Quality Assurance Gates

### Pre-Commit
- Linting passes
- Unit tests pass
- No obvious errors

### Pre-Merge
- All tests pass
- Code review approved
- Context artifacts updated if needed
- Documentation updated

### Pre-Deploy
- Integration tests pass
- E2E tests pass for critical paths
- Performance benchmarks met
- Security review (if applicable)

## Deployment Procedures

### Environment Strategy
- **Development**: Local development
- **Staging**: Pre-production testing
- **Production**: Live environment

### Deployment Checklist
- [ ] All tests passing
- [ ] Context artifacts reviewed
- [ ] Documentation updated
- [ ] Rollback plan prepared
- [ ] Monitoring in place

## Team Workflows

### Backend (BED) Team
- Focus on cart service refactoring
- Implement polymorphism patterns
- Support anonymous flows
- Maintain API contracts

### Frontend (FED) Team
- Implement cart UI components
- Build anonymous cart flows
- Integrate with backend services
- Ensure responsive design

### UX Team
- Research and design flows
- Prototype interactions
- User testing
- Iterate based on feedback

### Cross-Team Coordination
- Regular sync meetings
- Shared context artifacts
- Clear API contracts
- Documented integration points

## Team Communication

### Primary Communication Channel

**Slack Channel**: [C0A6AMMMTFY](https://wix.slack.com/archives/C0A6AMMMTFY)

The main team communication channel for SF Purchase Flow (DOM2-6162) is on Slack. This channel is used for:
- Real-time team coordination between BED, FED, UX, and Premium teams
- Status updates and progress sharing
- Discussion of blockers and dependencies
- Architectural and design decisions
- Quick questions and clarifications

### Channel Access

- **Channel ID**: C0A6AMMMTFY
- **URL**: https://wix.slack.com/archives/C0A6AMMMTFY
- **Workspace**: wix.slack.com

### Agent Access

Agents can read from this channel using MCP-S Slack tools:
- `slack_get_channel_history` - Get recent messages
- `slack_search-messages` - Search for specific content
- `slack_get_thread_replies` - Read message threads

See [sources/slack/channel-info.md](sources/slack/channel-info.md) for detailed access instructions.

### Communication Patterns

- **Status Updates**: Teams share progress updates in the channel
- **Blockers**: Blockers and dependencies are discussed openly
- **Decisions**: Important decisions are documented in Slack and should be reflected in context artifacts
- **Coordination**: Cross-team coordination happens in real-time via Slack

### When to Check Slack

- Before starting work on a track
- When checking for team updates
- When looking for decisions or discussions
- When investigating blockers or dependencies
- When needing clarification on implementation details

## Context Artifact Maintenance

### When to Update
- **product.md**: When product vision or goals change
- **tech-stack.md**: When adding dependencies or changing tech
- **workflow.md**: When practices evolve
- **tracks.md**: When track status changes
- **decisions.md**: When significant product or technical decisions are made

### Update Process
1. Identify needed update
2. Make change in appropriate artifact
3. Commit with clear message
4. Review in PR if significant change
