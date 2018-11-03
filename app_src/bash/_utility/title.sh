
LEN="80"
BAR=$(eval "printf '=%.0s' {1..${LEN}}")

function title()
{
  echo $BAR
  echo " -> "$1
  echo $BAR
}
export -f title
