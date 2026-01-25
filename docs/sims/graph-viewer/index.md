# Interactive Learning Graph Viewer - GED Science Assessment

## Overview

This interactive graph visualizes the 200 concepts from the GED Science Assessment Targets (Chapter 1). The graph shows the prerequisite relationships between concepts, organized into 9 taxonomy categories aligned with the Science Practices framework.

<iframe src="main.html" width="100%" height="600px" style="border: 1px solid #ccc;"></iframe>

[Open Full Screen Viewer](main.html){:target="_blank" .md-button .md-button--primary}

## Graph Structure

- **Nodes**: 200 concepts from the GED Science Assessment Targets
- **Edges**: 334 dependency relationships showing prerequisites
- **Categories**: 9 taxonomy groupings based on Science Practices
- **Foundational Concepts**: 1 root concept (Scientific Reasoning)
- **Longest Path**: 18 concepts in the deepest learning chain

## Taxonomy Categories

The concepts are organized into 9 categories reflecting the Science Practices and content domains:

| Category | Count | Percentage | Description |
|----------|-------|------------|-------------|
| **LIFE** | 42 | 21.0% | Life Science content topics |
| **DESIGN** | 27 | 13.5% | Investigation Design (SP.2) |
| **STATS** | 26 | 13.0% | Probability & Statistics (SP.8) |
| **EVAL** | 24 | 12.0% | Evaluating Conclusions (SP.4) |
| **THEORY** | 21 | 10.5% | Scientific Theories (SP.7) |
| **COMP** | 18 | 9.0% | Comprehension (SP.1) |
| **FOUND** | 15 | 7.5% | Foundational concepts |
| **EXPRESS** | 15 | 7.5% | Expression of Information (SP.6) |
| **REASON** | 12 | 6.0% | Reasoning from Data (SP.3) |

## Interactive Features

### Search Functionality
- **Type-ahead search**: Find concepts by name (minimum 2 characters)
- **Up to 10 results** displayed in dropdown
- **Category badges**: Each result shows its taxonomy category
- **Focus on select**: Clicking a result highlights the node and its connections

### Category Filtering
- **Toggle visibility**: Click category checkboxes in the legend to show/hide entire groups
- **Color-coded**: Each category has a distinct color matching the graph
- **Check/Uncheck All**: Bulk operations for quick filtering
- **Real-time updates**: Statistics update immediately when filtering

### Graph Navigation
- **Pan**: Click and drag on empty space to move the view
- **Zoom**: Scroll wheel to zoom in/out
- **Node selection**: Click nodes to highlight prerequisite relationships
- **Physics-based layout**: Nodes automatically arrange based on dependencies

### Statistics Panel
Shows real-time counts based on current filters:
- **Visible Nodes**: Number of concepts currently displayed
- **Visible Edges**: Number of dependency arrows shown
- **Foundational Concepts**: Nodes with no prerequisites (root concepts)

### Sidebar Controls
- **Collapsible**: Click the hamburger menu (☰) to collapse/expand sidebar
- **Maximize graph space**: Collapsed sidebar shows only icons
- **Responsive**: Automatically adjusts on mobile devices

## Science Practices Coverage

The learning graph encompasses all 8 GED Science Practices:

1. **SP.1 - Comprehending Scientific Presentations**: Understanding textual and visual scientific materials
2. **SP.2 - Investigation Design**: Creating and evaluating experimental designs
3. **SP.3 - Reasoning from Data**: Drawing conclusions from evidence
4. **SP.4 - Evaluating Conclusions**: Assessing claims against evidence
5. **SP.5 - Working with Findings**: Reconciling multiple findings and theories
6. **SP.6 - Expressing Scientific Information**: Communicating findings visually, numerically, and verbally
7. **SP.7 - Scientific Theories**: Applying models, theories, and formulas
8. **SP.8 - Probability & Statistics**: Statistical analysis and probability calculations

## Key Learning Paths

### Longest Chain (18 concepts)
Starting from Scientific Reasoning → ... → Paradigm Shifts

This path demonstrates the progression from basic scientific reasoning through data analysis, evaluation, and ultimately to understanding how scientific paradigms evolve.

### Foundational Starting Point
**Scientific Reasoning** (ID: 1) is the only concept with no prerequisites, serving as the foundation for all other concepts.

### Terminal Concepts (69 nodes)
Concepts that are not prerequisites for any other concept represent specialized topics or endpoint skills in the assessment framework.

## Using This Viewer

### For Educators
- **Curriculum Planning**: Use dependency chains to sequence instruction
- **Assessment Design**: Ensure prerequisite concepts are taught first
- **Learning Gaps**: Identify missing foundational knowledge by tracing back from advanced concepts
- **Category Focus**: Filter by taxonomy to create targeted lesson plans

### For Learners
- **Study Planning**: Follow prerequisite chains to build knowledge systematically
- **Progress Tracking**: Check off mastered concepts visually
- **Concept Relationships**: Understand how topics connect
- **Category Exploration**: Focus on specific Science Practice areas

### For Test Preparation
- **Coverage Check**: Ensure all 200 concepts are studied
- **Weak Area Identification**: Use categories to find gaps
- **Prerequisite Review**: Follow dependency arrows to review foundations
- **Practice Prioritization**: Focus on high-indegree nodes (many concepts depend on them)

## Technical Details

- **Visualization Library**: vis-network.js
- **Layout Algorithm**: Physics-based (forceAtlas2Based solver)
- **Data Format**: JSON with nodes, edges, and group definitions
- **Source Data**: 200 concepts from GED Science Assessment Targets (October 2020 Edition)
- **Graph Type**: Directed Acyclic Graph (DAG) - no circular dependencies

## Data Quality

Based on quality metrics analysis:
- ✅ **Valid DAG Structure**: No circular dependencies detected
- ✅ **Well-balanced categories**: No category exceeds 30% threshold
- ✅ **Connected graph**: All concepts in single connected component
- ✅ **Average dependencies**: 1.68 per concept (appropriate complexity)

## Related Documentation

- [Course Description](../../learning-graph/course-description.md) - Overview of GED Science Assessment
- [Concept Enumeration](../../learning-graph/list-concepts.md) - Complete list of 200 concepts
- [Quality Metrics](../../learning-graph/quality-metrics.md) - Graph structure validation
- [Taxonomy Distribution](../../learning-graph/taxonomy-distribution.md) - Category analysis

## Source Material

This learning graph was created from:
- **Source**: GED Assessment Guide for Educators: Science (October 2020 Edition)
- **Chapter**: Chapter 1 - Assessment Targets
- **Framework**: Common Core State Standards & Framework for K-12 Science Education
- **Standards**: CCSS ELA/Literacy, CCSS Mathematics, NRC Science Practices

---

*Last Updated*: January 25, 2026
*Graph Version*: 1.0
*License*: CC BY-NC-SA 4.0 DEED
