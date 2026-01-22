# DOM2-6598 - Implement polymorphism for CartSdl

## Track Overview

- **Key**: DOM2-6598
- **Summary**: [BED] - Implement polymorphism for CartSdl
- **Status**: In Progress
- **Priority**: High
- **Story Points**: 2
- **Assignee**: Shahar Itzko
- **Epic**: DOM2-6162 - SF Purchase Flow

## Description

Implement polymorphism pattern for CartSdl to support both anonymous and authenticated cart flows.

## Related Files

- [spec.md](spec.md) - Requirements and acceptance criteria
- [plan.md](plan.md) - Implementation plan
- [metadata.json](metadata.json) - Track metadata

## Context

This track is part of the backend refactoring to support anonymous cart functionality. The CartSdl needs to be refactored to use polymorphism patterns similar to other cart components.

## Dependencies

- Related to DOM2-6599 (CartEntityManager polymorphism)
- Related to DOM2-6605 (CartService extraction)
- Related to DOM2-6606 (CartService router refactoring)
