# Prompt to Create a Chapter Generator

!!! prompt
    Use the skill-creator skill to create a new skill called `book-chapter-generator`.
    This skill will look at the following resources:

## Input Resources
1. Course Description at /docs/course-description.md
2. Learning Graph at /docs/learning-graph/learning-graph.json
3. Concept Taxonomy at /docs/learning-graph/concept-taxonomy.md

## Step 1: Design Chapters

It will then suggest an outline of about 12 chapters for this book assuming you have about 200 concepts to cover.
Each chapter will have a Chapter Title in Title Case and be no longer than 200 characters long.
This is so that the listing of the chapters can fit on a single line per chapter.
Use the course description and the learning graph to make sure that

1. Each concept is covered once
2. No concept is introduced before its dependencies are covered
3. No chapter contains too many or two few concepts

You may, at your discretion have as few as six chapters, or as many as 20 chapters.

## Step 2: Present Chapter Design to the User

Present a simple list of Chapter Titles to the user.  Only present the
Chapter Titles and a single sentence of what that chapter contains.
You may also discuss any challenges you found and how your design met these challenges.

Ask the user if they approve the design (y/n) and if no, what changes they want to make.

## Step 3: Generate the Chapter Outline Files

For each chapter, create a "URL-PATH-NAME" which is only lowercase letters and dashes. Do not put any special characters in the URL-PATH-NAME.  Use abbreviations if you need to keep the URL-PATH-NAME short.

Create a series of directories using the following structure where URL-PATH-NAME is the name for each chapter.

```
chapters/index.md
chapters/01-URL-PATH-NAME/index.md
chapters/02-URL-PATH-NAME/index.md
chapters/03-URL-PATH-NAME/index.md
```

## Step 4: Add Content to the Index of Each Chapter

Add content to each chapter index.md file including:

1. The Chapter Title in a level 1 header
2. A summary of what is in the chapter in a level 2 ## Summary section
3. A numbered markdown list of concepts in a level 2 ## Concepts Covered section
4. A 'TODO: Generate Chapter Content" which will be used by a future skill