# Backend Repository Analysis - Premium Cart

## Source

**Repository**: premium-server/premium-cart  
**URL**: https://github.com/wix-private/premium/blob/6f4fed7906410a9b9d7c05e782dbba67dbabec5a/premium-server/premium-cart  
**Status**: Read-Only Analysis

## Repository Overview

This repository contains the backend cart service implementation for the premium/premium-server codebase.

## Key Components

### Cart Service
- **CartService**: Main cart service interface/implementation
- **CartServiceImpl**: Service implementation (to be extracted per DOM2-6605)
- **CartSdl**: Cart SDL implementation (polymorphism to be implemented per DOM2-6598)
- **CartEntityManager**: Entity manager for cart operations (polymorphism per DOM2-6599)

### Identity and Info
- **BuyerInfoDomain**: Buyer information domain (to be expanded per DOM2-6596)
- **Cart Identity Extractor**: Identity extraction logic (to be expanded per DOM2-6597)

### Validation
- **ValidationsEntricher**: Cart validation enrichment (to be expanded per DOM2-6602)
- **Validations Service**: Validation service (anonymous validations to be added per DOM2-6603)

### Mappers
- **CartService Mappers**: Mappers for cart operations (to be fixed for anonymous per DOM2-6613)

## Anonymous Flow Support

### Current State
- Anonymous cart support is being implemented
- Polymorphism patterns are being added for anonymous/authenticated flows

### Planned Changes
- Anonymous expiration configuration (30 days) - DOM2-6607
- Anonymous line item discounts design - DOM2-6608
- Anonymous discounts implementation - DOM2-6609
- Anonymous validation sets - DOM2-6603

## Integration Points

### Discounts Service
- Needs to support anonymous calls (DOM2-6616 - Blocker)

### Billing Service
- PreviewOrder needs anonymous support (DOM2-6617 - Blocker)

## Analysis Status

**Status**: Placeholder - Repository analysis pending  
**Next Steps**: 
1. Analyze repository structure
2. Document code patterns
3. Extract dependency information
4. Document architecture decisions

## Important Note

This repository remains in its original location (wix-private/premium). This file contains only analysis and documentation extracted from the repository. No code has been moved or copied.
