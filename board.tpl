{# defs #}
{% set empty_line = vb + ws * (widths.board - 2) + vb %}
{% set turn_text = 'Turn' + ws + '#' + (turn - 1 if won else turn)|string %}
{% set turn_width = turn_text|length %}
{# top border #}
{{ hb * widths.board }}
{{ empty_line }}
{# code + turn/winmessage #}
{{ vb + ws * 2 + code + ws * 5 + turn_text + ws * (widths.board - widths.code - turn_width - 9) + vb }}
{{ empty_line }}
{{ vb + hs * (widths.board - 2) + vb }}
{{ empty_line }}
{# guesses #}
{% for line_num in range(max_attempts) %}
{% if line_num >= max_attempts - turn + 1 %}
{% set attempt_idx = max_attempts - line_num - 1 %}
{% set score = 'col:' + scores[attempt_idx][0]|string + ws + 'pos:' + scores[attempt_idx][1]|string %}
{{ vb + ws * 2 + guesses[attempt_idx] + ws * 5 + score + ws * (widths.board - widths.code - score|length - 9) + vb }}
{{ empty_line }}
{% else %}
{{ empty_line }}
{{ empty_line }}
{% endif %}
{% endfor %}
{# bottom border #}
{{ hb * widths.board }}
