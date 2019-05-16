Available colors:
{% for col, hrc in human_readable_colors.iteritems() %}
{% if loop.index0 is divisibleby 4 and loop.index0 > 0 %}{{ '\n    ' }}{% endif %}{{ colors[col] + hrc|lower + reset + '   ' }}{% endfor %}
