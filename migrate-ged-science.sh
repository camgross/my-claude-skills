#!/bin/bash
# Script to migrate GED Science content to new repository
# Run this script from the claude-skills directory

set -e

SOURCE_DIR="/Users/camgross/Projects/claude-skills"
DEST_DIR="/Users/camgross/Projects/GED-Science-prep"

echo "Creating destination directories..."
mkdir -p "$DEST_DIR/docs/chapters"
mkdir -p "$DEST_DIR/docs/learning-graph"
mkdir -p "$DEST_DIR/docs/sims"
mkdir -p "$DEST_DIR/logs"

echo "Copying GED Science chapters..."
for i in {01..12}; do
    for dir in "$SOURCE_DIR/docs/chapters/$i-"*; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            echo "  Copying $dirname..."
            cp -r "$dir" "$DEST_DIR/docs/chapters/"
        fi
    done
done

echo "Copying chapter index..."
cp "$SOURCE_DIR/docs/chapters/index.md" "$DEST_DIR/docs/chapters/index.md"

echo "Copying learning graph files..."
cp "$SOURCE_DIR/docs/learning-graph/course-description.md" "$DEST_DIR/docs/learning-graph/"
cp "$SOURCE_DIR/docs/learning-graph/learning-graph.csv" "$DEST_DIR/docs/learning-graph/"
cp "$SOURCE_DIR/docs/learning-graph/learning-graph.json" "$DEST_DIR/docs/learning-graph/"
cp "$SOURCE_DIR/docs/learning-graph/list-concepts.md" "$DEST_DIR/docs/learning-graph/"

echo "Copying GED Science MicroSims..."
for sim in ged-science-assessment-framework scientific-reasoning-process-flow scientific-method-cycle scientific-data-visualization-types quantitative-qualitative-data-collection scientific-communication-process; do
    if [ -d "$SOURCE_DIR/docs/sims/$sim" ]; then
        echo "  Copying $sim..."
        cp -r "$SOURCE_DIR/docs/sims/$sim" "$DEST_DIR/docs/sims/"
    fi
done

echo "Copying assessment guide..."
if [ -f "$SOURCE_DIR/assessment-guide-for-educators-science.pdf" ]; then
    cp "$SOURCE_DIR/assessment-guide-for-educators-science.pdf" "$DEST_DIR/"
fi

echo "Migration complete!"
echo "Next steps:"
echo "1. Review files in $DEST_DIR"
echo "2. Create mkdocs.yml and README.md for new repository"
echo "3. Initialize git repository in $DEST_DIR"
echo "4. Restore original files in $SOURCE_DIR using git checkout"
