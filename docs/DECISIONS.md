# AgriParcel01 — Project Decisions

## Project
Satellite-based agricultural field and crop identification for Tirunelveli District.

## Official Problem
Differentiate land parcels and identify/differentiate paddy and banana cultivation in Tirunelveli District, covering Ambasamudram Taluk and Cheranmahadevi Taluk, using openly available satellite imagery.

Minimum study area: 20 sq. km.

---

## Decision Status

- LOCKED = agreed and must not be changed casually
- PROPOSED = suggested but not yet tested
- OPEN = decision still pending
- VERIFY = must be confirmed using real data/testing
- SUPERSEDED = replaced by a newer decision

---

## LOCKED

### Crop Classes

The classification system will use:

1. Paddy
2. Banana
3. Other
4. Uncertain

### Baseline Model

Random Forest will be the baseline machine-learning classifier.

### Core Principle

The satellite-derived agricultural map is the primary technical product.

The verification-support dashboard is an application built on top of that result.

### Terminology

Technical documentation:
- image-derived agricultural field object

Application UI:
- Field Object

Presentation:
- parcel-like agricultural object

The system will not claim cadastral, ownership, legal-parcel, or survey-grade accuracy.

### Validation

Validation must be spatially separated where practical.

Accuracy will not be reported without describing:
- reference data
- analysis period
- split methodology
- class distribution
- uncertainty/evidence limitations

### Area Calculation

Area calculations must use an appropriate projected coordinate reference system.

### Verification Language

The system will not label a discrepancy as fraud.

Allowed terminology:
- Difference
- Relative Difference
- Discrepancy for Review
- Insufficient Evidence
- Uncertain

"Verified" is reserved for human/government review.

### Offline-First Demonstration

Processed imagery, model outputs, field objects and results should be available locally so the demonstration does not depend on live satellite processing.

---

## PROPOSED

### Satellite Source

Sentinel-2 Level-2A is the primary candidate because of its open availability and multispectral observations.

The exact acquisition/access mechanism will be selected during the data audit.

### Feature Strategy

Potential features include:
- Sentinel-2 spectral bands
- NDVI
- useful red-edge features
- water-related indices where useful
- temporal mean
- temporal minimum
- temporal maximum
- temporal standard deviation
- temporal amplitude
- valid observation count

Only features supported by the actual data will be used.

### Segmentation

A lightweight segmentation approach will be tested on actual imagery.

Candidate approaches may include:
- SLIC
- Felzenszwalb
- watershed
- edge-based segmentation

The final method will be selected from actual results.

---

## OPEN

- Exact AOI geometry
- Exact satellite acquisition dates
- Cloud/quality thresholds
- Final agricultural-mask method
- Final segmentation method
- Reference-label source
- Final validation split
- Evidence-quality thresholds
- Declaration-comparison thresholds

These must be resolved using real data and testing.

---

## NON-GOALS

The 24-hour prototype will NOT attempt:

- cadastral/legal parcel verification
- ownership verification
- fraud detection
- yield prediction
- crop disease prediction
- nationwide agricultural mapping
- live satellite processing
- deep-learning segmentation
- government database integration
- Aadhaar integration
- production-scale infrastructure
- Kubernetes/microservices
- PostGIS unless later proven necessary

---

## Development Rule

Every stage follows:

BUILD → TEST → SAVE → COMMIT → PRESENTABLE CHECKPOINT

No fabricated satellite results, accuracy values, cloud statistics, or classification results will be used.