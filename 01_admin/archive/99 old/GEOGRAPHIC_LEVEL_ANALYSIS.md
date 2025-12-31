# Geographic Level Analysis - All Data Sources

**Date:** October 26, 2025
**Analysis:** What data is available at municipal level vs. regional/national

---

## DATA AVAILABILITY BY GEOGRAPHIC LEVEL

### 1. INSTITUTIONAL LEVEL (Finest Granularity)
**Source:** SNS Transparency Portal
- **Coverage:** 426 unique healthcare institutions
- **Data:** All hospital financial, operational, and quality indicators
- **Mapping:** Institutions can be mapped to municipalities/regions

---

### 2. MUNICIPAL LEVEL (336 Portuguese Municipalities)
**Source:** INE (Statistics Portugal)

| Indicator | Records | Status |
|-----------|---------|--------|
| ✅ Population by Age/Sex | 19,608 | MUNICIPAL |
| ✅ Aging Index | 344 | MUNICIPAL |
| ✅ Elderly Dependency Index | 344 | MUNICIPAL |
| ✅ Total Dependency Ratio | 344 | MUNICIPAL |
| ✅ Nurses per 1000 Inhabitants | 344 | MUNICIPAL |

**Total Municipal-Level Indicators from INE: 5**

---

### 3. NUTS 3 LEVEL (27-40 Regions)
**Source:** Eurostat

| Indicator | PT Regions | NUTS 3 Codes | Status |
|-----------|------------|--------------|--------|
| ✅ Regional GDP | 27 | PT111-PT11E, etc. | NUTS 3 |
| ✅ Population by Age/Sex | 40 | PT111-PT11E, etc. | NUTS 3 |
| ✅ Fertility Indicators | 40 | PT111-PT11E, etc. | NUTS 3 |
| ✅ Employment | 27 | PT111-PT11E, etc. | NUTS 3 |

**Total NUTS 3 Indicators from Eurostat: 4**

---

### 4. NUTS 2 LEVEL (7-12 Regions)
**Sources:** INE + Eurostat

**From INE:**
| Indicator | Regions | Status |
|-----------|---------|--------|
| Fertility Index | 30 | REGIONAL |
| Adolescent Fertility Rate | 30 | REGIONAL |
| Unemployment Rate | 11 | NUTS 2 |
| Employment Statistics | 9 | NUTS 2 |

**From Eurostat:**
| Indicator | PT Regions | Status |
|-----------|------------|--------|
| Hospital Beds | 9 | NUTS 2 |
| Physicians | 12 | NUTS 2 |
| Mortality Rate | 7 | NUTS 2 |
| Unemployment Rate | 12 | NUTS 2 |

**Total NUTS 2 Indicators: 8**

---

### 5. NATIONAL LEVEL
**Sources:** INE + Eurostat

| Indicator | Source | Status |
|-----------|--------|--------|
| Life Expectancy at 65 | INE | National only (1 record) |
| Life Expectancy | Eurostat | National (1 PT record) |

---

## MISSING AT MUNICIPAL LEVEL

### Data Types NOT Available at Municipal Level:

#### ECONOMIC INDICATORS:
| Indicator | Best Available | Gap |
|-----------|---------------|-----|
| **Regional GDP** | ❌ NUTS 3 (Eurostat) | Not available at municipal level |
| **Unemployment Rate** | ❌ NUTS 2 (INE/Eurostat) | Not available at municipal level |
| **Employment Statistics** | ❌ NUTS 2/3 (INE/Eurostat) | Not available at municipal level |

#### FERTILITY & DEMOGRAPHICS:
| Indicator | Best Available | Gap |
|-----------|---------------|-----|
| **Fertility Index** | ❌ NUTS 2/3 (INE/Eurostat) | Not available at municipal level |
| **Adolescent Fertility** | ❌ NUTS 2/3 (INE/Eurostat) | Not available at municipal level |

#### HEALTHCARE INFRASTRUCTURE:
| Indicator | Best Available | Gap |
|-----------|---------------|-----|
| **Hospital Beds** | ❌ NUTS 2 (Eurostat) | Not available at municipal level |
| **Physicians** | ❌ NUTS 2 (Eurostat) | Not available at municipal level |

#### HEALTH OUTCOMES:
| Indicator | Best Available | Gap |
|-----------|---------------|-----|
| **Mortality Rate by Cause** | ❌ NUTS 2 (Eurostat) | Not available at municipal level |
| **Life Expectancy** | ❌ National (INE/Eurostat) | Not available at municipal level |

---

## WHY CERTAIN DATA IS NOT AVAILABLE AT MUNICIPAL LEVEL

### Statistical Reasons:
1. **Small Population Size**
   - Many Portuguese municipalities have < 10,000 inhabitants
   - Economic indicators (GDP, employment) unreliable at this level
   - Statistical disclosure control (privacy concerns)

2. **Data Collection Methodology**
   - GDP calculated using regional economic accounts (NUTS 2/3)
   - Labor force surveys use regional samples (not municipal)
   - Hospital infrastructure data collected at facility level (then aggregated to NUTS 2)

3. **Administrative Structure**
   - Healthcare services often organized at regional level (NUTS 2)
   - Employment statistics follow labor market areas (larger than municipalities)

### Data Availability Check Across All Sources:

| Data Type | INE Municipal | INE Regional | Eurostat NUTS 3 | Eurostat NUTS 2 | SNS Institutional |
|-----------|---------------|--------------|-----------------|-----------------|-------------------|
| GDP | ❌ | ❌ | ✅ (27) | ✅ (10) | ❌ |
| Unemployment | ❌ | ✅ (11) | ❌ | ✅ (12) | ❌ |
| Employment | ❌ | ✅ (9) | ✅ (27) | ❌ | ❌ |
| Hospital Beds | ❌ | ❌ | ❌ | ✅ (9) | ✅ (426) |
| Physicians | ❌ | ❌ | ❌ | ✅ (12) | ❌ |
| Nurses | ✅ (336) | ❌ | ❌ | ❌ | ✅ (426) |
| Mortality | ❌ | ❌ | ❌ | ✅ (7) | ✅ (426) |
| Population | ✅ (336) | ❌ | ✅ (40) | ✅ (12) | ❌ |
| Aging | ✅ (336) | ❌ | ❌ | ❌ | ❌ |
| Fertility | ❌ | ✅ (30) | ✅ (40) | ✅ (12) | ❌ |

---

## CONCLUSION: WHAT CAN BE DONE

### Available Data by Level:

#### MUNICIPAL (336 municipalities) - INE:
✅ Population demographics (age, sex)
✅ Aging indicators
✅ Dependency ratios
✅ Nurses per capita

#### NUTS 3 (27-40 regions) - Eurostat:
✅ Regional GDP ⭐ (BEST ECONOMIC INDICATOR AVAILABLE)
✅ Population demographics
✅ Fertility indicators
✅ Employment

#### NUTS 2 (7-12 regions) - INE + Eurostat:
✅ Unemployment rate
✅ Hospital beds
✅ Physicians
✅ Mortality by cause
✅ Fertility

#### INSTITUTIONAL (426 entities) - SNS:
✅ Financial data
✅ Operational metrics
✅ Quality indicators
✅ Staffing levels

### Recommended Approach:

**For analyses requiring municipal-level granularity:**
1. Use INE municipal data (population, aging, dependency, nurses)
2. Supplement with NUTS 3 data from Eurostat (GDP, employment)
3. Map hospitals to municipalities using entity location data
4. Aggregate NUTS 2/3 data to municipal level using population weights (if needed)

**For regional economic analysis:**
1. Use Eurostat NUTS 3 GDP (27 regions) ⭐
2. Use Eurostat NUTS 2/3 employment and unemployment
3. These provide sufficient regional variation for analysis

**Multi-Level Modeling:**
- Level 1: Hospitals (426 entities)
- Level 2: Municipalities (336) or NUTS 3 (27-40)
- Level 3: NUTS 2 (7-12)
- Control variables at appropriate levels

---

## DATA THAT CANNOT BE OBTAINED AT MUNICIPAL LEVEL

### Definitively Not Available:
1. **Municipal GDP** - Not calculated by any Portuguese/EU agency
2. **Municipal Unemployment Rate** - Sample size too small
3. **Municipal Hospital Beds/Physicians** - Aggregated to NUTS 2 only
4. **Municipal Mortality by Cause** - Privacy concerns, small numbers

### Best Alternatives:
1. **For Municipal GDP:**
   - Use NUTS 3 GDP (27 regions) from Eurostat
   - Proxy with municipal tax revenue (if available from finance ministry)
   - Use business establishment counts (if available)

2. **For Municipal Unemployment:**
   - Use NUTS 2 rates (11-12 regions) from INE/Eurostat
   - Apply spatial interpolation if needed
   - Use registered unemployment data (may be available at municipal level from employment office)

3. **For Healthcare Infrastructure:**
   - Use SNS institutional data (426 facilities)
   - Aggregate to municipal level manually
   - Use NUTS 2 data as regional controls

4. **For Mortality:**
   - Use SNS hospital mortality data (426 facilities)
   - Use NUTS 2 standardized death rates (7 regions)
   - Request municipal vital statistics from INE (may require special permission)

---

## SUMMARY

### Data Coverage Assessment:

**Excellent Coverage (Municipal):**
- ✅ Demographics (population, age structure)
- ✅ Aging indicators
- ✅ Nurses per capita

**Good Coverage (NUTS 3):**
- ✅ Regional GDP ⭐
- ✅ Employment
- ✅ Fertility

**Adequate Coverage (NUTS 2):**
- ✅ Unemployment
- ✅ Hospital infrastructure
- ✅ Physicians
- ✅ Mortality

**Limited Coverage (National):**
- ⚠️ Life expectancy (national only)

### Gap Analysis:

**Critical Gaps:** None - all essential variables available at NUTS 2 or finer
**Minor Gaps:** GDP at municipal level (not available anywhere, use NUTS 3)
**Workarounds:** Available for all gaps using spatial aggregation or institutional data

### Research Impact:

**Your research can proceed with:**
- Hospital-level analysis (426 institutions) ✅
- Municipal context (336 municipalities for demographics) ✅
- Regional economic context (27-40 NUTS 3 regions for GDP) ✅
- Healthcare system analysis (7-12 NUTS 2 regions) ✅

**No critical data is missing** - you have sufficient geographic granularity for rigorous analysis.

---

**Generated:** October 26, 2025
**Conclusion:** All essential data available at appropriate geographic levels. Municipal GDP not available (use NUTS 3). Healthcare infrastructure at NUTS 2 (appropriate level for health system organization).
