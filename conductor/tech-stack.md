# Technology Stack

Technology choices, dependencies, and architectural decisions for the SF Purchase Flow project.

## Primary Languages and Frameworks

### Backend
- **Language**: Java/Kotlin (to be confirmed from repo analysis)
- **Framework**: Spring Boot (assumed, to be confirmed)
- **Service**: Cart Service in premium-server/premium-cart

### Frontend
- **Language**: TypeScript
- **Framework**: React (from premium-cart-anonymous)
- **Monorepo**: Setup completed (DOM2-6587)

## Key Dependencies

### Backend Dependencies
*To be populated from premium-server/premium-cart repository analysis*

Key areas to document:
- Cart service dependencies
- Validation service dependencies
- Discount service dependencies
- Billing service dependencies
- Database/ORM dependencies

### Frontend Dependencies
*To be populated from premium-cart-anonymous repository analysis*

Key areas to document:
- React and UI library versions
- State management (Redux, Zustand, etc.)
- Routing library
- Form handling
- API client libraries

### External Services
- **Jira**: Issue tracking (DOM2-6162 epic)
- **Google Docs**: Documentation (Master Document)
- **Google Sheets**: Dependencies tracking

## Infrastructure and Deployment

### Deployment Targets
- **Backend**: Wix infrastructure (to be detailed)
- **Frontend**: Wix infrastructure (to be detailed)

### Service Architecture
- **Cart Service**: Polymorphic design (anonymous/authenticated)
- **Validation Service**: Anonymous validation sets
- **Discount Service**: Anonymous discount support
- **Billing Service**: PreviewOrder for anonymous

## Development Tools

### Version Control
- **Git**: Source control
- **GitHub**: Repository hosting (wix-private for sources, hen-gold/anon-cart for this repo)

### IDE/Editors
- Standard development environment
- Context-driven development tooling

### Build Tools
*To be populated from repository analysis*

## Testing Frameworks

### Backend Testing
*To be populated from repository analysis*
- Unit testing framework
- Integration testing framework
- Mocking libraries

### Frontend Testing
*To be populated from repository analysis*
- Component testing (Jest, React Testing Library, etc.)
- E2E testing framework
- Visual regression testing

## Code Quality Tools

### Linting
*To be populated from repository analysis*

### Formatting
*To be populated from repository analysis*

### Static Analysis
*To be populated from repository analysis*

## Anonymous Flow Specific Technologies

### Cart Management
- Anonymous cart storage (30-day expiration)
- Cart identity extraction
- Cart to authenticated user migration

### Validation
- Anonymous validation sets
- Validation enrichment for anonymous carts

### Discounts
- Anonymous discount support
- Line item discount handling

## Dependencies Tracking

See [sources/docs/dependencies.md](sources/docs/dependencies.md) for detailed dependency information from the Google Sheets spreadsheet.

## Update Log

- **Initial**: Created from project context
- **Next**: To be updated with actual dependencies from repository analysis
