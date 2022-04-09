# WikiAgg

Neyha Shankar's Grow Therapy coding challenge, 04/09/2022.

This is a class that finds aggregate Wikipedia data on a week or month basis.

## Usage

```python

# Returns a dict of the most viewed articles for a given month (YYYY/MM)
# or week (starting with the Monday of YYYY/MM/DD)
most_viewed_articles('[YYYY/MM/DD | YYYY/MM]')

# Returns the number of views for an article for a week or month
article_view_count('[YYYY/MM/DD | YYYY/MM]', 'Article')

# Returns the day with the most views for an article for a week or month
article_most_viewed_day('[YYYY/MM/DD | YYYY/MM]', 'Article')
```
