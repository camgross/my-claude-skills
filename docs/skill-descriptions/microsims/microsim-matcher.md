# MicroSim Matcher

The microsim-matcher skill analyzes diagram, chart, or simulation specifications
and returns a ranked list of the most suitable MicroSim generator skills to use.
It compares specifications against all available generators and provides match
scores with detailed reasoning.

## Key Capabilities

This skill provides:

- **Specification Analysis**: Parses diagram/chart requirements
- **Multi-Generator Comparison**: Evaluates against all 9+ generators
- **Match Scoring**: 0-100 scale for each generator
- **Ranked Recommendations**: Ordered list with reasoning
- **Capability Matching**: Maps features to generator strengths

## Available Generators Evaluated

The skill evaluates matches against:

1. **microsim-p5** - General p5.js simulations and animations
2. **chartjs-generator** - Standard statistical charts
3. **math-function-plotter-plotly** - Mathematical function plots
4. **mermaid-generator** - Flowcharts and workflow diagrams
5. **vis-network** - Network graphs with nodes and edges
6. **causal-loop-microsim-generator** - Systems thinking diagrams
7. **timeline-generator** - Chronological event timelines
8. **map-generator** - Geographic visualizations
9. **venn-diagram-generator** - Set relationship diagrams
10. **bubble-chart-generator** - Priority matrices

## When to Use

Use this skill when:

- A user has a diagram specification and needs generator guidance
- Describing a desired MicroSim without specifying a generator
- Asking "Which MicroSim generator should I use for...?"
- Comparing multiple generator options
- Recommending the best generator for a specification

## Matching Criteria

The skill evaluates:

- **Interactivity Requirements**: Static vs animated vs user-controlled
- **Data Type**: Categorical, numerical, temporal, spatial
- **Visual Complexity**: Simple shapes to complex visualizations
- **Layout Needs**: Fixed, responsive, zoomable
- **Special Features**: Tooltips, legends, export capabilities

## Output Format

The skill returns a ranked list with:

```
1. microsim-p5 (Score: 95/100)
   Reasoning: Best for custom animations with physics simulation...

2. chartjs-generator (Score: 72/100)
   Reasoning: Could work for the data display but lacks...
```

## Integration

This skill is typically used at the start of MicroSim development to
ensure the right tool is selected before implementation begins.
