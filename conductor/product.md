# Product Vision

## Product Overview

**Product Name**: Storefront Purchase Flow  
**Epic**: DOM2-6162 - SF Purchase Flow  
**One-line Description**: Rebuild the Storefront purchase flow to create a modern, intuitive, and scalable purchase experience.

## Problem Statement

The current Storefront purchase flow has significant issues that impact user experience and conversion:

### Main Issues in Current Flow

1. **The flow lacks continuity and orientation**, with multiple context jumps, no progress tracking, and visual inconsistencies that reduce trust.

2. **Key e-commerce expectations are broken**, from missing cart views to premature login, creating confusion and slowing decision making.

3. **Users are pushed through repeated and disjointed purchase moments**, creating fatigue and weakening the overall purchase experience.

4. **Success moments lack delight and clarity**, reducing the sense of progress and completion.

5. **The final landing in the dashboard is confusing and underwhelming**, especially for new users.

## Solution Approach

Rebuild the purchase flow with focus on:

- **Continuity**: Seamless flow with clear progress tracking
- **Transparency**: Clear pricing and value communication at every step
- **User Control**: Cart views, ability to review before committing
- **Delight**: Meaningful success moments and clear completion
- **Scalability**: Support for anonymous users and future expansion

## Phases

Phases are still TBD, but initial planning includes:

- **Phase 1**: Single domain purchase
- **Phase 2**: Domain + brand protection bundle
- **Phase 3**: Multiple domains

## Target Users

- **Primary**: New users purchasing domains through Storefront
- **Secondary**: Existing users adding domains
- **Focus**: Anonymous users (enabling purchase without authentication)

## Core Features and Capabilities

### Anonymous Cart Flow
- Anonymous cart functionality
- Package pickers (Premium, Mailbox)
- Cart page with validations
- MiniCart integration
- Success pages

### Backend Infrastructure
- Polymorphic cart service (anonymous/authenticated)
- Anonymous validations
- Anonymous discounts support
- Cart expiration (30 days for anonymous)

### User Experience
- Split page functionality
- Business email in cart flows
- Recommendation upsells
- Contact form integration
- Progress tracking and orientation

## Success Metrics and KPIs

### Key Learnings from Previous Cart Sessions

1. **Clarity**: Users need absolute clarity on the process, context, and position in the journey, especially when transitioning from premium plan purchase to domain flow.

2. **Real Numbers**: Always test flows with real numbers to understand true cost to users and how pricing escalates with each selection.

3. **Transparent Pricing**: The one-year free domain offer must be explicitly communicated because multi-year registrations, privacy add-ons, and promotions can quickly inflate pricing.

4. **Clear KPIs**: Set clear KPIs to measure success and define what we're optimizing for in each test.

5. **Structured Testing**: Create a structured "what if" strategy to layer tests gradually so that every experiment has a fallback path.

## Product Roadmap

### Current Status
- **Progress**: 10% complete
- **Done**: 4 items (UX research, cart vision, dev design, monorepo setup)
- **In Progress**: 3 items (SF cart flow, anonymous tests, CartSdl polymorphism)
- **PR Pending**: 4 items
- **Backlog**: 30 items

### Key Themes
1. Anonymous user flow: enabling purchase without authentication
2. Cart infrastructure: refactoring to support anonymous and authenticated flows
3. Premium package picker integration: Eclipse components for Storefront
4. Discounts and pricing: anonymous discount support and transparent pricing
5. User experience: improving flow continuity, progress tracking, and success moments

## Relevant Links

- [SF Strategy](https://docs.google.com/presentation/d/1AswC4QkW0EOczC3BD4FRRQTbFI_Wt6pdeU4KFBuSNdQ/edit?usp=sharing)
- [Competitive Analysis (Laura)](https://docs.google.com/presentation/d/1byWeYl7jZUMzqY7smxq0O_VdcOzE02NF6LM87laqbA4/edit?usp=sharing)
- [Cart Documentation](https://docs.google.com/document/d/1h5ASyHohbEIJLVQx3-KYqMT-fvEAK-bzjT7Vrcs_rDk/edit?usp=sharing)
- [FED Tech Design](https://coda.io/d/matanlas-wix-coms-Coda-Playground_dI2LrngbVKN/Anonymous-Cart-FED-Tech-Design_suW2-E-2#_lu8liGCT)
