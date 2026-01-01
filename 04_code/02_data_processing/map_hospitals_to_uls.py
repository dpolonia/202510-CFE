"""
Map Pre-Integration Hospitals to Parent ULS

Analyzes the 95 pre-integration hospitals and maps them to their parent ULS
based on geographic indicators in hospital names.

Creates comprehensive mapping showing:
- Old hospital name (2017-2023)
- Parent ULS (2024+)
- Confidence level (High/Medium/Low)
- Geographic indicators used for matching

Author: Research Team
Date: 2025-12-31
"""

import pandas as pd
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CROSSWALK_DIR = PROJECT_ROOT / "03_data" / "processed" / "crosswalks"
OUTPUT_DOC = PROJECT_ROOT / "08_documentation"

OUTPUT_DOC.mkdir(parents=True, exist_ok=True)


# Known hospital → ULS mappings based on geographic location
KNOWN_MAPPINGS = {
    # Porto area - Major university hospitals
    'Centro Hospitalar Universitário de Santo António': 'ULS Santo António',
    'Centro Hospitalar Universitário de São João': 'ULS São João',
    'Centro Hospitalar Universitário do Porto': 'ULS Santo António',  # Merged into Santo António

    # Lisboa area - Major university hospitals
    'Centro Hospitalar Universitário Lisboa Norte': 'ULS Santa Maria',
    'Centro Hospitalar Universitário Lisboa Central': 'ULS São José',
    'Centro Hospitalar Universitário de Lisboa Central': 'ULS São José',
    'Centro Hospitalar Lisboa Central': 'ULS São José',

    # Lisboa periphery
    'Hospital Fernando Fonseca': 'ULS Amadora/Sintra',
    'Hospital Professor Doutor Fernando Fonseca': 'ULS Amadora/Sintra',
    'Hospital Garcia de Orta': 'ULS Almada-Seixal',
    'Centro Hospitalar de Setúbal': 'ULS Arrábida',
    'Centro Hospitalar do Barreiro': 'ULS Arco Ribeirinho',
    'Centro Hospitalar Barreiro/Montijo': 'ULS Arco Ribeirinho',

    # Centro region
    'Centro Hospitalar e Universitário de Coimbra': 'ULS Coimbra',
    'Centro Hospitalar Universitário Cova da Beira': 'ULS Cova da Beira',
    'Centro Hospitalar de Leiria': 'ULS Região de Leiria',
    'Hospital Distrital de Santarém': 'ULS Médio Tejo',
    'Centro Hospitalar Médio Tejo': 'ULS Médio Tejo',
    'Centro Hospitalar Tondela-Viseu': 'ULS Viseu Dão-Lafões',
    'Hospital Distrital Figueira da Foz': 'ULS Baixo Mondego',
    'Centro Hospitalar do Baixo Vouga': 'ULS Região de Aveiro',

    # Norte region
    'Centro Hospitalar Póvoa Varzim': 'ULS Póvoa de Varzim/Vila do Conde',
    'Centro Hospitalar Póvoa de Varzim/Vila do Conde': 'ULS Póvoa de Varzim/Vila do Conde',
    'Centro Hospitalar Vila Nova Gaia/Espinho': 'ULS Gaia/Espinho',
    'Centro Hospitalar Vila Nova de Gaia/Espinho': 'ULS Gaia/Espinho',
    'Hospital de Braga': 'ULS Braga',
    'Centro Hospitalar Médio Ave': 'ULS Médio Ave',
    'Centro Hospitalar do Médio Ave': 'ULS Médio Ave',
    'Centro Hospitalar do Alto Ave': 'ULS Alto Ave',
    'Centro Hospitalar de Entre o Douro e Vouga': 'ULS Entre Douro e Vouga',
    'Centro Hospitalar Entre Douro e Vouga': 'ULS Entre Douro e Vouga',
    'Centro Hospitalar do Tâmega e Sousa': 'ULS Tâmega e Sousa',
    'Centro Hospitalar Tâmega e Sousa': 'ULS Tâmega e Sousa',
    'Centro Hospitalar Trás-os-Montes e Alto Douro': 'ULS Trás-os-Montes e Alto Douro',
    'Hospital da Senhora da Oliveira Guimarães': 'ULS Alto Ave',
    'Hospital Distrital S.Maria Maior': 'ULS Barcelos/Esposende',

    # Algarve
    'Centro Hospitalar Universitário do Algarve': 'ULS Algarve',

    # Alentejo
    'Hospital Espírito Santo de Évora': 'ULS Alentejo Central',

    # Lisboa Ocidental
    'Centro Hospitalar de Lisboa': 'ULS Lisboa Ocidental',
    'Centro Hospitalar de Lisboa - Zona Ocidental': 'ULS Lisboa Ocidental',
    'Centro Hospitalar de Lisboa Ocidental': 'ULS Lisboa Ocidental',
    'Centro Hospitalar do Oeste': 'ULS Oeste',

    # Vila Franca de Xira area
    'Hospital de Vila Franca de Xira': 'ULS Estuário do Tejo',

    # Loures
    'Hospital de Loures': 'ULS Loures-Odivelas',
}


def extract_geographic_keywords(hospital_name):
    """Extract geographic location keywords from hospital name."""
    # Common geographic terms
    locations = []

    # Major cities
    cities = [
        'Porto', 'Lisboa', 'Coimbra', 'Braga', 'Setúbal', 'Évora', 'Faro',
        'Aveiro', 'Leiria', 'Guarda', 'Viseu', 'Castelo Branco',
        'Santarém', 'Portalegre', 'Beja', 'Viana do Castelo',
        'Vila Real', 'Bragança', 'Guimarães', 'Almada', 'Amadora',
        'Sintra', 'Cascais', 'Loures', 'Odivelas', 'Ovar', 'Anadia',
        'Barcelos', 'Esposende', 'Gaia', 'Espinho', 'Matosinhos'
    ]

    # Regions
    regions = [
        'Algarve', 'Alentejo', 'Minho', 'Douro', 'Vouga', 'Mondego',
        'Tejo', 'Tâmega', 'Sousa', 'Dão', 'Lafões', 'Beira',
        'Trás-os-Montes', 'Alto Douro', 'Arrábida', 'Lezíria'
    ]

    # Compass directions
    directions = ['Norte', 'Sul', 'Centro', 'Alto', 'Baixo', 'Médio', 'Litoral']

    name_lower = hospital_name.lower()

    for city in cities:
        if city.lower() in name_lower:
            locations.append(city)

    for region in regions:
        if region.lower() in name_lower:
            locations.append(region)

    # Extract composite locations
    if 'vila nova de gaia' in name_lower:
        locations.append('Vila Nova de Gaia')
    if 'póvoa de varzim' in name_lower or 'povoa varzim' in name_lower:
        locations.append('Póvoa de Varzim')
    if 'vila do conde' in name_lower:
        locations.append('Vila do Conde')

    return locations


def find_best_uls_match(hospital_name, uls_list):
    """
    Find best ULS match for hospital based on geographic overlap.

    Returns: (best_match, confidence, matching_keywords)
    """
    # Check known mappings first
    for known_hospital, known_uls in KNOWN_MAPPINGS.items():
        if known_hospital.lower() in hospital_name.lower():
            return (known_uls, 'High', f'Known mapping: {known_hospital}')

    # Extract hospital keywords
    hospital_keywords = extract_geographic_keywords(hospital_name)

    if not hospital_keywords:
        return (None, 'Low', 'No geographic keywords found')

    # Score each ULS
    best_match = None
    best_score = 0
    matching_keywords = []

    for uls in uls_list:
        score = 0
        matches = []

        uls_lower = uls.lower()

        for keyword in hospital_keywords:
            if keyword.lower() in uls_lower:
                score += 1
                matches.append(keyword)

        if score > best_score:
            best_score = score
            best_match = uls
            matching_keywords = matches

    if best_score >= 2:
        confidence = 'High'
    elif best_score == 1:
        confidence = 'Medium'
    else:
        confidence = 'Low'

    return (best_match, confidence, ', '.join(matching_keywords) if matching_keywords else 'No match')


def create_hospital_uls_mapping():
    """Create comprehensive hospital → ULS mapping."""
    logger.info("="*70)
    logger.info("MAPPING PRE-INTEGRATION HOSPITALS TO PARENT ULS")
    logger.info("="*70 + "\n")

    # Load crosswalk
    crosswalk_file = CROSSWALK_DIR / "entity_name_crosswalk_standardized.csv"
    df = pd.read_csv(crosswalk_file, encoding='utf-8-sig')

    # Load canonical ULS list
    uls_file = CROSSWALK_DIR / "canonical_uls_list.csv"
    uls_df = pd.read_csv(uls_file)
    uls_list = ['ULS ' + name for name in uls_df['uls_name'].tolist()]

    logger.info(f"Loaded {len(uls_list)} canonical ULS")

    # Filter hospitals
    hospitals_df = df[df['entity_type'] == 'Hospital/Centro Hospitalar'].copy()
    logger.info(f"Found {len(hospitals_df)} pre-integration hospitals\n")

    # Map each hospital
    mappings = []

    for idx, row in hospitals_df.iterrows():
        hospital_name = row['entity_name']
        hospital_std = row['entity_name_standardized']

        # Find best ULS match
        uls_match, confidence, keywords = find_best_uls_match(hospital_name, uls_list)

        mappings.append({
            'old_hospital_name': hospital_name,
            'hospital_standardized': hospital_std,
            'parent_uls': uls_match,
            'confidence': confidence,
            'matching_keywords': keywords,
            'mapping_method': 'Known' if confidence == 'High' and 'Known mapping' in keywords else 'Geographic'
        })

    mapping_df = pd.DataFrame(mappings)

    # Summary statistics
    logger.info("\nMAPPING SUMMARY")
    logger.info("="*70)

    total = len(mapping_df)
    high_conf = len(mapping_df[mapping_df['confidence'] == 'High'])
    medium_conf = len(mapping_df[mapping_df['confidence'] == 'Medium'])
    low_conf = len(mapping_df[mapping_df['confidence'] == 'Low'])
    unmapped = len(mapping_df[mapping_df['parent_uls'].isna()])

    logger.info(f"\nTotal hospitals: {total}")
    logger.info(f"  High confidence: {high_conf} ({high_conf/total*100:.1f}%)")
    logger.info(f"  Medium confidence: {medium_conf} ({medium_conf/total*100:.1f}%)")
    logger.info(f"  Low confidence: {low_conf} ({low_conf/total*100:.1f}%)")
    logger.info(f"  Unmapped: {unmapped} ({unmapped/total*100:.1f}%)")

    # Show high confidence mappings
    logger.info("\n" + "="*70)
    logger.info("HIGH CONFIDENCE MAPPINGS (Sample)")
    logger.info("="*70)

    high_df = mapping_df[mapping_df['confidence'] == 'High'].head(20)
    for idx, row in high_df.iterrows():
        logger.info(f"\n{row['old_hospital_name']}")
        logger.info(f"  → {row['parent_uls']}")
        logger.info(f"  Match: {row['matching_keywords']}")

    # Show uncertain mappings
    logger.info("\n" + "="*70)
    logger.info("UNCERTAIN MAPPINGS (Require Manual Review)")
    logger.info("="*70)

    uncertain_df = mapping_df[mapping_df['confidence'].isin(['Low', 'Medium'])]
    for idx, row in uncertain_df.iterrows():
        logger.info(f"\n{row['old_hospital_name']}")
        logger.info(f"  → {row['parent_uls']} (Confidence: {row['confidence']})")
        logger.info(f"  Keywords: {row['matching_keywords']}")

    # Save mapping
    output_file = CROSSWALK_DIR / "hospital_to_uls_mapping.csv"
    mapping_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    logger.info(f"\n\nMapping saved: {output_file}")

    # Create markdown documentation
    create_mapping_documentation(mapping_df)

    return mapping_df


def create_mapping_documentation(mapping_df):
    """Create markdown documentation of hospital→ULS mappings."""
    logger.info("\nGenerating mapping documentation...")

    doc_lines = []
    doc_lines.append("# Hospital to ULS Mapping")
    doc_lines.append("## Pre-Integration Hospitals (2017-2023) → Parent ULS (2024+)")
    doc_lines.append("")
    doc_lines.append("**Generated**: 2025-12-31")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")

    # Summary
    total = len(mapping_df)
    high = len(mapping_df[mapping_df['confidence'] == 'High'])
    medium = len(mapping_df[mapping_df['confidence'] == 'Medium'])
    low = len(mapping_df[mapping_df['confidence'] == 'Low'])

    doc_lines.append("## Summary")
    doc_lines.append("")
    doc_lines.append(f"- **Total hospitals mapped**: {total}")
    doc_lines.append(f"- **High confidence**: {high} ({high/total*100:.1f}%)")
    doc_lines.append(f"- **Medium confidence**: {medium} ({medium/total*100:.1f}%)")
    doc_lines.append(f"- **Low confidence**: {low} ({low/total*100:.1f}%)")
    doc_lines.append("")

    # Mappings by ULS
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## Mappings by Parent ULS")
    doc_lines.append("")

    for uls in sorted(mapping_df['parent_uls'].dropna().unique()):
        uls_hospitals = mapping_df[mapping_df['parent_uls'] == uls].sort_values('confidence', ascending=False)

        doc_lines.append(f"### {uls}")
        doc_lines.append("")
        doc_lines.append(f"**Incorporated hospitals**: {len(uls_hospitals)}")
        doc_lines.append("")

        for idx, row in uls_hospitals.iterrows():
            conf_emoji = {'High': '✓', 'Medium': '⚠', 'Low': '?'}[row['confidence']]
            doc_lines.append(f"{conf_emoji} **{row['old_hospital_name']}**")
            doc_lines.append(f"  - Confidence: {row['confidence']}")
            doc_lines.append(f"  - Match: {row['matching_keywords']}")
            doc_lines.append("")

        doc_lines.append("")

    # Unmapped hospitals
    unmapped = mapping_df[mapping_df['parent_uls'].isna()]
    if len(unmapped) > 0:
        doc_lines.append("---")
        doc_lines.append("")
        doc_lines.append("## Unmapped Hospitals (Require Manual Research)")
        doc_lines.append("")

        for idx, row in unmapped.iterrows():
            doc_lines.append(f"- {row['old_hospital_name']}")

        doc_lines.append("")

    # Save
    doc_file = OUTPUT_DOC / "hospital_to_uls_mapping.md"
    with open(doc_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(doc_lines))

    logger.info(f"Documentation saved: {doc_file}")


def main():
    """Main execution."""
    mapping_df = create_hospital_uls_mapping()

    logger.info("\n" + "="*70)
    logger.info("MAPPING COMPLETE")
    logger.info("="*70)
    logger.info("\nOutputs:")
    logger.info("  1. CSV: 03_data/processed/crosswalks/hospital_to_uls_mapping.csv")
    logger.info("  2. Documentation: 08_documentation/hospital_to_uls_mapping.md")
    logger.info("\nNext steps:")
    logger.info("  1. Review uncertain mappings (Medium/Low confidence)")
    logger.info("  2. Manually verify against official ULS integration decrees")
    logger.info("  3. Update parent_uls column in crosswalk for quality metric aggregation")


if __name__ == "__main__":
    main()
