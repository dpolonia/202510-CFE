"""
Analyze ULS (Unidades Locais de Saúde) Structure

Extract and document:
1. Current ULS count (should be 39 ULS + 3 IPO = 42 entities)
2. Former hospitals/centros hospitalares that were incorporated
3. ACES (Agrupamentos de Centros de Saúde) primary care units incorporated
4. Entity name crosswalk for CQMI component construction

Data sources:
- SNS monthly panel
- Quality metrics data
- Financial data

Outputs:
- ULS structure report: 08_documentation/uls_integration_structure.md
- Entity crosswalk: 03_data/processed/crosswalks/entity_name_crosswalk.csv

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "03_data" / "processed"
OUTPUT_DOC = PROJECT_ROOT / "08_documentation"
OUTPUT_CROSSWALK = DATA_PROCESSED / "crosswalks"

OUTPUT_DOC.mkdir(parents=True, exist_ok=True)
OUTPUT_CROSSWALK.mkdir(parents=True, exist_ok=True)


class ULSStructureAnalyzer:
    """
    Analyzes ULS integration structure and creates entity crosswalk.
    """

    def __init__(self):
        self.entities_all = []
        self.uls_entities = []
        self.hospital_entities = []
        self.aces_entities = []
        self.ipo_entities = []
        self.other_entities = []

    def load_all_entities(self):
        """Load entities from all available datasets."""
        logger.info("Loading entities from all datasets...")

        # Monthly panel
        panel_file = DATA_PROCESSED / "panel" / "hospital_month_panel.parquet"
        if panel_file.exists():
            panel = pd.read_parquet(panel_file)
            panel_entities = panel['entidade'].unique().tolist()
            logger.info(f"  Monthly panel: {len(panel_entities)} entities")
            self.entities_all.extend(panel_entities)

        # Quality metrics
        quality_file = DATA_PROCESSED / "quality" / "quality_metrics.parquet"
        if quality_file.exists():
            quality = pd.read_parquet(quality_file)
            # Quality data uses 'instituicao' column
            if 'instituicao' in quality.columns:
                quality_entities = quality['instituicao'].unique().tolist()
            elif 'entidade' in quality.columns:
                quality_entities = quality['entidade'].unique().tolist()
            else:
                quality_entities = []

            logger.info(f"  Quality data: {len(quality_entities)} entities")
            self.entities_all.extend(quality_entities)

        # Financial data
        financial_file = DATA_PROCESSED / "financial" / "agregados-economico-financeiros.parquet"
        if financial_file.exists():
            financial = pd.read_parquet(financial_file)
            if 'entidade' in financial.columns:
                financial_entities = financial['entidade'].unique().tolist()
                logger.info(f"  Financial data: {len(financial_entities)} entities")
                self.entities_all.extend(financial_entities)

        # Remove duplicates
        self.entities_all = list(set(self.entities_all))
        logger.info(f"\nTotal unique entities: {len(self.entities_all)}")

    def classify_entities(self):
        """
        Classify entities into categories:
        - ULS (Unidades Locais de Saúde)
        - IPO (Institutos Portugueses de Oncologia)
        - Hospitals (Centro Hospitalar, Hospital)
        - ACES (Agrupamentos de Centros de Saúde)
        - Other (administrative entities)
        """
        logger.info("\nClassifying entities...")

        for entity in self.entities_all:
            entity_lower = entity.lower()

            # ULS
            if 'unidade local de saúde' in entity_lower or 'unidade local de' in entity_lower:
                self.uls_entities.append(entity)

            # IPO
            elif 'instituto' in entity_lower and ('oncologia' in entity_lower or 'portugues' in entity_lower):
                self.ipo_entities.append(entity)

            # Hospitals
            elif any(keyword in entity_lower for keyword in ['hospital', 'centro hospitalar', 'ch ']):
                self.hospital_entities.append(entity)

            # ACES (Primary care)
            elif 'aces' in entity_lower or 'agrupamento de centros de saúde' in entity_lower:
                self.aces_entities.append(entity)

            # Administrative
            elif any(keyword in entity_lower for keyword in ['administração', 'serviço nacional']):
                self.other_entities.append(entity)

            # Other
            else:
                self.other_entities.append(entity)

        logger.info(f"\nClassification results:")
        logger.info(f"  ULS: {len(self.uls_entities)}")
        logger.info(f"  IPO: {len(self.ipo_entities)}")
        logger.info(f"  Hospitals/Centros Hospitalares: {len(self.hospital_entities)}")
        logger.info(f"  ACES: {len(self.aces_entities)}")
        logger.info(f"  Other: {len(self.other_entities)}")

    def extract_uls_names(self):
        """Extract and display all ULS names."""
        logger.info("\n" + "="*70)
        logger.info("UNIDADES LOCAIS DE SAÚDE (ULS)")
        logger.info("="*70)

        # Sort alphabetically
        uls_sorted = sorted(self.uls_entities)

        for i, uls in enumerate(uls_sorted, 1):
            logger.info(f"{i:2d}. {uls}")

        # Extract geographic location from ULS name
        logger.info("\nGeographic distribution:")
        regions = {}
        for uls in uls_sorted:
            # Extract location (word after "de" or "do")
            match = re.search(r'de\s+([\w\s]+?),?\s*E\.?P\.?E?\.?', uls, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                regions[location] = regions.get(location, 0) + 1

        for region, count in sorted(regions.items()):
            logger.info(f"  {region}: {count}")

    def extract_ipo_names(self):
        """Extract and display all IPO names."""
        logger.info("\n" + "="*70)
        logger.info("INSTITUTOS PORTUGUESES DE ONCOLOGIA (IPO)")
        logger.info("="*70)

        ipo_sorted = sorted(self.ipo_entities)

        for i, ipo in enumerate(ipo_sorted, 1):
            logger.info(f"{i}. {ipo}")

    def verify_counts(self):
        """Verify entity counts match expected structure (39 ULS + 3 IPO)."""
        logger.info("\n" + "="*70)
        logger.info("VERIFICATION")
        logger.info("="*70)

        expected_uls = 39
        expected_ipo = 3

        logger.info(f"\nExpected structure (as of 2024 reform):")
        logger.info(f"  ULS: {expected_uls}")
        logger.info(f"  IPO: {expected_ipo}")
        logger.info(f"  Total core entities: {expected_uls + expected_ipo}")

        logger.info(f"\nFound in data:")
        logger.info(f"  ULS: {len(self.uls_entities)}")
        logger.info(f"  IPO: {len(self.ipo_entities)}")
        logger.info(f"  Total: {len(self.uls_entities) + len(self.ipo_entities)}")

        if len(self.uls_entities) == expected_uls:
            logger.info(f"\n✓ ULS count matches expected ({expected_uls})")
        else:
            logger.warning(f"\n⚠ ULS count mismatch: Found {len(self.uls_entities)}, expected {expected_uls}")
            logger.warning(f"  Difference: {len(self.uls_entities) - expected_uls}")

        if len(self.ipo_entities) == expected_ipo:
            logger.info(f"✓ IPO count matches expected ({expected_ipo})")
        else:
            logger.warning(f"⚠ IPO count mismatch: Found {len(self.ipo_entities)}, expected {expected_ipo}")

    def identify_pre_integration_hospitals(self):
        """
        Identify hospitals/centros hospitalares that existed before ULS integration.

        These are hospitals that appear in early data (2017-2020) but may have been
        incorporated into ULS post-2024.
        """
        logger.info("\n" + "="*70)
        logger.info("PRE-INTEGRATION HOSPITALS & CENTROS HOSPITALARES")
        logger.info("="*70)

        hospital_sorted = sorted(self.hospital_entities)

        logger.info(f"\nFound {len(hospital_sorted)} hospital entities:")
        for i, hospital in enumerate(hospital_sorted, 1):
            logger.info(f"{i:3d}. {hospital}")

        # These may be pre-2024 entities that were incorporated into ULS
        logger.info(f"\nNOTE: These {len(hospital_sorted)} hospital entities likely represent:")
        logger.info(f"  1. Historical entities (2017-2023) before ULS integration")
        logger.info(f"  2. Entities incorporated into the 39 ULS in 2024")
        logger.info(f"  3. Specialized hospitals not yet integrated")

    def create_entity_crosswalk(self):
        """
        Create entity name crosswalk for mapping pre-2024 to post-2024 entities.

        This is CRITICAL for CQMI component construction.
        """
        logger.info("\n" + "="*70)
        logger.info("CREATING ENTITY CROSSWALK")
        logger.info("="*70)

        crosswalk_data = []

        # Add ULS (post-2024 entities)
        for uls in self.uls_entities:
            crosswalk_data.append({
                'entity_name': uls,
                'entity_type': 'ULS',
                'integration_status': 'Integrated',
                'integration_year': 2024,
                'parent_uls': uls,  # Self-reference for ULS
                'notes': 'Current ULS entity (post-2024)'
            })

        # Add IPO
        for ipo in self.ipo_entities:
            crosswalk_data.append({
                'entity_name': ipo,
                'entity_type': 'IPO',
                'integration_status': 'Independent',
                'integration_year': None,
                'parent_uls': None,
                'notes': 'Instituto Português de Oncologia (specialized cancer center)'
            })

        # Add pre-integration hospitals
        for hospital in self.hospital_entities:
            crosswalk_data.append({
                'entity_name': hospital,
                'entity_type': 'Hospital/Centro Hospitalar',
                'integration_status': 'Unknown',  # Needs manual verification
                'integration_year': None,
                'parent_uls': None,  # TO BE MAPPED
                'notes': 'Pre-2024 entity - requires manual mapping to parent ULS'
            })

        # Add ACES
        for aces in self.aces_entities:
            crosswalk_data.append({
                'entity_name': aces,
                'entity_type': 'ACES',
                'integration_status': 'Unknown',
                'integration_year': None,
                'parent_uls': None,
                'notes': 'Primary care grouping - requires manual mapping'
            })

        # Add other
        for other in self.other_entities:
            crosswalk_data.append({
                'entity_name': other,
                'entity_type': 'Administrative',
                'integration_status': 'N/A',
                'integration_year': None,
                'parent_uls': None,
                'notes': 'Administrative entity (not clinical)'
            })

        crosswalk_df = pd.DataFrame(crosswalk_data)

        # Save crosswalk
        output_file = OUTPUT_CROSSWALK / "entity_name_crosswalk.csv"
        crosswalk_df.to_csv(output_file, index=False, encoding='utf-8-sig')

        logger.info(f"\nEntity crosswalk saved: {output_file}")
        logger.info(f"Total entities: {len(crosswalk_df)}")

        # Summary
        logger.info(f"\nCrosswalk summary:")
        logger.info(f"  ULS (integrated): {len(self.uls_entities)}")
        logger.info(f"  IPO (independent): {len(self.ipo_entities)}")
        logger.info(f"  Hospitals (need mapping): {len(self.hospital_entities)}")
        logger.info(f"  ACES (need mapping): {len(self.aces_entities)}")
        logger.info(f"  Administrative: {len(self.other_entities)}")

        logger.info(f"\n⚠ ACTION REQUIRED:")
        logger.info(f"  Manual mapping needed for {len(self.hospital_entities)} hospitals")
        logger.info(f"  Map each pre-2024 hospital to its parent ULS in 'parent_uls' column")

        return crosswalk_df

    def generate_documentation(self, crosswalk_df):
        """Generate comprehensive ULS structure documentation."""
        logger.info("\nGenerating documentation...")

        doc_lines = []
        doc_lines.append("# ULS Integration Structure Analysis")
        doc_lines.append("## Portuguese National Health Service (SNS) Reorganization")
        doc_lines.append("")
        doc_lines.append("**Date**: 2025-12-31")
        doc_lines.append("**Author**: Research Team")
        doc_lines.append("")
        doc_lines.append("---")
        doc_lines.append("")

        # Executive Summary
        doc_lines.append("## Executive Summary")
        doc_lines.append("")
        doc_lines.append(f"The 2024 ULS integration reform consolidated Portuguese public hospitals into:")
        doc_lines.append(f"- **{len(self.uls_entities)} ULS** (Unidades Locais de Saúde)")
        doc_lines.append(f"- **{len(self.ipo_entities)} IPO** (Institutos Portugueses de Oncologia)")
        doc_lines.append(f"- **Total**: {len(self.uls_entities) + len(self.ipo_entities)} core clinical entities")
        doc_lines.append("")
        doc_lines.append(f"This represents consolidation of **{len(self.hospital_entities)} pre-integration hospitals** and **{len(self.aces_entities)} ACES primary care groupings**.")
        doc_lines.append("")

        # ULS List
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append(f"## 1. Unidades Locais de Saúde (ULS) - {len(self.uls_entities)} entities")
        doc_lines.append("")

        for i, uls in enumerate(sorted(self.uls_entities), 1):
            doc_lines.append(f"{i}. {uls}")

        doc_lines.append("")

        # IPO List
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append(f"## 2. Institutos Portugueses de Oncologia (IPO) - {len(self.ipo_entities)} entities")
        doc_lines.append("")

        for i, ipo in enumerate(sorted(self.ipo_entities), 1):
            doc_lines.append(f"{i}. {ipo}")

        doc_lines.append("")

        # Pre-integration entities
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append(f"## 3. Pre-Integration Hospitals & Centros Hospitalares - {len(self.hospital_entities)} entities")
        doc_lines.append("")
        doc_lines.append("These entities existed in 2017-2023 data and were incorporated into ULS in 2024:")
        doc_lines.append("")

        for i, hospital in enumerate(sorted(self.hospital_entities), 1):
            doc_lines.append(f"{i}. {hospital}")

        doc_lines.append("")

        # ACES
        if self.aces_entities:
            doc_lines.append("---")
            doc_lines.append("")
            doc_lines.append(f"## 4. ACES (Primary Care Groupings) - {len(self.aces_entities)} entities")
            doc_lines.append("")

            for i, aces in enumerate(sorted(self.aces_entities), 1):
                doc_lines.append(f"{i}. {aces}")

            doc_lines.append("")

        # Data implications
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append("## 5. Implications for PHFSI Analysis")
        doc_lines.append("")
        doc_lines.append("### Entity Name Mapping Challenge")
        doc_lines.append("")
        doc_lines.append(f"**Problem**: Quality metrics from 2017-2023 use pre-integration hospital names (n={len(self.hospital_entities)}), while post-2024 data uses ULS names (n={len(self.uls_entities)}).")
        doc_lines.append("")
        doc_lines.append("**Solution**:")
        doc_lines.append("1. Manual mapping of pre-2024 hospitals to parent ULS")
        doc_lines.append("2. Create `parent_uls` column in entity crosswalk")
        doc_lines.append("3. Aggregate quality metrics by parent ULS for time-series consistency")
        doc_lines.append("")

        doc_lines.append("### CQMI Component Construction")
        doc_lines.append("")
        doc_lines.append("**Current Status**: CQMI (Clinical Quality Maintenance Index) cannot be calculated due to entity name mismatch.")
        doc_lines.append("")
        doc_lines.append("**Required Actions**:")
        doc_lines.append(f"1. **Complete entity crosswalk**: Map {len(self.hospital_entities)} hospitals to 39 ULS")
        doc_lines.append("2. **Source for mapping**: Use official ACSS decrees or Ministry of Health announcements")
        doc_lines.append("3. **Validation**: Verify all hospitals map to exactly one ULS")
        doc_lines.append("4. **Aggregate quality data**: Sum/average quality metrics by parent ULS")
        doc_lines.append("")

        # Next steps
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append("## 6. Next Steps")
        doc_lines.append("")
        doc_lines.append("### Immediate (Priority 1)")
        doc_lines.append("")
        doc_lines.append("- [ ] **Manual entity mapping**: Assign `parent_uls` for all pre-2024 hospitals")
        doc_lines.append("- [ ] **Data sources**: Search ACSS website, government gazettes, Ministry of Health press releases")
        doc_lines.append("- [ ] **Validation**: Cross-check with SNS organizational charts")
        doc_lines.append("")

        doc_lines.append("### Short-term (Priority 2)")
        doc_lines.append("")
        doc_lines.append("- [ ] **Aggregate quality metrics** by parent ULS")
        doc_lines.append("- [ ] **Calculate CQMI** for all 5 components")
        doc_lines.append("- [ ] **Re-run PHFSI** with complete 5-component index")
        doc_lines.append("")

        doc_lines.append("### Medium-term (Priority 3)")
        doc_lines.append("")
        doc_lines.append("- [ ] **DiD analysis**: Use entity crosswalk to identify treatment timing")
        doc_lines.append("- [ ] **Validate integration dates**: Verify exact month of ULS creation for each entity")
        doc_lines.append("")

        # References
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append("## 7. References")
        doc_lines.append("")
        doc_lines.append("- **ACSS (Administração Central do Sistema de Saúde)**: https://www.acss.min-saude.pt/")
        doc_lines.append("- **Ministry of Health**: https://www.sns.gov.pt/")
        doc_lines.append("- **Government Gazettes (Diário da República)**: https://diariodarepublica.pt/")
        doc_lines.append("")

        # Files
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append("## 8. Related Files")
        doc_lines.append("")
        doc_lines.append(f"- **Entity crosswalk**: `03_data/processed/crosswalks/entity_name_crosswalk.csv` ({len(crosswalk_df)} entities)")
        doc_lines.append(f"- **Monthly panel**: `03_data/processed/panel/hospital_month_panel.parquet`")
        doc_lines.append(f"- **Quality metrics**: `03_data/processed/quality/quality_metrics.parquet`")
        doc_lines.append("")

        # Save documentation
        doc_file = OUTPUT_DOC / "uls_integration_structure.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(doc_lines))

        logger.info(f"Documentation saved: {doc_file}")

        return doc_file

    def run_analysis(self):
        """Execute full ULS structure analysis pipeline."""
        logger.info("="*70)
        logger.info("ULS INTEGRATION STRUCTURE ANALYSIS")
        logger.info("="*70 + "\n")

        # Load entities
        self.load_all_entities()

        # Classify
        self.classify_entities()

        # Extract ULS names
        self.extract_uls_names()

        # Extract IPO names
        self.extract_ipo_names()

        # Verify counts
        self.verify_counts()

        # Identify pre-integration hospitals
        self.identify_pre_integration_hospitals()

        # Create crosswalk
        crosswalk_df = self.create_entity_crosswalk()

        # Generate documentation
        doc_file = self.generate_documentation(crosswalk_df)

        logger.info("\n" + "="*70)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*70)
        logger.info(f"\nOutputs:")
        logger.info(f"  1. Entity crosswalk: 03_data/processed/crosswalks/entity_name_crosswalk.csv")
        logger.info(f"  2. Documentation: 08_documentation/uls_integration_structure.md")
        logger.info(f"\n⚠ CRITICAL ACTION REQUIRED:")
        logger.info(f"  Complete manual mapping of {len(self.hospital_entities)} hospitals to parent ULS")


def main():
    """Main execution."""
    analyzer = ULSStructureAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
