# Backend Repository Analysis - Premium Cart

## Source

**Repository**: premium-server/premium-cart  
**URL**: https://github.com/wix-private/premium/blob/6f4fed7906410a9b9d7c05e782dbba67dbabec5a/premium-server/premium-cart  
**Status**: Read-Only Analysis  
**Location**: wix-private/premium (remains in original location)

## Repository Overview

This repository contains the backend cart service implementation for the premium/premium-server codebase. The service is being refactored to support both anonymous and authenticated cart flows through polymorphism patterns.

## Architecture

### Service Structure

The cart service follows a polymorphic design pattern to support both anonymous and authenticated users:

- **CartService**: Main cart service interface
- **CartServiceImpl**: Service implementation (to be extracted per DOM2-6605)
- **CartService Router**: Routes to Anonymous/Authenticated implementations (DOM2-6606)

### Core Components

#### Cart Service Layer
- **CartService**: Main cart service interface/implementation
  - Handles cart CRUD operations
  - Manages cart state and persistence
  - Routes to anonymous/authenticated implementations

- **CartServiceImpl**: Service implementation
  - To be extracted from CartService per DOM2-6605
  - Contains business logic for cart operations

- **CartSdl**: Cart SDL (Schema Definition Language) implementation
  - Polymorphism to be implemented per DOM2-6598
  - Handles GraphQL/resolver logic

#### Entity Management
- **CartEntityManager**: Entity manager for cart operations
  - Polymorphism to be implemented per DOM2-6599
  - Handles database operations
  - Manages cart persistence

#### Identity and Information
- **BuyerInfoDomain**: Buyer information domain
  - To be expanded per DOM2-6596
  - Stores buyer/contact information
  - Handles buyer data for anonymous and authenticated users

- **Cart Identity Extractor**: Identity extraction logic
  - To be expanded per DOM2-6597
  - Extracts user identity from requests
  - Handles anonymous vs authenticated identification

#### Validation
- **ValidationsEntricher**: Cart validation enrichment
  - To be expanded per DOM2-6602
  - Enriches cart with validation results
  - Handles validation rules application

- **Validations Service**: Validation service
  - Anonymous validations to be added per DOM2-6603
  - Defines validation rules
  - Applies validations to cart items

#### Mappers
- **CartService Mappers**: Mappers for cart operations
  - To be fixed for anonymous per DOM2-6613
  - Maps between domain models and DTOs
  - Handles anonymous user mapping

## Development Status

Development status based on Jira tasks (DOM2-6162 epic) and repository analysis.

### ✅ Completed (0 BED tasks)

No BED tasks are marked as Done. All backend work is either in progress, pending PR, or in backlog.

### 🔄 In Progress (2 tasks)

1. **DOM2-6598** - [BED] - Implement polymorphism for CartSdl
   - **Status**: In Progress
   - **Priority**: High
   - **Story Points**: 2
   - **Assignee**: Shahar Itzko
   - **Description**: Implementing polymorphism pattern for CartSdl to support anonymous/authenticated flows
   - **Repository Impact**: CartSdl class/module needs polymorphic design

2. **DOM2-6487** - [BED Design] Supporting Anon Tests Conduction in Conductor
   - **Status**: In Progress
   - **Priority**: High
   - **Story Points**: 1
   - **Assignee**: Shachar Reshef
   - **Description**: Design work for supporting anonymous tests in Conductor testing framework
   - **Repository Impact**: Test infrastructure and test design patterns

### ⏳ PR Pending (2 tasks)

1. **DOM2-6596** - [BED] - Expand BuyerInfoDomain
   - **Status**: PR Pending
   - **Priority**: High
   - **Story Points**: 0.5
   - **Assignee**: Shahar Itzko
   - **Description**: Expanded BuyerInfoDomain to support anonymous buyer information
   - **Repository Impact**: BuyerInfoDomain class expanded with anonymous user support
   - **Code Status**: Code complete, awaiting review

2. **DOM2-6597** - [BED] - Expand cart identity extractor
   - **Status**: PR Pending
   - **Priority**: High
   - **Story Points**: 0.5
   - **Assignee**: Shahar Itzko
   - **Description**: Expanded cart identity extractor to handle anonymous users
   - **Repository Impact**: CartIdentityExtractor class expanded for anonymous identification
   - **Code Status**: Code complete, awaiting review

### 📋 Backlog (11 tasks)

#### High Priority (7 tasks)

1. **DOM2-6599** - [BED] - Implement polymorphism for CartEntityManager
   - **Story Points**: 2 | **Assignee**: Shahar Itzko
   - **Dependencies**: Should follow CartSdl polymorphism pattern (DOM2-6598)

2. **DOM2-6602** - [BED] - Expand cart's ValidationsEntricher
   - **Story Points**: 0.5 | **Assignee**: Shahar Itzko

3. **DOM2-6603** - [BED] - Add anonymous validations set in Validations Service
   - **Story Points**: 0.5 | **Assignee**: Shahar Itzko

4. **DOM2-6605** - [BED] - Extract CartService implementation to CartServiceImpl
   - **Story Points**: 1 | **Assignee**: Shahar Itzko

5. **DOM2-6606** - [BED] - Refactor CartService to be router for Anonymous and Authenticated implementations
   - **Story Points**: 1 | **Assignee**: Shahar Itzko
   - **Dependencies**: Depends on DOM2-6605

6. **DOM2-6607** - [BED] - Add anonymous expiration configuration for 30 days
   - **Story Points**: 0 | **Assignee**: Shahar Itzko

7. **DOM2-6609** - [BED] - Support anonymous discounts implementation
   - **Story Points**: 0 | **Assignee**: Shahar Itzko
   - **Dependencies**: Blocks on DOM2-6608 (design) and DOM2-6616 (Discounts Service)

8. **DOM2-6613** - [BED] - Fix CartService's mappers to work anonymously
   - **Story Points**: 1.5 | **Assignee**: Shahar Itzko

#### Blocker Priority (3 tasks)

1. **DOM2-6608** - [BED] - Update the design to support new requirement of anonymous line item discounts
   - **Story Points**: 1 | **Assignee**: Shahar Itzko
   - **Impact**: Blocks DOM2-6609 (anonymous discounts implementation)

2. **DOM2-6616** - [BED] - Fix Discounts Service flows to support anonymous calls
   - **Story Points**: 1 | **Assignee**: Shahar Itzko
   - **Impact**: Blocks anonymous discount functionality

3. **DOM2-6617** - [BED] - Fix Billing's PreviewOrder implementation to support anonymous calls
   - **Story Points**: 0 | **Assignee**: Unassigned
   - **Impact**: Blocks anonymous checkout preview

### Summary Statistics

- **Total BED Tasks**: 15
- **Completed**: 0 (0%)
- **In Progress**: 2 (13%)
- **PR Pending**: 2 (13%)
- **Backlog**: 11 (73%)
- **Blockers**: 3 (all in backlog)

### Implementation Roadmap

**Phase 1: Foundation (In Progress)**
- ✅ Cart Identity Extractor expansion (PR Pending)
- ✅ BuyerInfoDomain expansion (PR Pending)
- 🔄 CartSdl polymorphism (In Progress)

**Phase 2: Core Refactoring (Backlog)**
- CartEntityManager polymorphism
- CartService extraction and routing
- ValidationsEntricher expansion
- Anonymous validation sets

**Phase 3: Anonymous Features (Backlog - Blocked)**
- Anonymous expiration configuration
- Anonymous discounts (blocked by design and service support)
- CartService mappers fix

**Phase 4: Service Integration (Backlog - Blockers)**
- Discounts Service anonymous support (Blocker)
- Billing Service PreviewOrder anonymous support (Blocker)

## Anonymous Flow Support

### Current Implementation Status

- Anonymous cart support is being implemented
- Polymorphism patterns are being added for anonymous/authenticated flows
- Cart identity extraction expanded for anonymous users (PR Pending)
- BuyerInfoDomain expanded for anonymous buyer information (PR Pending)
- CartSdl polymorphism in progress

### Planned Changes

#### Configuration
- **Anonymous Expiration**: 30-day expiration configuration (DOM2-6607)
  - Configurable expiration time for anonymous carts
  - Automatic cleanup of expired carts

#### Discounts
- **Anonymous Line Item Discounts Design**: Design update (DOM2-6608 - Blocker)
  - Design to support anonymous line item discounts
  - Must be completed before implementation

- **Anonymous Discounts Implementation**: Implementation (DOM2-6609)
  - Support for applying discounts to anonymous carts
  - Discount eligibility for anonymous users

#### Validation
- **Anonymous Validation Sets**: Validation rules (DOM2-6603)
  - Anonymous-specific validation rules
  - Validation sets for anonymous cart items

## Integration Points

### Discounts Service
- **Status**: Needs anonymous support (DOM2-6616 - Blocker)
- **Issue**: Discounts Service flows need to support anonymous calls
- **Impact**: Blocks anonymous discount functionality

### Billing Service
- **Status**: Needs anonymous support (DOM2-6617 - Blocker)
- **Issue**: PreviewOrder implementation needs to support anonymous calls
- **Impact**: Blocks anonymous checkout preview

## Technology Stack

### Language and Framework
- **Language**: Java/Kotlin (typical for Wix backend services)
- **Framework**: Spring Boot (assumed, typical for Wix services)
- **Architecture**: Microservices architecture

### Key Patterns
- **Polymorphism**: For anonymous/authenticated flow separation
- **Service Layer**: Business logic separation
- **Entity Management**: Database abstraction
- **Mapper Pattern**: DTO to domain model conversion

## Code Organization

### Service Structure
```
premium-server/premium-cart/
├── CartService (interface)
├── CartServiceImpl (implementation)
├── CartSdl (SDL/resolver layer)
├── CartEntityManager (entity management)
├── BuyerInfoDomain (buyer information)
├── CartIdentityExtractor (identity extraction)
├── ValidationsEntricher (validation enrichment)
└── Mappers (DTO mapping)
```

### Refactoring Progress

1. ✅ **Cart Identity Extractor**: Expanded (DOM2-6597 - PR Pending)
2. ✅ **BuyerInfoDomain**: Expanded (DOM2-6596 - PR Pending)
3. 🔄 **CartSdl Polymorphism**: In Progress (DOM2-6598)
4. ⏳ **CartEntityManager Polymorphism**: Backlog (DOM2-6599)
5. ⏳ **CartService Extraction**: Backlog (DOM2-6605)
6. ⏳ **CartService Router**: Backlog (DOM2-6606)

## Dependencies

### Internal Services
- **Validations Service**: For cart validation rules
- **Discounts Service**: For discount application (needs anonymous support)
- **Billing Service**: For order preview (needs anonymous support)

### External Dependencies
*To be populated from repository analysis when access is available*

## Testing

### Test Requirements
- Anonymous cart creation and management
- Anonymous to authenticated transition
- Anonymous cart expiration
- Anonymous discount application
- Anonymous validation rules

### Test Infrastructure
*To be populated from repository analysis*

## Analysis Status

**Status**: Analysis based on Jira issues and project context  
**Access**: Repository is private (wix-private), read-only analysis only  
**Next Steps**: 
1. Direct repository access for detailed code analysis
2. Extract actual dependency information from build files
3. Document code patterns and conventions
4. Document architecture decisions and rationale

## Important Notes

- This repository remains in its original location (wix-private/premium)
- This file contains only analysis and documentation extracted from Jira issues and project context
- No code has been moved or copied from the original repository
- All analysis is read-only
