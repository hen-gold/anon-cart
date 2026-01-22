# Master Document Summary

## Source

**Document**: Domains Storefront 2.0 Cart - Master Document  
**URL**: https://docs.google.com/document/d/1WaJH6C4jCMAqGaF-UoUGPFtkieWxfASaTZBMRUfi0mM/edit?tab=t.0#heading=h.9fn2zifgpfz6  
**Owner**: Tal Soffer Nachshon | Product  
**Status**: WIP

## Overview

This master document contains comprehensive specifications for the Domains Storefront 2.0 Cart implementation, focusing on anonymous cart functionality and the new purchase flow experience.

## Key Sections

### Product Experimentation Requirements

This initiative introduces a new purchase flow experience, with a global cart for anonymous users, designed to work consistently across multiple storefronts, including Domains and Business Email (and future more entry points).

### Cart Actions and Use Cases

#### Item Presence States (Valid Combinations)

Given constraints (single domain, single premium, single business email, privacy depends on domain):
- Domain can exist alone or with Premium/Business Email
- Premium and Business Email can exist together or separately
- Privacy add-on depends on domain presence

#### Entry Points

**EP1. User completed selections in flow and lands in Full Cart**
- Cart loads with chosen items and configuration (plan tier, cycles, seats, privacy state)
- If any promo/eligibility changed since selection, show a cart-level notice (see Promo section) - TBD with engs

**EP2. User navigates to Full Cart via Mini Cart CTA**
- Preserve state from mini cart, but always reprice on open

**EP3. User taps a cart item (deep link / jump to cart section)**
- Reprice, change eligibility, check domain eligibility and show a cart-level notice

### Cart Actions

#### Remove Item
Applies to: Domain, Premium, Business Email, Privacy

#### Edit Item
- Change domain billing cycle (1/2/3/5/10 years) - reprice domain and savings
- TLD supports 1 year cycle only - communicate it to the user, remove cycle savings promo

#### Upsell Logic - Add Items (from within cart)
- If premium was removed in this session, show an upsell to premium
- Additional upsell opportunities based on cart contents

### Promotions, Eligibility, and Pricing Edge Cases

#### Domain in Cart Is No Longer Available
- Marks domain as unavailable
- Message: "This domain is no longer available - The domain in your cart has been taken and can't be purchased anymore."

### User Authentication Flow

#### Example Flow: Search → Results → Split → Package picker → Login happens here

**Expected behavior:**
- Immediately revalidate prices, promotions and eligibility (voucher, discounts)
- Carry updated data silently - if the user continues making selections, they're already interacting with the updated state
- Display a message first time the user lands on the Full Cart

#### User Logs In Right Before Checkout

**Happy path**: Cart → Login → Domain Contact Info → Checkout

**Expected behavior:**
- On login success - revalidate cart immediately in the background
- If there are any changes in the cart, display the cart after login
- Flow: Cart → Login → Return to Cart (updated) → Contact info → Checkout

### Entry Points & Navigation

#### Open Mini Cart
- Accessed via the cart icon
- The cart icon is persistent across Storefront (from home until signup)
- The Mini Cart is never opened automatically during the flow

#### Primary CTA – Continue
- Label adapts to the funnel stage
- Closes the Mini Cart and returns the user to continue selections in the flow

## Architecture Considerations

### Anonymous Cart
- Global cart for anonymous users
- Works consistently across multiple storefronts
- 30-day expiration for anonymous carts
- Support for anonymous discounts and promotions

### Service Integration
- Cart service with polymorphic design (anonymous/authenticated)
- Validation service with anonymous validation sets
- Discount service supporting anonymous calls
- Billing service PreviewOrder for anonymous

### State Management
- Cart state preservation across navigation
- Repricing on cart open
- Eligibility revalidation on login
- Silent state updates with user notification

## Implementation Notes

### Key Requirements
1. **Continuity**: Seamless flow with clear progress tracking
2. **Transparency**: Clear pricing and value communication at every step
3. **User Control**: Cart views, ability to review before committing
4. **Delight**: Meaningful success moments and clear completion
5. **Scalability**: Support for anonymous users and future expansion

### Technical Considerations
- Anonymous cart expiration (30 days)
- Anonymous discount support
- Anonymous validation sets
- Cart identity extraction
- Polymorphic cart service design

## Related Links

- [Figma Designs](https://figma.com) - Design specifications
- [FED Tech Design](https://coda.io/d/matanlas-wix-coms-Coda-Playground_dI2LrngbVKN/Anonymous-Cart-FED-Tech-Design_suW2-E-2#_lu8liGCT)
- [Jira Epic DOM2-6162](https://wix.atlassian.net/browse/DOM2-6162)

## Processing Status

- **Status**: Key sections extracted
- **Size**: ~2.4MB original document
- **Format**: Google Docs JSON
- **Last Updated**: Document is WIP (Work In Progress)

## Access

The full document is available at the URL above (read-only access). This summary contains key sections extracted for context-driven development purposes.
