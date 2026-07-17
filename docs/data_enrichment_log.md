# Data Enrichment Log

Documents every record added to the starter dataset during Task 1.

## New Observations

### Fayda Digital ID Enrollment (2025-09-01)
- **Value:** 25000000 people
- **Pillar:** ACCESS
- **Source:** [Shega News](https://shega.co/news/fayda-digital-id-to-become-mandatory-for-banking-services-as-ethiopia-begins-nationwide-account-harmonization)
- **Original text:** "As of September 2025, Fayda digital ID enrollment stands at 25 million"
- **Confidence:** high
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Replaces earlier non-approved source; Shega is on the approved Ethiopia source list.

### Total Bank Accounts and Mobile Wallets (2025-09-01)
- **Value:** 272000000 accounts
- **Pillar:** USAGE
- **Source:** [Shega News](https://shega.co/news/fayda-digital-id-to-become-mandatory-for-banking-services-as-ethiopia-begins-nationwide-account-harmonization)
- **Original text:** "the number of bank accounts in Ethiopia and mobile wallets had reached 272 million"
- **Confidence:** medium
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Same approved source as above, same article - counts accounts/wallets, not unique users, so treat as a context indicator, not a direct Findex proxy.

### Annual Digital Transaction Value (2024-07-01)
- **Value:** 9700000000000 ETB
- **Pillar:** USAGE
- **Source:** [National Bank of Ethiopia](https://nbe.gov.et/nbe_news/ethiopia-launches-phase-two-of-national-digital-payments-strategy-building-on-strong-momentum-from-phase-one/)
- **Original text:** "In the 2023/24 fiscal year, Ethiopia recorded a substantial 9.7 trillion Birr in digital transactions, exceeding cash transactions"
- **Confidence:** high
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Already an approved nbe.gov.et source - unchanged from before.

## New Events

### NBE Payment Instrument Issuer Interoperability Directive (ONPS/10/2025) (2025-05-12)
- **Record ID:** EVT_0011
- **Category:** regulation
- **Source:** [National Bank of Ethiopia](https://nbe.gov.et/files/onps-10-2025-oversight-of-the-natioanl-payment-system-licensing-and-authorization-of-payment-instrument-issuer-amendment-directive/)
- **Original text:** "Oversight of the National Payment System Licensing and Authorization of Payment Instrument Issuer (Amendment) Directive"
- **Confidence:** high
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Replaces the addisinsight.net citation with the official nbe.gov.et directive page directly.

### National Digital Payments Strategy Phase Two (NDPS 2.0) Launch (2025-04-03)
- **Record ID:** EVT_0012
- **Category:** policy
- **Source:** [National Bank of Ethiopia](https://nbe.gov.et/nbe_news/ethiopia-launches-phase-two-of-national-digital-payments-strategy-building-on-strong-momentum-from-phase-one/)
- **Original text:** "Phase Two of the Strategy (2025-2029) will focus on deepening usage of digital payments, ensuring full interoperability, expanding digital ID integration..."
- **Confidence:** high
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Already an approved nbe.gov.et source - unchanged from before.

### Fayda-Bank Account Mandatory Linkage (Verifayda 2 Migration) (2026-01-08)
- **Record ID:** EVT_0013
- **Category:** policy
- **Source:** [Shega News](https://shega.co/news/fayda-digital-id-to-become-mandatory-for-banking-services-as-ethiopia-begins-nationwide-account-harmonization)
- **Original text:** "Addis Ababa, Dire Dawa, and regional administration capital cities have been given a shorter timeline, with a deadline of January 8, 2026"
- **Confidence:** high
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Replaces the unsourced federal-agency-mandate event with a properly-sourced Fayda/banking event from the approved list.

## New Impact Links

### Links EVT_0011 -> USG_P2P_COUNT
- **Pillar:** USAGE
- **Direction / Magnitude:** increase / high
- **Lag:** 6 months
- **Evidence basis:** literature
- **Confidence:** medium
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Mandatory interoperability removes friction for cross-platform P2P transfers.

### Links EVT_0004 -> ACC_FAYDA
- **Pillar:** ACCESS
- **Direction / Magnitude:** increase / high
- **Lag:** 12 months
- **Evidence basis:** empirical
- **Confidence:** high
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Supported by shega.co-confirmed enrollment growth to 25M by Sept 2025 following the Fayda rollout.

### Links EVT_0013 -> ACC_ACCOUNT_OWNERSHIP
- **Pillar:** ACCESS
- **Direction / Magnitude:** increase / medium
- **Lag:** 3 months
- **Evidence basis:** empirical
- **Confidence:** medium
- **Collected by:** The Project Owner on 2026-07-17
- **Why it's useful:** Mandatory Fayda-bank linkage pushes unregistered account holders to register for Fayda, indirectly reinforcing Access measurement/verification.
