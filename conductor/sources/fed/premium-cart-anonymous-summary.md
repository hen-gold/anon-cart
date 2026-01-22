# Frontend Repository Analysis - Premium Cart Anonymous

## Source

**Repository**: premium-cart-anonymous  
**URL**: https://github.com/wix-private/premium-cart-anonymous  
**Status**: Read-Only Analysis  
**Location**: wix-private/premium-cart-anonymous (remains in original location)

## Repository Overview

This repository contains the frontend implementation for anonymous cart functionality in the Storefront purchase flow. It's a React/TypeScript monorepo that provides cart UI components and flows for anonymous users.

## Architecture

### Monorepo Structure

- **Status**: Completed (DOM2-6587)
- **Assignee**: Matan Lasry
- **Setup**: Monorepo configured for multiple packages/apps

### Technology Stack

- **Language**: TypeScript
- **Framework**: React
- **Architecture**: Monorepo with multiple packages
- **Build System**: To be confirmed from repository

## Key Components

### Cart Pages

#### Anon Cart Page (DOM2-6584)
- **Status**: Backlog
- **Story Points**: 5
- **Priority**: Minor
- **Description**: Main anonymous cart page for displaying cart contents
- **Features**:
  - Display cart items (domain, premium, business email, privacy)
  - Edit item functionality
  - Remove item functionality
  - Pricing display with breakdown
  - Promotions and discounts display
  - Checkout CTA

#### Success Page (DOM2-6604)
- **Status**: Backlog
- **Story Points**: 2
- **Priority**: Minor
- **Description**: Post-purchase success page
- **Features**:
  - Purchase confirmation
  - Next steps guidance
  - Account creation prompts (if anonymous)

#### Split Page (DOM2-6612)
- **Status**: Backlog
- **Story Points**: 1
- **Priority**: Minor
- **Assignee**: Or Efrat
- **Description**: Page that splits flow for different user types
- **Features**:
  - Anonymous user flow
  - Authenticated user flow
  - Route based on user state

### Package Pickers

#### Anon Premium Package Picker (DOM2-6506)
- **Status**: Backlog
- **Story Points**: 3
- **Priority**: High
- **Description**: Premium package selection with billing cycle
- **Features**:
  - Package tier selection
  - Billing cycle selection
  - Pricing display
  - Add to cart functionality

#### Anon Mailbox Package Picker (DOM2-6583)
- **Status**: Backlog
- **Story Points**: 4
- **Priority**: Minor
- **Description**: Mailbox package selection
- **Features**:
  - Mailbox plan selection
  - Seat selection
  - Pricing calculation
  - Add to cart functionality

### UI Components

#### MiniCart (DOM2-6586)
- **Status**: Backlog
- **Story Points**: 3
- **Priority**: Minor
- **Description**: Compact cart component for navigation/header
- **Features**:
  - Cart icon with item count
  - Quick cart preview
  - Navigate to full cart
  - Persistent across Storefront

#### Recommendation Upsells (DOM2-6601)
- **Status**: Backlog
- **Story Points**: 3
- **Priority**: Minor
- **Description**: Upsell recommendations within cart
- **Features**:
  - Contextual upsell suggestions
  - Add item from upsell
  - Dismiss functionality

#### Contact Form (DOM2-6611)
- **Status**: Backlog
- **Story Points**: 2
- **Priority**: Minor
- **Description**: Contact form integration
- **Features**:
  - Contact information collection
  - Form validation
  - Submission handling

### Integration Components

#### Cart Validations Handling (DOM2-6585)
- **Status**: Backlog
- **Story Points**: 3
- **Priority**: Minor
- **Description**: Validation error handling and display
- **Features**:
  - Error message display
  - Field-level validation
  - Cart-level validation notices
  - Actionable error messages

#### Eclipse SDK Integration (PREM2-28707)
- **Status**: Backlog
- **Story Points**: 1
- **Priority**: Major
- **Assignee**: Shay Tal-Gerby
- **Description**: Expose standalone components and pages via Eclipse SDK
- **Features**:
  - Component export
  - Page export
  - SDK integration

#### RouteGuard (PREM2-28704)
- **Status**: PR Pending
- **Story Points**: 0.5
- **Priority**: Major
- **Assignee**: Shay Tal-Gerby
- **Description**: Make Eclipse PP props optional & update RouteGuard for anonymous flow
- **Features**:
  - Anonymous route handling
  - Optional props support
  - Route protection

#### FeaturesGrid CTA (PREM2-28706)
- **Status**: PR Pending
- **Story Points**: 0.5
- **Priority**: Major
- **Assignee**: Shay Tal-Gerby
- **Description**: Show FeaturesGrid CTA buttons for anonymous users
- **Features**:
  - CTA visibility for anonymous
  - Button functionality
  - Anonymous user support

## Development Status

Development status based on Jira tasks (DOM2-6162 epic) and repository analysis.

### ✅ Completed (2 tasks)

1. **DOM2-6454** - [FED] Dev Design
   - **Status**: Done
   - **Priority**: Minor
   - **Story Points**: 3
   - **Assignee**: Matan Lasry
   - **Description**: Frontend development design completed
   - **Repository Impact**: Design documentation and architecture decisions

2. **DOM2-6587** - [FED] - Cart anonymous monorepo
   - **Status**: Done
   - **Priority**: Minor
   - **Story Points**: 1
   - **Assignee**: Matan Lasry
   - **Description**: Monorepo setup for anonymous cart project
   - **Repository Impact**: Monorepo structure configured and operational

### 🔄 In Progress (0 tasks)

No FED tasks currently in progress.

### ⏳ PR Pending (2 tasks)

1. **PREM2-28704** - [Anonymous] Make Eclipse PP props optional & update RouteGuard for anonymous flow
   - **Status**: PR Pending
   - **Priority**: Major
   - **Story Points**: 0.5
   - **Assignee**: Shay Tal-Gerby
   - **Description**: Make Eclipse PP props optional and update RouteGuard for anonymous flow
   - **Repository Impact**: RouteGuard component updated, Eclipse props made optional
   - **Code Status**: Code complete, awaiting review

2. **PREM2-28706** - [Anonymous] Show FeaturesGrid CTA buttons for anonymous users
   - **Status**: PR Pending
   - **Priority**: Major
   - **Story Points**: 0.5
   - **Assignee**: Shay Tal-Gerby
   - **Description**: Enable FeaturesGrid CTA buttons for anonymous users
   - **Repository Impact**: FeaturesGrid component updated for anonymous support
   - **Code Status**: Code complete, awaiting review

### 📋 Backlog (9 FED tasks)

#### High Priority (1 task)

1. **DOM2-6506** - [FED] Anon Premium package picker & billing cycle
   - **Story Points**: 3 | **Assignee**: Unassigned
   - **Description**: Premium package selection with billing cycle picker

#### Minor Priority (8 tasks)

1. **DOM2-6583** - [FED] - Anon Mailbox package picker
   - **Story Points**: 4 | **Assignee**: Unassigned

2. **DOM2-6584** - [FED] - Anon Cart Page
   - **Story Points**: 5 | **Assignee**: Unassigned
   - **Description**: Main anonymous cart page

3. **DOM2-6585** - [FED] - Cart validations handling
   - **Story Points**: 3 | **Assignee**: Unassigned

4. **DOM2-6586** - [FED] - MiniCart Integration
   - **Story Points**: 3 | **Assignee**: Unassigned

5. **DOM2-6601** - [FED] - Recommendation Upsells
   - **Story Points**: 3 | **Assignee**: Unassigned

6. **DOM2-6604** - [FED] - Success Page
   - **Story Points**: 2 | **Assignee**: Unassigned

7. **DOM2-6611** - [FED] - Contact Form integration
   - **Story Points**: 2 | **Assignee**: Unassigned

8. **DOM2-6612** - [FED] - Split Page
   - **Story Points**: 1 | **Assignee**: Or Efrat

### Premium/Eclipse Integration (2 tasks in backlog)

1. **PREM2-28705** - [Anonymous] Verify DoublePurchase & SwitchProduct modules handle missing siteGuid gracefully
   - **Status**: Backlog
   - **Priority**: Major
   - **Story Points**: 0.5
   - **Assignee**: Shay Tal-Gerby

2. **PREM2-28707** - [Anonymous] Expose standalone components and pages via Eclipse SDK
   - **Status**: Backlog
   - **Priority**: Major
   - **Story Points**: 1
   - **Assignee**: Shay Tal-Gerby

### Summary Statistics

- **Total FED Tasks**: 11
- **Completed**: 2 (18%)
- **In Progress**: 0 (0%)
- **PR Pending**: 2 (18%)
- **Backlog**: 7 (64%)

- **Premium/Eclipse Tasks**: 4
- **PR Pending**: 2 (50%)
- **Backlog**: 2 (50%)

### Implementation Roadmap

**Phase 1: Foundation (Completed)**
- ✅ Dev Design (Done)
- ✅ Monorepo setup (Done)

**Phase 2: Eclipse Integration (PR Pending)**
- RouteGuard updates (PR Pending)
- FeaturesGrid CTA (PR Pending)

**Phase 3: Core Components (Backlog)**
- Anon Cart Page (High priority, 5 SP)
- Package pickers (Premium, Mailbox)
- MiniCart integration
- Cart validations handling

**Phase 4: User Experience (Backlog)**
- Success Page
- Split Page
- Recommendation Upsells
- Contact Form integration

**Phase 5: Eclipse SDK (Backlog)**
- Standalone components export
- DoublePurchase/SwitchProduct verification

## Anonymous Flow Features

### Implemented
- ✅ Monorepo setup completed (DOM2-6587)
- ✅ Dev Design completed (DOM2-6454)

### PR Pending (Ready for Review)
- RouteGuard for anonymous flow (PREM2-28704)
- FeaturesGrid CTA for anonymous users (PREM2-28706)

### In Progress / Planned

#### Core Cart Functionality (Backlog)
- Anonymous cart page (DOM2-6584) - High priority, 5 SP
- Cart validations handling (DOM2-6585)
- MiniCart integration (DOM2-6586)

#### Package Selection (Backlog)
- Anon Premium package picker & billing cycle (DOM2-6506) - High priority
- Anon Mailbox package picker (DOM2-6583)

#### User Experience (Backlog)
- Success pages (DOM2-6604)
- Split page functionality (DOM2-6612)
- Recommendation upsells (DOM2-6601)
- Contact form integration (DOM2-6611)

## Eclipse Integration

### Components
- **Standalone Components**: Expose via Eclipse SDK (PREM2-28707)
- **FeaturesGrid CTA**: Buttons for anonymous users (PREM2-28706)
- **RouteGuard**: Updates for anonymous flow (PREM2-28704)

### Verification
- **DoublePurchase & SwitchProduct**: Handle missing siteGuid gracefully (PREM2-28705)
  - Status: Backlog
  - Priority: Major
  - Story Points: 0.5

## State Management

### Cart State
- Cart items management
- Pricing state
- Validation state
- Promotion/discount state

### User State
- Anonymous user identification
- Authentication state
- User preferences

### Navigation State
- Current flow step
- Entry point tracking
- Navigation history

## API Integration

### Backend Services
- **Cart Service**: Cart CRUD operations
- **Validation Service**: Cart validation
- **Discount Service**: Discount application
- **Billing Service**: Order preview

### API Patterns
- Anonymous user identification
- Cart state synchronization
- Error handling
- Retry logic

## User Flows

### Anonymous Cart Flow
1. User selects items (domain, premium, etc.)
2. Items added to anonymous cart
3. User views cart (full cart page)
4. User edits/removes items
5. User proceeds to checkout
6. Login prompt (if needed)
7. Cart migration to authenticated user
8. Checkout completion

### Mini Cart Flow
1. User adds items to cart
2. Cart icon shows item count
3. User clicks cart icon
4. Mini cart opens
5. User can view items
6. User clicks "Continue" to full cart
7. User continues in flow

## Dependencies

### Frontend Libraries
*To be populated from repository analysis when access is available*

Expected dependencies:
- React and React DOM
- TypeScript
- State management library (Redux, Zustand, etc.)
- Routing library (React Router, etc.)
- Form handling library
- UI component library
- API client library

### Build Tools
*To be populated from repository analysis*

## Testing

### Test Requirements
- Component unit tests
- Integration tests
- E2E tests for cart flows
- Anonymous user flow tests
- Cart state management tests

### Test Frameworks
*To be populated from repository analysis*

## Analysis Status

**Status**: Analysis based on Jira issues and project context  
**Access**: Repository is private (wix-private), read-only analysis only  
**Next Steps**: 
1. Direct repository access for detailed code analysis
2. Extract actual dependency information from package.json
3. Document component architecture and patterns
4. Document React patterns and conventions
5. Document monorepo structure

## Important Notes

- This repository remains in its original location (wix-private/premium-cart-anonymous)
- This file contains only analysis and documentation extracted from Jira issues and project context
- No code has been moved or copied from the original repository
- All analysis is read-only
