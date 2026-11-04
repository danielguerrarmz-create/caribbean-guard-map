# Unified beach safety and spacing refinement

Date: 2026-11-03
Status: local review. No commit, push or deployment.

## What changed

- One safety component contains the existing beach instruction, clock-driven lifeguard hours, attendance caveat and expandable Safety details. Removed the redundant status icon and the separate repeated advisory above the forecast.
- Storm escalation remains visible in the same safety component. Advisory refresh preserves the disclosure state. Safety evaluator and schedule semantics are unchanged.
- Established 32 px section spacing around a hairline between emergency guidance and forecast. Fixed missing coastal palette variables on zone-detail, which previously invalidated divider colors.
- Forecast disclosure has an explicit View forecast sources & limitations action, chevron, 56 px minimum row, 24 px chart gap and 32 px following-section gap.
- Refined mobile Back text, 44 px target and spacing below the drag handle. Increased segmented-control labels to 15 px. Scrollbar-free mobile behavior remains.

## Why

Repeated lifeguard instructions competed for attention, while a decorative icon consumed space without adding meaning. Accumulated spacing rules and a missing color variable made section boundaries inconsistent.

## How to verify

Open http://127.0.0.1:5174/mobile-preview.html and select Playa Cocles, or http://127.0.0.1:5174/?z=cocles on desktop. Confirm one safety component and no left-hand status icon. Expand Safety details, refresh the forecast and confirm it stays open. Expand View forecast sources & limitations, then collapse it. Review emergency-to-forecast spacing and mobile Back/handle separation.

## Validation

52 Node tests, copy checks and the 549-asset offline build pass. Cocles reviewed in the 390 x 844 mobile frame and 1031 x 859 desktop. Verified one advisory, no repeated confirmation title, retained expanded safety details through refresh, and functioning forecast disclosure. No mobile console errors observed.

Proofs: out/visual-review/cocles-refined-mobile.png, cocles-refined-forecast-mobile.png, cocles-refined-desktop.png.

## What's left

User visual review and physical-device release checks.

## Files touched

web/index.html, web/coastal-panels.css, web/sw.js (cache v64), this handoff and proof captures. Burondono local docs/references/coastal-panels updated with CSS, README and beach-safety.js consumer reference.
